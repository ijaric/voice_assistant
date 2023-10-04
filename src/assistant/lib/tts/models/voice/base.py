import enum

import pydantic


class LanguageCodes(enum.Enum):
    RUSSIAN = "ru-RU"
    ENGLISH = "en-US"
    KAZAKH = "kk-KK"
    GERMAN = "de-DE"
    HEBREW = "he-IL"
    UZBEK = "uz-UZ"


class VoiceModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    voice_name: str
    role: str | None = None
    lang: LanguageCodes
