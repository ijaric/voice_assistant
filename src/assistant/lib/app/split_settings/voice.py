import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class VoiceSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="VOICE_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    max_input_seconds: int = 30
    max_input_size: int = 5120  # 5MB
    available_formats: str = "wav,mp3,ogg"

    @pydantic.field_validator("available_formats")
    def validate_available_formats(cls, v: str) -> list[str]:
        return v.split(",")
