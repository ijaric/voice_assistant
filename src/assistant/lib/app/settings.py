import pydantic
import pydantic_settings

import lib.app.split_settings as app_split_settings


class Settings(pydantic_settings.BaseSettings):
    api: app_split_settings.ApiSettings = pydantic.Field(default_factory=lambda: app_split_settings.ApiSettings())
    app: app_split_settings.AppSettings = pydantic.Field(default_factory=lambda: app_split_settings.AppSettings())
    postgres: app_split_settings.PostgresSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.PostgresSettings()
    )
    logger: app_split_settings.LoggingSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.LoggingSettings()
    )
    openai: app_split_settings.OpenaiSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.OpenaiSettings()
    )
    project: app_split_settings.ProjectSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.ProjectSettings()
    )

    proxy: app_split_settings.ProxySettings = pydantic.Field(default_factory=lambda: app_split_settings.ProxySettings())
    voice: app_split_settings.VoiceSettings = pydantic.Field(default_factory=lambda: app_split_settings.VoiceSettings())
    tts_yandex: app_split_settings.TTSYandexSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.TTSYandexSettings()
    )
    tts_eleven_labs: app_split_settings.TTSElevenLabsSettings = pydantic.Field(
        default_factory=lambda: app_split_settings.TTSElevenLabsSettings()
    )
