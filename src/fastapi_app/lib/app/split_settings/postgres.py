import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class PostgresSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="DB_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 5432
    user: str = "app"
    password: pydantic.SecretStr = pydantic.Field(
        default=..., validation_alias=pydantic.AliasChoices("password", "db_password")
    )
