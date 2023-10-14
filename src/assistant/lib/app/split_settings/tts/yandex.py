import typing

import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class TTSYandexSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="TTS_YANDEX_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    audio_format: typing.Literal["oggopus", "mp3", "lpcm"] = "oggopus"
    sample_rate_hertz: int = 48000
    api_key: pydantic.SecretStr = pydantic.Field(default=...)
    base_url: str = "https://tts.api.cloud.yandex.net/speech/v1/"
    timeout_seconds: int = 30

    @property
    def base_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Api-Key {self.api_key.get_secret_value()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
