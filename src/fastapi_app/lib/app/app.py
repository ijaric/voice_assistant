import logging
import logging.config as logging_config

import fastapi

import lib.api.v1.endpoints as api_v1_endpoints

from .logger import LOGGING
from .settings import get_settings

logging_config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Application:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        self.producer = None

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
            title="FastAPI",
            version="0.1.0",
            docs_url="/api/openapi",
            openapi_url="/api/openapi.json",
            default_response_class=fastapi.responses.ORJSONResponse,
        )
        app = self.setup_application(app)

        @app.on_event("startup")
        async def startup_event():
            self.logger.info("Starting server")

        @app.on_event("shutdown")
        async def shutdown_event():
            self.logger.info("Shutting down server")

        return app


# Позволяет запускать через uvicorn lib.app.app:create_application --reload
def create_application():
    application = Application()
    return application.create_app()
