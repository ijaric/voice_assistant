import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class OpenaiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="OPENAI_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: pydantic.SecretStr = pydantic.Field(
        default=..., validation_alias=pydantic.AliasChoices("api_key", "openai_api_key")
    )
    stt_model: str = "whisper-1"
    agent_temperature: float = 0.7
