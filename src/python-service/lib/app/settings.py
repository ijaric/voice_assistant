import typing

import pydantic

LogLevel = typing.Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


class Settings(pydantic.BaseSettings):
    # App

    APP_ENV: str = "development"
    APP_NAME: str = "discord-chatbot-backend"
    APP_VERSION: str = "0.0.1"

    # Logging

    LOGS_MIN_LEVEL: LogLevel = "DEBUG"
    LOGS_FORMAT: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    # Server

    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8080

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


__all__ = [
    "Settings",
]
