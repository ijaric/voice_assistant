import typing

from libs.app import settings as libs_app_settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

settings = libs_app_settings.get_settings()

# Создаём базовый класс для будущих моделей


class Base(DeclarativeBase):
    pass


# Создаём движок
# Настройки подключения к БД передаём из переменных окружения, которые заранее загружены в файл настроек

database_dsn = (
    f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}"
    f"@{settings.db.host}:{settings.db.port}/{settings.db.name}"
)

engine = create_async_engine(database_dsn, echo=True, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> typing.AsyncGenerator[AsyncSession, typing.Any]:
    async with async_session() as session:
        yield session
