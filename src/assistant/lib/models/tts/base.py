import typing

import pydantic

import lib.models.tts.languages as models_tts_languages


class TTSCreateRequestModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    voice_model_name: str
    text: str


class TTSCreateResponseModel(pydantic.BaseModel):
    audio_content: bytes


class BaseVoiceModel(pydantic.BaseModel):
    voice_id: str
    voice_name: str | None = None
    languages: list[models_tts_languages.LANGUAGE_CODES_ENUM_TYPE]
    company_name: str

    @pydantic.model_validator(mode="before")
    @classmethod
    def check_voice_name_exists(cls, data: typing.Any) -> typing.Any:
        voice_id = data.get("voice_id")
        voice_name = data.get("voice_name")
        if not voice_name and voice_id:
            data["voice_name"] = voice_id
        return data


class TTSSearchVoiceRequestModel(pydantic.BaseModel):
    voice_id: str | None = None
    voice_name: str | None = None
    languages: list[models_tts_languages.LANGUAGE_CODES_ENUM_TYPE] | None = None
    company_name: str | None = None

    @pydantic.model_validator(mode="after")
    def check_at_least_one_field(self):
        if not any((self.voice_name, self.languages, self.company_name)):
            raise ValueError("At least one field required")
        return self
