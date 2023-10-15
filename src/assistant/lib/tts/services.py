import lib.models as _models
import lib.tts.models as tts_models


class TTSService:
    def __init__(
        self,
        repositories: dict[_models.VoiceModelProvidersEnum, tts_models.TTSRepositoryProtocol],
    ):
        self.repositories = repositories

    async def get_audio_as_bytes(self, request: _models.TTSCreateRequestModel) -> _models.TTSCreateResponseModel:
        model = request.voice_model
        repository = self.repositories[model.provider]
        audio_response = await repository.get_audio_as_bytes(request)
        return audio_response

    async def get_voice_model_by_name(self, voice_model_name: str) -> _models.BaseVoiceModel | None:
        for repository in self.repositories.values():
            voice_model = await repository.get_voice_model_by_name(voice_model_name)
            if voice_model:
                return voice_model
        raise ValueError("Voice model not found")

    async def get_list_voice_models_by_fields(
        self, fields: _models.TTSSearchVoiceRequestModel
    ) -> list[_models.AVAILABLE_MODELS_TYPE]:
        response_models: list[_models.AVAILABLE_MODELS_TYPE] = []
        for repository in self.repositories.values():
            voice_models = await repository.get_voice_models_by_fields(fields)
            if voice_models.models:
                response_models.extend(voice_models.models)
        return response_models

    async def get_all_models(self) -> list[_models.AVAILABLE_MODELS_TYPE]:
        response_models: list[_models.AVAILABLE_MODELS_TYPE] = []
        for repository in self.repositories.values():
            response = await repository.voice_models
            for model in response.models:
                model.languages = [  # type: ignore
                    _models.BaseLanguageCodesEnum[language.name] for language in model.languages
                ]
                response_models.append(model)
        return response_models
