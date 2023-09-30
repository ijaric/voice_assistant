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
import lib.joke.services as joke_services

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
        http_client = clients.get_async_http_session()

        disposable_resources.append(
            DisposableResource(
                name="postgres_client",
                dispose_callback=postgres_client.dispose_callback(),
            )
        )

        # Clients

        logger.info("Initializing clients")

        # Repositories

        logger.info("Initializing repositories")

        # Caches

        logger.info("Initializing caches")

        # Services

        logger.info("Initializing services")
        jk_serivces = joke_services.JokeService(http_client=http_client)

        # Handlers

        logger.info("Initializing handlers")
        liveness_probe_handler = api_v1_handlers.basic_router
        joke_handler = api_v1_handlers.get_joke(joke_service=jk_serivces)

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
