import functools

import pydantic_settings
from pydantic import Field, field_validator


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
    debug: str = "false"
    db: DbSettings = Field(default_factory=DbSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)

    jwt_secret_key: str

    @field_validator("debug")
    @classmethod
    def validate_debug(cls, v: str) -> bool:
        return v.lower() == "true"


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
