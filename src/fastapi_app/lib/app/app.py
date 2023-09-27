import logging
import logging.config as logging_config
from contextlib import asynccontextmanager

import fastapi

import lib.api.v1.endpoints as api_v1_endpoints
import lib.app.settings as app_settings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Application:
    def __init__(self) -> None:
        self.settings = app_settings.settings
        self.logger = logging.getLogger(__name__)
        self.producer = None

    @asynccontextmanager
    async def lifespan(self, app: fastapi.FastAPI):
        self.logger.info("Starting server")
        yield
        # Clean up the ML models and release the resources
        self.logger.info("Shutting down server")

    def setup_application(self, app: fastapi.FastAPI) -> fastapi.FastAPI:
        logger.info("Initializing application")

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

        app.include_router(api_v1_endpoints.health.health_router, prefix="/api/v1/health", tags=["health"])

        logger.info("Initializing handlers")

        logger.info("Initializing application finished")

        return app

    def create_app(self) -> fastapi.FastAPI:
        app = fastapi.FastAPI(
            title=self.settings.app.title,
            version=self.settings.app.version,
            docs_url=self.settings.app.docs_url,
            openapi_url=self.settings.app.openapi_url,
            default_response_class=fastapi.responses.ORJSONResponse,
            lifespan=self.lifespan,
        )
        app = self.setup_application(app)

        app.state.settings = self.settings

        return app


# Позволяет запускать через uvicorn lib.app.app:create_application --reload
def create_application():
    application = Application()
    return application.create_app()
