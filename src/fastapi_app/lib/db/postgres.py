import typing

from lib.app import settings as app_settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

settings = app_settings.get_settings()

# Создаём базовый класс для будущих моделей


class Base(DeclarativeBase):
    pass


# Создаём движок
# Настройки подключения к БД передаём из переменных окружения, которые заранее загружены в файл настроек
class AsyncDB:
    def __init__(self):
        self.database_dsn = (
            f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}"
            f"@{settings.db.host}:{settings.db.port}/{settings.db.name}"
        )
        self.engine = create_async_engine(
            self.database_dsn, echo=settings.debug, future=True
        )
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )


db = AsyncDB()


async def get_session() -> typing.AsyncGenerator[AsyncSession, typing.Any]:
    async with db.async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
