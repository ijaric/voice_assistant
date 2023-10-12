import fastapi

import lib.agent as agent
import lib.models as models


class AgentHandler:
    def __init__(self, chat_history_repository: agent.ChatHistoryRepository):
        self.chat_history_repository = chat_history_repository
        self.router = fastapi.APIRouter()
        self.router.add_api_route(
            "/",
            self.get_agent,
            methods=["GET"],
            summary="Статус работоспособности",
            description="Проверяет доступность сервиса FastAPI.",
        )

    async def get_agent(self):
        request = models.RequestLastSessionId(channel="test", user_id="test", minutes_ago=3)
        response = await self.chat_history_repository.get_last_session_id(request=request)
        print("RESPONSE: ", response)
        return {"response": response}
