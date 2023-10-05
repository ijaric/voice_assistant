import typing

import pydantic

import lib.app.split_settings as app_split_settings


class SttVoice(pydantic.BaseModel):
    audio_size: int
    audio_format: str
    audio_name: str = "123"
    audio_data: bytes
    voice_settings: app_split_settings.VoiceSettings

    @pydantic.model_validator(mode="before")
    @classmethod
    def validate_audio(cls, v: dict[str, typing.Any]) -> dict[str, typing.Any]:
        settings: app_split_settings.VoiceSettings = v["voice_settings"]
        if v["audio_size"] > settings.max_input_size:
            raise ValueError(f"Audio size is too big: {v['audio_size']}")
        if v["audio_format"] not in settings.available_formats:
            raise ValueError(f"Audio format is not supported: {v['audio_format']}")
        if "audio_name" not in v or not v["audio_name"]:
            v["audio_name"] = f"audio.{v['audio_format']}"
        return v
