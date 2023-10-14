import typing

import pydantic

import lib.models.tts.voice.base as models_tts_base
import lib.models.tts.voice.languages as models_tts_languages


class ElevenLabsVoiceModel(models_tts_base.BaseVoiceModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)
    voice_id: str
    voice_name: str | None = None
    languages: list[models_tts_languages.LANGUAGE_CODES_ENUM_TYPE]
    provider: models_tts_base.VoiceModelProvidersEnum = models_tts_base.VoiceModelProvidersEnum.ELEVEN_LABS


class ElevenLabsListVoiceModelsModel(pydantic.BaseModel):
    models: list[ElevenLabsVoiceModel] = [
        ElevenLabsVoiceModel(
            voice_id="eleven_multilingual_v1",
            languages=[
                models_tts_languages.ElevenLabsLanguageCodesEnum.ENGLISH,
                models_tts_languages.ElevenLabsLanguageCodesEnum.GERMAN,
                models_tts_languages.ElevenLabsLanguageCodesEnum.POLISH,
                models_tts_languages.ElevenLabsLanguageCodesEnum.SPANISH,
                models_tts_languages.ElevenLabsLanguageCodesEnum.ITALIAN,
                models_tts_languages.ElevenLabsLanguageCodesEnum.FRENCH,
                models_tts_languages.ElevenLabsLanguageCodesEnum.PORTUGUESE,
                models_tts_languages.ElevenLabsLanguageCodesEnum.HINDI,
                models_tts_languages.ElevenLabsLanguageCodesEnum.ARABIC,
            ],
        ),
        ElevenLabsVoiceModel(
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
        ),
        ElevenLabsVoiceModel(
            voice_id="eleven_multilingual_v2",
            languages=[models_tts_languages.ElevenLabsLanguageCodesEnum.ENGLISH],
        ),
    ]

    @classmethod
    def from_api(cls, voice_models_from_api: list[dict[str, typing.Any]]) -> typing.Self:
        voice_models = [ElevenLabsVoiceModel.model_validate(voice_model) for voice_model in voice_models_from_api]
        return ElevenLabsListVoiceModelsModel(models=voice_models)
