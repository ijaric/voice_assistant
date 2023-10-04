import pydantic

import lib.tts.models.voice as tts_models_voice


class TTSRequestModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    voice_model_name: tts_models_voice.YandexVoiceModelNamesString
    audio_content: bytes


class TTSResponseModel(pydantic.BaseModel):
    audio_content: bytes
