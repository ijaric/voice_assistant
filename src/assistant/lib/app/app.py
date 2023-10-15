import dataclasses
import logging
import logging.config as logging_config
import typing

import fastapi
import uvicorn

import lib.api.v1.handlers as api_v1_handlers
import lib.app.errors as app_errors
import lib.app.settings as app_settings
import lib.app.split_settings as app_split_settings
import lib.clients as clients
import lib.models as models
import lib.stt as stt
import lib.tts as tts

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DisposableResource:
    name: str
    dispose_callback: typing.Awaitable[typing.Any]


class Application:
    def __init__(
        self,
        settings: app_settings.Settings,
        fastapi_app: fastapi.FastAPI,
        disposable_resources: list[DisposableResource],
    ) -> None:
        self._settings = settings
        self._fastapi_app = fastapi_app
        self._disposable_resources = disposable_resources

    @classmethod
    def from_settings(cls, settings: app_settings.Settings) -> typing.Self:
        # Logging

        logging_config.dictConfig(app_split_settings.get_logging_config(**settings.logger.model_dump()))

        logger.info("Initializing application")
        disposable_resources = []

        # Global clients

        logger.info("Initializing global clients")
        postgres_client = clients.AsyncPostgresClient(settings=settings)

        disposable_resources.append(
            DisposableResource(
                name="postgres_client",
                dispose_callback=postgres_client.dispose_callback(),
            )
        )

        # Clients

        logger.info("Initializing clients")

        http_yandex_tts_client = clients.AsyncHttpClient(
            proxy_settings=settings.proxy,
            base_url=settings.tts_yandex.base_url,
            headers=settings.tts_yandex.base_headers,
            timeout=settings.tts_yandex.timeout_seconds,
        )
        http_eleven_labs_tts_client = clients.AsyncHttpClient(
            base_url=settings.tts_eleven_labs.base_url,
            headers=settings.tts_eleven_labs.base_headers,
            timeout=settings.tts_eleven_labs.timeout_seconds,
        )

        disposable_resources.append(
            DisposableResource(
                name="http_client yandex",
                dispose_callback=http_yandex_tts_client.close(),
            )
        )
        disposable_resources.append(
            DisposableResource(
                name="http_client eleven labs",
                dispose_callback=http_eleven_labs_tts_client.close(),
            )
        )

        # Repositories

        logger.info("Initializing repositories")
        stt_repository: stt.STTProtocol = stt.OpenaiSpeechRepository(settings=settings)

        tts_yandex_repository = tts.TTSYandexRepository(
            tts_settings=app_split_settings.TTSYandexSettings(),
            client=http_yandex_tts_client,
        )
        tts_eleven_labs_repository = tts.TTSElevenLabsRepository(
            tts_settings=app_split_settings.TTSElevenLabsSettings(),
            client=http_eleven_labs_tts_client,
            is_models_from_api=True,
        )

        # Caches

        logger.info("Initializing caches")

        # Services

        logger.info("Initializing services")
        stt_service: stt.SpeechService = stt.SpeechService(repository=stt_repository)

        tts_service: tts.TTSService = tts.TTSService(
            repositories={
                models.VoiceModelProvidersEnum.YANDEX: tts_yandex_repository,
                models.VoiceModelProvidersEnum.ELEVEN_LABS: tts_eleven_labs_repository,
            },
        )

        # Handlers

        logger.info("Initializing handlers")
        liveness_probe_handler = api_v1_handlers.basic_router

        # TODO: объявить сервисы tts и openai и добавить их в voice_response_handler
        voice_response_handler = api_v1_handlers.VoiceResponseHandler(
            stt=stt_service,
            # tts=tts_service,  # TODO
        ).router

        tts_handler = api_v1_handlers.TTSHandler(tts=tts_service).router

        logger.info("Creating application")

        fastapi_app = fastapi.FastAPI(
            title=settings.app.title,
            version=settings.app.version,
            docs_url=settings.app.docs_url,
            openapi_url=settings.app.openapi_url,
            default_response_class=fastapi.responses.ORJSONResponse,
        )

        # Routes
        fastapi_app.include_router(liveness_probe_handler, prefix="/api/v1/health", tags=["health"])
        fastapi_app.include_router(voice_response_handler, prefix="/api/v1/voice", tags=["voice"])
        fastapi_app.include_router(tts_handler, prefix="/api/v1/tts", tags=["tts"])

        application = Application(
            settings=settings,
            fastapi_app=fastapi_app,
            disposable_resources=disposable_resources,
        )

        logger.info("Initializing application finished")

        return application

    async def start(self) -> None:
        try:
            config = uvicorn.Config(
                app=self._fastapi_app,
                host=self._settings.api.host,
                port=self._settings.api.port,
            )
            server = uvicorn.Server(config)
            await server.serve()
        except BaseException as unexpected_error:
            logger.exception("FastAPI failed to start")
            raise app_errors.StartServerError("FastAPI failed to start") from unexpected_error

    async def dispose(self) -> None:
        logger.info("Application is shutting down...")
        dispose_errors = []

        for resource in self._disposable_resources:
            logger.info("Disposing %s...", resource.name)
            try:
                await resource.dispose_callback
            except Exception as unexpected_error:
                dispose_errors.append(unexpected_error)
                logger.exception("Failed to dispose %s", resource.name)
            else:
                logger.info("%s has been disposed", resource.name)

        if len(dispose_errors) != 0:
            logger.error("Application has shut down with errors")
            raise app_errors.DisposeError("Application has shut down with errors, see logs above")

        logger.info("Application has successfully shut down")
