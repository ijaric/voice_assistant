import pydantic_settings

import lib.app.split_settings as app_split_settings


class Settings(pydantic_settings.BaseSettings):
    agent: app_split_settings.AgentSettings = app_split_settings.AgentSettings()
    api: app_split_settings.ApiSettings = app_split_settings.ApiSettings()
    app: app_split_settings.AppSettings = app_split_settings.AppSettings()
    postgres: app_split_settings.PostgresSettings = app_split_settings.PostgresSettings()
    logger: app_split_settings.LoggingSettings = app_split_settings.LoggingSettings()
    openai: app_split_settings.OpenaiSettings = app_split_settings.OpenaiSettings()
    project: app_split_settings.ProjectSettings = app_split_settings.ProjectSettings()
    proxy: app_split_settings.ProxySettings = app_split_settings.ProxySettings()
    voice: app_split_settings.VoiceSettings = app_split_settings.VoiceSettings()
    tts_yandex: app_split_settings.TTSYandexSettings = app_split_settings.TTSYandexSettings()
    tts_eleven_labs: app_split_settings.TTSElevenLabsSettings = app_split_settings.TTSElevenLabsSettings()
