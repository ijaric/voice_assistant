import sqlalchemy.ext.asyncio as sa_asyncio

import lib.app.settings as app_settings


class AsyncPostgresClient:
    """Async Postgres Client that return sessionmaker."""

    def __init__(self, settings: app_settings.Settings) -> None:
        self.settings = settings.postgres
        self.async_enging = sa_asyncio.create_async_engine(
            url=self.settings.dsn,
            pool_size=self.settings.pool_size,
            pool_pre_ping=self.settings.pool_pre_ping,
            echo=self.settings.echo,
            future=True,
        )

    def get_async_session(self) -> sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession]:
        async_session = sa_asyncio.async_sessionmaker(
            bind=self.async_enging,
            autocommit=self.settings.auto_commit,
            autoflush=self.settings.auto_flush,
            expire_on_commit=self.settings.expire_on_commit,
        )

        return async_session  # noqa: RET504

    async def dispose_callback(self) -> None:
        await self.async_enging.dispose()
