import typing

import sqlalchemy.ext.asyncio as sa_asyncio

import lib.app.settings as app_settings


class AsyncDB:
    """Async DB connection."""

    def __init__(self, settings: app_settings.Settings):
        self.engine = sa_asyncio.create_async_engine(
            url=settings.db.dsn,
            pool_size=settings.db.pool_size,
            pool_pre_ping=settings.db.pool_pre_ping,
            echo=settings.db.echo,
            future=True,
        )
        self.async_session = sa_asyncio.async_sessionmaker(
            bind=self.engine,
            autocommit=settings.db.auto_commit,
            autoflush=settings.db.auto_flush,
            expire_on_commit=settings.db.expire_on_commit,
            class_=sa_asyncio.AsyncSession,
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
