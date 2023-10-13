import enum
import typing

import pydantic

import lib.models.tts.voice.languages as models_tts_languages


class VoiceModelProvidersEnum(enum.Enum):
    YANDEX = "yandex"
    ELEVEN_LABS = "eleven_labs"


class BaseVoiceModel(pydantic.BaseModel):
    voice_id: str
    voice_name: str | None = None
    languages: list[models_tts_languages.LANGUAGE_CODES_ENUM_TYPE]
    provider: VoiceModelProvidersEnum

    @pydantic.model_validator(mode="before")
    @classmethod
    def check_voice_name_exists(cls, data: typing.Any) -> typing.Any:
        if not data:
            return data
        voice_id = data.get("voice_id")
        voice_name = data.get("voice_name")
        if not voice_name and voice_id:
            data["voice_name"] = voice_id
        return data
