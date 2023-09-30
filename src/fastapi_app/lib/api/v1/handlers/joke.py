import fastapi

import lib.api.v1.schemas as api_shemas
import lib.joke.services as services

joke_router = fastapi.APIRouter()


@joke_router.get(
    "/",
    response_model=api_shemas.JokeResponse,
    summary="Random joke",
    description="Return a random joke from a free API.",
)
async def get_joke(joke_service: services.JokeService):
    joke = await joke_service.get_joke()
    if joke:
        return api_shemas.JokeResponse(
            joke=f"{joke.setup}\n{joke.punchline}", id=joke.id_field, category=joke.type_field
        )

    return api_shemas.JokeResponse(joke="No joke for you!", id=0, category="No category")
