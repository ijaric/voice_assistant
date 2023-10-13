import pydantic
import pydantic_settings

import tgbot.split_settings.utils as split_settings_utils


class TgBotSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=split_settings_utils.ENV_PATH,
        env_prefix="BOT_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    token: pydantic.SecretStr = pydantic.Field(
        default=..., validation_alias=pydantic.AliasChoices("token", "bot_token")
    )
    admins: str = pydantic.Field(default="")

    @pydantic.field_validator("admins")
    def validate_bot_admins(cls, v: str) -> list[int]:
        return list(map(int, v.split(",")))
