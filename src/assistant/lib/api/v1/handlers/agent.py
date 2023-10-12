import uuid

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
        self.router.add_api_route(
            "/add",
            self.add_message,
            methods=["GET"],
            summary="Статус работоспособности",
            description="Проверяет доступность сервиса FastAPI.",
        )
        self.router.add_api_route(
            "/messages",
            self.get_messages,
            methods=["GET"],
            summary="Статус работоспособности",
            description="Проверяет доступность сервиса FastAPI.",
        )

    async def get_agent(self):
        request = models.RequestLastSessionId(channel="test", user_id="user_id_1", minutes_ago=3)
        response = await self.chat_history_repository.get_last_session_id(request=request)
        print("RESPONSE: ", response)
        return {"response": response}

    async def add_message(self):
        sid: uuid.UUID = uuid.UUID("0cd3c882-affd-4929-aff1-e1724f5b54f2")
        import faker

        fake = faker.Faker()

        message = models.RequestChatMessage(
            session_id=sid, user_id="user_id_1", channel="test", message={"role": "system", "content": fake.sentence()}
        )
        await self.chat_history_repository.add_message(request=message)
        return {"response": "ok"}

    async def get_messages(self):
        sid: uuid.UUID = uuid.UUID("0cd3c882-affd-4929-aff1-e1724f5b54f2")

        request = models.RequestChatHistory(session_id=sid)
        response = await self.chat_history_repository.get_messages_by_sid(request=request)
        print("RESPONSE: ", response)
        return {"response": response}
