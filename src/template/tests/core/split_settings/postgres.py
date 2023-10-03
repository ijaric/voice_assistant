import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class PostgresSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="POSTGRES_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    name: str = "test_database_name"
    host: str = "localhost"
    port: int = 5432
    user: str = "app"
    password: pydantic.SecretStr = pydantic.Field(
        default=...,
        validation_alias=pydantic.AliasChoices("password", "postgres_password"),
    )

    @property
    def db_uri_async(self) -> str:
        db_uri: str = "postgresql+asyncpg://{pg_user}:{pg_pass}@{pg_host}/{pg_dbname}".format(
            pg_user=self.user,
            pg_pass=self.password,
            pg_host=self.host,
            pg_dbname=self.name,
        )
        return db_uri

    @property
    def db_uri_sync(self) -> str:
        db_uri: str = "postgresql://{pg_user}:{pg_pass}@{pg_host}/{pg_dbname}".format(
            pg_user=self.user,
            pg_pass=self.password,
            pg_host=self.host,
            pg_dbname=self.name,
        )
        return db_uri
