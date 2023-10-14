import typing

import pydantic

import lib.models.tts.voice.base as models_tts_base
import lib.models.tts.voice.languages as models_tts_languages


class YandexVoiceModel(models_tts_base.BaseVoiceModel):
    voice_id: str
    voice_name: str | None = None
    languages: list[models_tts_languages.LANGUAGE_CODES_ENUM_TYPE]
    provider: models_tts_base.VoiceModelProvidersEnum = models_tts_base.VoiceModelProvidersEnum.YANDEX
    role: str | None = None

    @pydantic.model_validator(mode="before")
    @classmethod
    def check_voice_name_exists(cls, data: typing.Any) -> typing.Any:
        if not data:
            return data
        voice_id = data.get("voice_id")
        voice_name = data.get("voice_name")
        role = data.get("role")
        if not voice_name and voice_id:
            data["voice_name"] = f"{voice_id} {role}" if role else voice_id
        return data


class YandexListVoiceModelsModel(pydantic.BaseModel):
    models: list[YandexVoiceModel] = [
        YandexVoiceModel(
            voice_id="ermil", role="neutral", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="ermil", role="good", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="alena", role="neutral", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="alena", role="good", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="jane", role="neutral", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="jane", role="good", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="jane", role="evil", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="omazh", role="neutral", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="omazh", role="evil", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="zahar", role="neutral", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="zahar", role="good", languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="filipp", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="madirus", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(voice_id="dasha", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]),
        YandexVoiceModel(voice_id="julia", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]),
        YandexVoiceModel(voice_id="lera", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]),
        YandexVoiceModel(
            voice_id="marina", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="alexander", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(
            voice_id="kirill", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]
        ),
        YandexVoiceModel(voice_id="anton", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.RUSSIAN]),
        YandexVoiceModel(voice_id="john", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.ENGLISH]),
        YandexVoiceModel(voice_id="amira", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.KAZAKH]),
        YandexVoiceModel(voice_id="madi", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.KAZAKH]),
        YandexVoiceModel(voice_id="lea", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.GERMAN]),
        YandexVoiceModel(
            voice_id="naomi", role="modern", languages=[models_tts_languages.YandexLanguageCodesEnum.HEBREW]
        ),
        YandexVoiceModel(
            voice_id="naomi", role="classic", languages=[models_tts_languages.YandexLanguageCodesEnum.HEBREW]
        ),
        YandexVoiceModel(voice_id="nigora", role=None, languages=[models_tts_languages.YandexLanguageCodesEnum.UZBEK]),
    ]

    @classmethod
    def from_api(cls, voice_models_from_api: list[dict[str, typing.Any]]) -> typing.Self:
        voice_models = [YandexVoiceModel.model_validate(voice_model) for voice_model in voice_models_from_api]
        return YandexListVoiceModelsModel(models=voice_models)
