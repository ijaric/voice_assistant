import pydantic
import pydantic_settings

import tgbot.split_settings as app_split_settings


class Settings(pydantic_settings.BaseSettings):
    api: app_split_settings.ApiSettings = pydantic.Field(default_factory=app_split_settings.ApiSettings)
    tgbot: app_split_settings.TgBotSettings = pydantic.Field(default_factory=app_split_settings.TgBotSettings)
