import typing

import lib.models as models
import lib.tts.models.utils as tts_models_utils


class TTSRepositoryProtocol(typing.Protocol):
    def get_audio_as_bytes_from_text(self, text: str) -> models.TTSCreateResponseModel:
        ...

    def get_voice_model_by_name(self, voice_model_name: str) -> models.BaseVoiceModel | None:
        ...

    def get_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> tts_models_utils.LIST_VOICE_MODELS_TYPE:
        ...
