import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class DBSettings(pydantic_settings.BaseSettings):
    """Parent DB Settings Class."""

    # Connection settings
    protocol: str
    name: str
    host: str
    port: int
    user: str
    password: pydantic.SecretStr

    # Enginge settings
    pool_size: int = 10
    pool_pre_ping: bool = True
    echo: bool = False

    # Session settings
    auto_commit: bool = False
    auto_flush: bool = False
    expire_on_commit: bool = False

    @property
    def dsn(self) -> str:
        password = self.password.get_secret_value() if isinstance(self.password, pydantic.SecretStr) else self.password
        return f"{self.protocol}://{self.user}:{password}@{self.host}:{self.port}"

    @property
    def dsn_as_safe_url(self) -> str:
        return f"{self.protocol}://{self.user}:***@{self.host}:{self.port}"


class PostgresSettings(DBSettings):
    """Postgres settings."""

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
