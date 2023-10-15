import http
import io

import fastapi

import lib.agent.services as agent_service
import lib.models as models
import lib.stt.services as stt_services
import lib.tts.services as tts_service


class VoiceResponseHandler:
    def __init__(
        self,
        stt: stt_services.SpeechService,
        tts: tts_service.TTSService,
        agent: agent_service.AgentService,
    ):
        self.stt = stt
        self.tts = tts
        self.agent = agent
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
        channel: str="tg",
        user_id: str="1234",
        voice: bytes = fastapi.File(...),
    ) -> fastapi.responses.StreamingResponse:
        voice_text: str = await self.stt.recognize(voice)
        if voice_text == "":
            raise fastapi.HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Speech recognition failed")

        agent_request = models.AgentCreateRequestModel(channel=channel, user_id=user_id, text=voice_text)
        reply_text = await self.agent.process_request(agent_request)

        response = await self.tts.get_audio_as_bytes(
            models.TTSCreateRequestModel(
                text=reply_text.text,
            )
        )
        return fastapi.responses.StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/ogg")
        # return fastapi.responses.StreamingResponse(io.BytesIO(voice), media_type="audio/ogg")
