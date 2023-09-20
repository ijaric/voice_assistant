import functools

import pydantic
import pydantic_settings


class DbSettings(pydantic_settings.BaseSettings):
    host: str = pydantic.Field("127.0.0.1", validation_alias="db_host")
    port: int = pydantic.Field(5432, validation_alias="db_port")
    user: str = pydantic.Field(..., validation_alias="db_user")
    password: str = pydantic.Field(..., validation_alias="db_password")
    name: str = pydantic.Field("db_name", validation_alias="db_name")


class ApiSettings(pydantic_settings.BaseSettings):
    host: str = pydantic.Field("0.0.0.0", validation_alias="server_host")
    port: int = pydantic.Field(8000, validation_alias="server_port")


class Settings(pydantic_settings.BaseSettings):
    debug: str = pydantic.Field("false", validation_alias="debug")
    db: DbSettings = pydantic.Field(default_factory=lambda: DbSettings())
    api: ApiSettings = pydantic.Field(default_factory=lambda: ApiSettings())

    jwt_secret_key: str = pydantic.Field(..., validation_alias="jwt_secret_key")

    @pydantic.field_validator("debug")
    @classmethod
    def validate_debug(cls, v: str) -> bool:
        return v.lower() == "true"


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
