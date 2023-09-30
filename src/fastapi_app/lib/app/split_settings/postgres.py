import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class PostgresSettings(pydantic_settings.BaseSettings):
    """Postgres settings."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="POSTGRES_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Connection settings
    driver: str = "postgresql+asyncpg"
    db_name: str = "database_name"
    host: str = "localhost"
    port: int = 5432
    user: str = "app"
    password: pydantic.SecretStr = pydantic.Field(
        default=..., validation_alias=pydantic.AliasChoices("password", "postgres_password")
    )

    # Engine settings
    pool_size: int = 50
    pool_pre_ping: bool = True
    echo: bool = False

    # Session settings
    auto_commit: bool = False
    auto_flush: bool = False
    expire_on_commit: bool = False

    @property
    def dsn(self) -> str:
        password = self.password.get_secret_value()
        return f"{self.driver}://{self.user}:{password}@{self.host}:{self.port}"

    @property
    def dsn_as_safe_url(self) -> str:
        return f"{self.driver}://{self.user}:***@{self.host}:{self.port}"
