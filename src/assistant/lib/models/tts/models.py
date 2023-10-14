import pydantic

import lib.models.tts.voice as models_tts_voice
import lib.models.tts.voice.languages as models_tts_languages

AVAILABLE_MODELS_TYPE = models_tts_voice.YandexVoiceModel | models_tts_voice.ElevenLabsVoiceModel
LIST_VOICE_MODELS_TYPE = models_tts_voice.YandexListVoiceModelsModel | models_tts_voice.ElevenLabsListVoiceModelsModel
DEFAULT_MODEL = models_tts_voice.ElevenLabsVoiceModel(
    voice_id="eleven_multilingual_v2",
    languages=[
        models_tts_languages.ElevenLabsLanguageCodesEnum.ENGLISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.JAPANESE,
        models_tts_languages.ElevenLabsLanguageCodesEnum.CHINESE,
        models_tts_languages.ElevenLabsLanguageCodesEnum.GERMAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.HINDI,
        models_tts_languages.ElevenLabsLanguageCodesEnum.FRENCH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.KOREAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.PORTUGUESE,
        models_tts_languages.ElevenLabsLanguageCodesEnum.ITALIAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.SPANISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.INDONESIAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.DUTCH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.TURKISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.FILIPINO,
        models_tts_languages.ElevenLabsLanguageCodesEnum.POLISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.SWEDISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.BULGARIAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.ROMANIAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.ARABIC,
        models_tts_languages.ElevenLabsLanguageCodesEnum.CZECH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.GREEK,
        models_tts_languages.ElevenLabsLanguageCodesEnum.FINNISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.CROATIAN,
        models_tts_languages.ElevenLabsLanguageCodesEnum.MALAY,
        models_tts_languages.ElevenLabsLanguageCodesEnum.SLOVAK,
        models_tts_languages.ElevenLabsLanguageCodesEnum.DANISH,
        models_tts_languages.ElevenLabsLanguageCodesEnum.TAMIL,
        models_tts_languages.ElevenLabsLanguageCodesEnum.UKRAINIAN,
    ],
)


class TTSCreateRequestModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    voice_model: AVAILABLE_MODELS_TYPE = DEFAULT_MODEL
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
