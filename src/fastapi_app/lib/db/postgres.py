import typing

import sqlalchemy.ext.asyncio as sa_asyncio

import lib.app.split_settings as app_split_settings


class AsyncDB:
    """Async DB connection."""

    def __init__(self, settings: app_split_settings.DBSettings):
        self.engine = sa_asyncio.create_async_engine(
            url=settings.dsn,
            pool_size=settings.pool_size,
            pool_pre_ping=settings.pool_pre_ping,
            echo=settings.echo,
            future=True,
        )
        self.async_session = sa_asyncio.async_sessionmaker(
            bind=self.engine,
            autocommit=settings.auto_commit,
            autoflush=settings.auto_flush,
            expire_on_commit=settings.expire_on_commit,
            class_=sa_asyncio.AsyncSession,
        )


async def get_session(
    settings: app_split_settings.DBSettings,
) -> typing.AsyncGenerator[sa_asyncio.AsyncSession, typing.Any]:
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
