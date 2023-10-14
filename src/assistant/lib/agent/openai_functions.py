import logging
import uuid

import langchain.agents
import orm_models
import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.ext.asyncio as sa_asyncio

import lib.agent.repositories as repositories
import lib.models as models


class OpenAIFunctions:
    """OpenAI Functions for langchain agents."""

    def __init__(
        self,
        repository: repositories.EmbeddingRepository,
        pg_async_session: sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession],
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.pg_async_session = pg_async_session
        self.repository = repository

    @langchain.agents.tool
    async def get_movie_by_description(self, description: str) -> list[models.Movie] | None:
        """Provide a movie data by description."""

        self.logger.info("Request to get movie by description: %s", description)
        embedded_description = await self.repository.aget_embedding(description)
        try:
            async with self.pg_async_session() as session:
                result: list[models.Movie] = []
                stmt = (
                    sa.select(orm_models.FilmWork)
                    .order_by(orm_models.FilmWork.embedding.cosine_distance(embedded_description))
                    .limit(5)
                )
                neighbours = session.scalars(stmt)
                for neighbour in await neighbours:
                    result.append(models.Movie(**neighbour.__dict__))
                return result
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)

    @langchain.agents.tool
    def get_movie_by_id(self, id: uuid.UUID) -> models.Movie | None:
        """Provide a movie data by movie id."""
        self.logger.info("Request to get movie by id: %s", id)
        return None

    @langchain.agents.tool
    def get_similar_movies(self, id: uuid.UUID) -> list[models.Movie] | None:
        """Provide similar movies for the given movie ID."""

        self.logger.info("Request to get movie by id: %s", id)
        return None
