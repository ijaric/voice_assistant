import pydantic
import pydantic_settings

import tests.core.split_settings as app_split_settings


class TestsSettings(pydantic_settings.BaseSettings):
    api: app_split_settings.ApiSettings = pydantic.Field(default_factory=lambda: app_split_settings.ApiSettings())
    postgres: app_split_settings.PostgresSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.PostgresSettings()
    )
    project: app_split_settings.ProjectSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.ProjectSettings()
    )


tests_settings = TestsSettings()
