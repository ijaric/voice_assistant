import pydantic

import lib.models.tts.voice as models_tts_voice
import lib.models.tts.voice.languages as models_tts_languages

AVAILABLE_MODELS_TYPE = models_tts_voice.YandexVoiceModel | models_tts_voice.ElevenLabsVoiceModel
LIST_VOICE_MODELS_TYPE = models_tts_voice.YandexListVoiceModelsModel | models_tts_voice.ElevenLabsListVoiceModelsModel


class TTSCreateRequestModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    voice_model: AVAILABLE_MODELS_TYPE
    text: str


class TTSCreateResponseModel(pydantic.BaseModel):
    audio_content: bytes


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
