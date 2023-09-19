import asyncio
import dataclasses
import logging
import typing

import aiohttp.web as aiohttp_web
import lib.api.rest.v1.health as health_handlers
import lib.app.errors as app_errors
import lib.app.settings as app_settings
import typing_extensions

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DisposableResource:
    name: str
    dispose_callback: typing.Awaitable[typing.Any]


class Application:
    def __init__(
        self,
        settings: app_settings.Settings,
        aio_app: aiohttp_web.Application,
        disposable_resources: typing.Sequence[DisposableResource],
    ) -> None:
        self._settings = settings
        self._aio_app = aio_app
        self._disposable_resources = disposable_resources

    @classmethod
    def from_settings(cls, settings: app_settings.Settings) -> typing_extensions.Self:
        # Logging

        logging.basicConfig(
            level=settings.LOGS_MIN_LEVEL,
            format=settings.LOGS_FORMAT,
        )

        logger.info("Initializing application")
        disposable_resources = []

        # Global clients

        logger.info("Initializing global clients")

        # Clients

        logger.info("Initializing clients")

        # Repositories

        logger.info("Initializing repositories")

        # Caches

        logger.info("Initializing caches")

        # Services

        logger.info("Initializing services")

        # Handlers

        logger.info("Initializing handlers")
        liveness_probe_handler = health_handlers.LivenessProbeHandler()

        logger.info("Creating application")
        aio_app = aiohttp_web.Application()

        # Routes
        aio_app.add_routes(
            [
                aiohttp_web.get(
                    "/api/v1/health/liveness",
                    liveness_probe_handler.process,
                ),
            ]
        )

        application = Application(
            settings=settings,
            aio_app=aio_app,
            disposable_resources=disposable_resources,
        )

        logger.info("Initializing application finished")

        return application

    async def start(self) -> None:
        logger.info("Discord server is starting")

        try:
            await aiohttp_web._run_app(
                app=self._aio_app,
                host=self._settings.SERVER_HOST,
                port=self._settings.SERVER_PORT,
            )
        except asyncio.CancelledError:
            logger.info("HTTP server has been interrupted")
        except BaseException as unexpected_error:
            logger.exception("HTTP server failed to start")
            raise app_errors.StartServerError(
                "HTTP server failed to start"
            ) from unexpected_error

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
            raise app_errors.DisposeError(
                "Application has shut down with errors, see logs above"
            )

        logger.info("Application has successfully shut down")


__all__ = [
    "Application",
]
