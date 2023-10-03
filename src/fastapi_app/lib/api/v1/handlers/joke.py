import fastapi

import lib.api.v1.schemas as api_shemas
import lib.joke.services as joke_services


class JokeHandler:
    def __init__(self, joke_service: joke_services.JokeService):
        self.joke_service = joke_service
        self.router = fastapi.APIRouter()
        self.router.add_api_route(
            "/",
            self.get_joke,
            methods=["GET"],
            summary="Статус работоспособности",
            description="Проверяет доступность сервиса FastAPI.",
        )

    async def get_joke(self):
        joke = await self.joke_service.get_joke()
        if joke:
            return api_shemas.JokeResponse(
                joke=f"{joke.setup}\n{joke.punchline}", id=joke.id_field, category=joke.type_field
            )
        return api_shemas.JokeResponse(joke="No joke for you!", id=0, category="No category")
