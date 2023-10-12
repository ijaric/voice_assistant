import typing

import lib.models as models


class TTSRepositoryProtocol(typing.Protocol):
    def get_audio_as_bytes(self, request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        ...

    def get_voice_model_by_name(self, voice_model_name: str) -> models.BaseVoiceModel | None:
        ...

    def get_voice_models_by_fields(self, fields: models.TTSSearchVoiceRequestModel) -> models.LIST_VOICE_MODELS_TYPE:
        ...
