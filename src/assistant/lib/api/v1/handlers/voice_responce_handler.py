import http
import io

import fastapi

import lib.stt.services as stt_services


class VoiceResponseHandler:
    def __init__(
        self,
        stt: stt_services.SpeechService,
    ):
        self.stt = stt
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
        return fastapi.responses.StreamingResponse(io.BytesIO(voice), media_type="audio/ogg")
