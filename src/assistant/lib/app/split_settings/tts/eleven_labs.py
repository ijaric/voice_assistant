import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class TTSElevenLabsSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="TTS_ELEVEN_LABS_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: pydantic.SecretStr = pydantic.Field(default=...)
    default_voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    base_url: str = "https://api.elevenlabs.io/v1/"
    timeout_seconds: int = 30

    @property
    def base_headers(self) -> dict[str, str]:
        return {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key.get_secret_value(),
        }
