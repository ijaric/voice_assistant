import logging.config as logging_config

import pydantic
import pydantic_settings

import lib.app.split_settings as app_split_settings


class Settings(pydantic_settings.BaseSettings):
    api: app_split_settings.ApiSettings = pydantic.Field(default_factory=lambda: app_split_settings.ApiSettings())
    postgres: app_split_settings.PostgresSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.PostgresSettings()
    )
    logger: app_split_settings.LoggingSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.LoggingSettings()
    )
    project: app_split_settings.ProjectSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.ProjectSettings()
    )


settings = Settings()  # todo Вынести в инициализацию

logging_config.dictConfig(  # todo Вынести в инициализацию
    app_split_settings.get_logging_config(**settings.logger.model_dump())
)
