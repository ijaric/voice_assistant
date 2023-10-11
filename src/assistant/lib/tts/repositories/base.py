import abc

import lib.models as models


class HttpClient:  # Mocked class todo remove and use real http client from lib.clients.http_client
    ...


class TTSBaseRepository(abc.ABC):
    def __init__(self, client: HttpClient, is_models_from_api: bool = False):
        self.http_client = client
        self.is_models_from_api = is_models_from_api

    @property
    @abc.abstractmethod
    def voice_models(self) -> models.LIST_VOICE_MODELS_TYPE:
        ...

    @abc.abstractmethod
    def get_audio_as_bytes(self, request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        raise NotImplementedError

    def get_voice_model_by_name(self, voice_model_name: str) -> models.BaseVoiceModel | None:
        """
        Search voice model by name
        :param voice_model_name: String name
        :return: Voice model that match the name
        """
        for voice_model in self.voice_models.models:
            if voice_model.voice_name == voice_model_name:
                return voice_model

    def get_list_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> list[models.AVAILABLE_MODELS_TYPE]:
        """
        Search voice model by fields
        :param fields: Any fields from TTSSearchVoiceRequestModel
        :return: All voice models that match the fields
        """
        fields_dump = fields.model_dump(exclude_none=True)
        voice_models_response = []
        for voice_model in self.voice_models.models:
            for field, field_value in fields_dump.items():
                if field == "languages":  # language is a list
                    language_names: set[str] = {item.name for item in field_value}
                    voice_model_language_names: set[str] = {item.name for item in voice_model.languages}
                    if language_names.issubset(voice_model_language_names):
                        continue
                    break
                voice_model_dump = voice_model.model_dump()
                if voice_model_dump[field] != field_value.name:
                    break
            else:
                voice_models_response.append(voice_model)
        return voice_models_response  # type: ignore[reportUnknownVariableType]
