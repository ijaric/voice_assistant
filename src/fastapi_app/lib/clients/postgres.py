import sqlalchemy.ext.asyncio as sa_asyncio

import lib.app.split_settings as app_split_settings


async def get_async_session(
    settings: app_split_settings.DBSettings,
) -> sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession]:
    engine = sa_asyncio.create_async_engine(
        url=settings.dsn,
        pool_size=settings.pool_size,
        pool_pre_ping=settings.pool_pre_ping,
        echo=settings.echo,
        future=True,
    )

    async_session = sa_asyncio.async_sessionmaker(
        bind=engine,
        autocommit=settings.auto_commit,
        autoflush=settings.auto_flush,
        expire_on_commit=settings.expire_on_commit,
    )

    return async_session  # noqa: RET504
