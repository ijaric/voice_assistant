import typing

import pydantic

import lib.models as models


class ElevenLabsVoiceModel(models.BaseVoiceModel):
    voice_id: str
    voice_name: str | None = None
    languages: list[models.LANGUAGE_CODES_ENUM_TYPE]
    company_name: str = "eleven labs"


class ElevenLabsListVoiceModelsModel(pydantic.BaseModel):
    models: list[ElevenLabsVoiceModel] = [
        ElevenLabsVoiceModel(
            voice_id="eleven_multilingual_v1",
            languages=[
                models.ElevenLabsLanguageCodesEnum.ENGLISH,
                models.ElevenLabsLanguageCodesEnum.GERMAN,
                models.ElevenLabsLanguageCodesEnum.POLISH,
                models.ElevenLabsLanguageCodesEnum.SPANISH,
                models.ElevenLabsLanguageCodesEnum.ITALIAN,
                models.ElevenLabsLanguageCodesEnum.FRENCH,
                models.ElevenLabsLanguageCodesEnum.PORTUGUESE,
                models.ElevenLabsLanguageCodesEnum.HINDI,
                models.ElevenLabsLanguageCodesEnum.ARABIC,
            ],
        ),
        ElevenLabsVoiceModel(
            voice_id="eleven_multilingual_v2",
            languages=[
                models.ElevenLabsLanguageCodesEnum.ENGLISH,
                models.ElevenLabsLanguageCodesEnum.JAPANESE,
                models.ElevenLabsLanguageCodesEnum.CHINESE,
                models.ElevenLabsLanguageCodesEnum.GERMAN,
                models.ElevenLabsLanguageCodesEnum.HINDI,
                models.ElevenLabsLanguageCodesEnum.FRENCH,
                models.ElevenLabsLanguageCodesEnum.KOREAN,
                models.ElevenLabsLanguageCodesEnum.PORTUGUESE,
                models.ElevenLabsLanguageCodesEnum.ITALIAN,
                models.ElevenLabsLanguageCodesEnum.SPANISH,
                models.ElevenLabsLanguageCodesEnum.INDONESIAN,
                models.ElevenLabsLanguageCodesEnum.DUTCH,
                models.ElevenLabsLanguageCodesEnum.TURKISH,
                models.ElevenLabsLanguageCodesEnum.FILIPINO,
                models.ElevenLabsLanguageCodesEnum.POLISH,
                models.ElevenLabsLanguageCodesEnum.SWEDISH,
                models.ElevenLabsLanguageCodesEnum.BULGARIAN,
                models.ElevenLabsLanguageCodesEnum.ROMANIAN,
                models.ElevenLabsLanguageCodesEnum.ARABIC,
                models.ElevenLabsLanguageCodesEnum.CZECH,
                models.ElevenLabsLanguageCodesEnum.GREEK,
                models.ElevenLabsLanguageCodesEnum.FINNISH,
                models.ElevenLabsLanguageCodesEnum.CROATIAN,
                models.ElevenLabsLanguageCodesEnum.MALAY,
                models.ElevenLabsLanguageCodesEnum.SLOVAK,
                models.ElevenLabsLanguageCodesEnum.DANISH,
                models.ElevenLabsLanguageCodesEnum.TAMIL,
                models.ElevenLabsLanguageCodesEnum.UKRAINIAN,
            ],
        ),
        ElevenLabsVoiceModel(
            voice_id="eleven_multilingual_v2",
            languages=[models.ElevenLabsLanguageCodesEnum.ENGLISH],
        ),
    ]

    @classmethod
    def from_api(cls, voice_models_from_api: list[dict[str, typing.Any]]) -> typing.Self:
        voice_models = [ElevenLabsVoiceModel.model_validate(voice_model) for voice_model in voice_models_from_api]
        return ElevenLabsListVoiceModelsModel(models=voice_models)
