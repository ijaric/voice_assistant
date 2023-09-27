import logging

import fastapi

import lib.app.settings as app_settings

logger = logging.getLogger(__name__)


class Application:
    def __init__(self) -> None:
        self.settings = app_settings
        self.logger = logging.getLogger(__name__)
        self.producer = None

    def create_app(self) -> fastapi.FastAPI:
        app = fastapi.FastAPI(
            title="FastAPI",
            version="0.1.0",
            docs_url="/api/openapi",
            openapi_url="/api/openapi.json",
            default_response_class=fastapi.responses.ORJSONResponse,
        )

        # app.include_router(api_handlers.user_router, prefix="/api/v1/users", tags=["users"])
        # app.include_router(api_handlers.movie_router, prefix="/api/v1/movies", tags=["movies"])

        @app.on_event("startup")
        async def startup_event():
            self.logger.info("Starting server")

        @app.on_event("shutdown")
        async def shutdown_event():
            self.logger.info("Shutting down server")

        return app
