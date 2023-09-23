import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class DBSettings(pydantic_settings.BaseSettings):
    """Abstract class for database settings."""

    protocol: str
    name: str
    host: str
    port: int
    user: str
    password: pydantic.SecretStr

    @property
    def dsn(self) -> str:
        """Get database DSN."""
        return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class PostgresSettings(DBSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="POSTGRES_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    protocol: str = "postgresql+asyncpg"
    name: str = "database_name"
    host: str = "localhost"
    port: int = 5432
    user: str = "app"
    password: pydantic.SecretStr = pydantic.Field(
        default=..., validation_alias=pydantic.AliasChoices("password", "postgres_password")
    )
