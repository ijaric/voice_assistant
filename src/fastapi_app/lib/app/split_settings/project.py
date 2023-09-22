import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class ApiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="SERVER_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8000


class ProjectSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug: str = "false"
    jwt_secret_key: pydantic.SecretStr = pydantic.Field(default=..., validation_alias="jwt_secret_key")

    @pydantic.field_validator("debug")
    def validate_debug(cls, v: str) -> bool:
        return v.lower() == "true"