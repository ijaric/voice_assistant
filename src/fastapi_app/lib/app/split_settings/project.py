import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class ProjectSettings(pydantic_settings.BaseSettings):
    """Project settings."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug: str = "false"
    jwt_secret_key: str = pydantic.Field(default=..., validation_alias="jwt_secret_key")
    jwt_algorithm: str = "HS256"

    @pydantic.field_validator("debug")
    def validate_debug(cls, v: str) -> bool:
        return v.lower() == "true"
