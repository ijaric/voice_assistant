import http
import io

import fastapi

import lib.stt.services as stt_services

import lib.tts.services as tts_service
import lib.models as models


class VoiceResponseHandler:
    def __init__(
        self,
        stt: stt_services.SpeechService,
        tts: tts_service.TTSService,
    ):
        self.stt = stt
        self.tts = tts
        self.router = fastapi.APIRouter()
        self.router.add_api_route(
            "/",
            self.voice_response,
            methods=["POST"],
            summary="Ответ голосового помощника",
            description="Маршрут возвращает потоковый ответ аудио",
        )

    async def voice_response(
        self,
        voice: bytes = fastapi.File(...),
    ) -> fastapi.responses.StreamingResponse:
        voice_text: str = await self.stt.recognize(voice)
        if voice_text == "":
            raise fastapi.HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Speech recognition failed")
        # TODO: Добавить обработку текста через клиента openai
        # TODO: Добавить синтез речи через клиента tts
        # TODO: Заменить заглушку на реальный ответ
        response = await self.tts.get_audio_as_bytes(
            models.TTSCreateRequestModel(
                text=voice_text,
            )
        )
        return fastapi.responses.StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/ogg")
        # return fastapi.responses.StreamingResponse(io.BytesIO(voice), media_type="audio/ogg")
