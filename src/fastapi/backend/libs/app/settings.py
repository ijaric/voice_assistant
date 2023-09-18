import functools

import pydantic_settings
from dotenv import load_dotenv
from pydantic import Field

load_dotenv('.env.dev')


class DbSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="db_")

    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    name: str


class ApiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="server_")

    host: str = "0.0.0.0"
    port: int = 8000


class Settings(pydantic_settings.BaseSettings):
    db: DbSettings = Field(default_factory=DbSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)

    jwt_secret_key: str


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
