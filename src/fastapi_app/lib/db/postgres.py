import typing

import sqlalchemy.ext.asyncio as sa_asyncio

import lib.app.settings as app_settings


class AsyncDB:
    """Async DB connection."""

    def __init__(self, settings: app_settings.Settings):
        self.database_dsn = settings.db.dsn
        self.engine = sa_asyncio.create_async_engine(self.database_dsn, echo=settings.project.debug, future=True)
        self.async_session = sa_asyncio.async_sessionmaker(
            self.engine, class_=sa_asyncio.AsyncSession, expire_on_commit=False
        )


async def get_session(settings: app_settings.Settings) -> typing.AsyncGenerator[sa_asyncio.AsyncSession, typing.Any]:
    db = AsyncDB(settings)
    async with db.async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            await db.engine.dispose()
