import functools

import pydantic
import pydantic_settings


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
    db: DbSettings = pydantic.Field(default_factory=lambda: DbSettings())
    api: ApiSettings = pydantic.Field(default_factory=lambda: ApiSettings())

    jwt_secret_key: str = pydantic.Field(default=...)

    @pydantic.field_validator("debug")
    @classmethod
    def validate_debug(cls, v: str) -> bool:
        return v.lower() == "true"


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
