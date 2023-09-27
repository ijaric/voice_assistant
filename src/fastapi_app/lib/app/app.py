import logging

import fastapi
import sqlalchemy
import sqlalchemy.ext.asyncio as sa_asyncio

import lib.app.settings as app_settings
import lib.clients as clients

# import sqlalchemy.ext.asyncio as sa_asyncio


logger = logging.getLogger(__name__)


class Application:
    def __init__(self) -> None:
        self.settings = app_settings.settings
        self.logger = logging.getLogger(__name__)
        self.producer = None

    async def create_app(self) -> fastapi.FastAPI:
        postgres_client = clients.get_async_session(self.settings.postgres)

        app = fastapi.FastAPI(
            title="FastAPI",
            version="0.1.0",
            docs_url="/api/openapi",
            openapi_url="/api/openapi.json",
            default_response_class=fastapi.responses.ORJSONResponse,
        )

        router = fastapi.APIRouter()

        @router.get("/health")
        async def health(get_async_session: sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession]):
            async with get_async_session.begin() as session:
                statement = sqlalchemy.text("SELECT 1")
                results = await session.execute(statement)
                print(results.unique().scalar_one_or_none())
            return {"status": "ok"}

        app.include_router(router)
        # app.include_router(api_handlers.user_router, prefix="/api/v1/users", tags=["users"])
        # app.include_router(api_handlers.movie_router, prefix="/api/v1/movies", tags=["movies"])

        @app.on_event("startup")
        async def startup_event():  # noqa: ANN202
            self.logger.info("Starting server")

        @app.on_event("shutdown")
        async def shutdown_event():  # noqa: ANN202
            self.logger.info("Shutting down server")

        return app
