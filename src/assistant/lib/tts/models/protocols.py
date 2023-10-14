import typing

import lib.models as models


class TTSRepositoryProtocol(typing.Protocol):
    async def get_audio_as_bytes(self, request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        ...

    async def get_voice_model_by_name(self, voice_model_name: str) -> models.BaseVoiceModel | None:
        ...

    async def get_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> models.LIST_VOICE_MODELS_TYPE:
        ...
