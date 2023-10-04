import enum

import lib.tts.models.voice.base as tts_models_voice_base


class YandexVoiceModelNamesString(enum.Enum):
    ERMIL_NEUTRAL = "ermil neutral"
    ERMIL_GOOD = "ermil good"
    ALENA_NEUTRAL = "alena neutral"
    ALENA_GOOD = "alena good"
    JANE_NEUTRAL = "jane neutral"
    JANE_GOOD = "jane good"
    JANE_EVIL = "jane evil"
    OMAZH_NEUTRAL = "omazh neutral"
    OMAZH_EVIL = "omazh evil"
    ZAHAR_NEUTRAL = "zahar neutral"
    ZAHAR_GOOD = "zahar good"
    FILIPP = "filipp"
    MADIRUS = "madirus"
    DASHA = "dasha"
    JULIA = "julia"
    LERA = "lera"
    MARINA = "marina"
    ALEXANDER = "alexander"
    KIRILL = "kirill"
    ANTON = "anton"
    # English
    JOHN = "john"
    # Kazakh
    AMIRA = "amira"
    MADI = "madi"
    # German
    LEA = "lea"
    # HEBREW
    NAOMI_MODERN = "naomi modern"
    NAOMI_CLASSIC = "naomi classic"
    # Uzbek
    NIGORA = "nigora"


class YandexVoiceModels(enum.Enum):
    # Russian
    ERMIL_NEUTRAL = tts_models_voice_base.VoiceModel(
        voice_name="ermil", role="neutral", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ERMIL_GOOD = tts_models_voice_base.VoiceModel(
        voice_name="ermil", role="good", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ALENA_NEUTRAL = tts_models_voice_base.VoiceModel(
        voice_name="alena", role="neutral", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ALENA_GOOD = tts_models_voice_base.VoiceModel(
        voice_name="alena", role="good", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    JANE_NEUTRAL = tts_models_voice_base.VoiceModel(
        voice_name="jane", role="neutral", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    JANE_GOOD = tts_models_voice_base.VoiceModel(
        voice_name="jane", role="good", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    JANE_EVIL = tts_models_voice_base.VoiceModel(
        voice_name="jane", role="evil", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    OMAZH_NEUTRAL = tts_models_voice_base.VoiceModel(
        voice_name="omazh", role="neutral", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    OMAZH_EVIL = tts_models_voice_base.VoiceModel(
        voice_name="omazh", role="evil", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ZAHAR_NEUTRAL = tts_models_voice_base.VoiceModel(
        voice_name="zahar", role="neutral", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ZAHAR_GOOD = tts_models_voice_base.VoiceModel(
        voice_name="zahar", role="good", lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    FILIPP = tts_models_voice_base.VoiceModel(
        voice_name="filipp", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    MADIRUS = tts_models_voice_base.VoiceModel(
        voice_name="madirus", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    DASHA = tts_models_voice_base.VoiceModel(
        voice_name="dasha", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    JULIA = tts_models_voice_base.VoiceModel(
        voice_name="julia", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    LERA = tts_models_voice_base.VoiceModel(
        voice_name="lera", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    MARINA = tts_models_voice_base.VoiceModel(
        voice_name="marina", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ALEXANDER = tts_models_voice_base.VoiceModel(
        voice_name="alexander", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    KIRILL = tts_models_voice_base.VoiceModel(
        voice_name="kirill", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    ANTON = tts_models_voice_base.VoiceModel(
        voice_name="anton", role=None, lang=tts_models_voice_base.LanguageCodes.RUSSIAN
    )
    # English
    JOHN = tts_models_voice_base.VoiceModel(
        voice_name="john", role=None, lang=tts_models_voice_base.LanguageCodes.ENGLISH
    )
    # Kazakh
    AMIRA = tts_models_voice_base.VoiceModel(
        voice_name="amira", role=None, lang=tts_models_voice_base.LanguageCodes.KAZAKH
    )
    MADI = tts_models_voice_base.VoiceModel(
        voice_name="madi", role=None, lang=tts_models_voice_base.LanguageCodes.KAZAKH
    )
    # German
    LEA = tts_models_voice_base.VoiceModel(voice_name="lea", role=None, lang=tts_models_voice_base.LanguageCodes.GERMAN)
    # HEBREW
    NAOMI_MODERN = tts_models_voice_base.VoiceModel(
        voice_name="naomi", role="modern", lang=tts_models_voice_base.LanguageCodes.HEBREW
    )
    NAOMI_CLASSIC = tts_models_voice_base.VoiceModel(
        voice_name="naomi", role="classic", lang=tts_models_voice_base.LanguageCodes.HEBREW
    )
    # Uzbek
    NIGORA = tts_models_voice_base.VoiceModel(
        voice_name="nigora", role=None, lang=tts_models_voice_base.LanguageCodes.UZBEK
    )
