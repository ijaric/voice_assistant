import logging

import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.ext.asyncio as sa_asyncio

import lib.agent.repositories as repositories
import lib.models as models
import lib.orm_models as orm_models


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

    async def get_movie_by_description(self, description: str) -> list[models.Movie] | None:
        """Use this function to find data about a movie by movie's description."""

        self.logger.info("Request to get movie by description: %s", description)
        embedded_description = await self.repository.aget_embedding(description)
        try:
            async with self.pg_async_session() as session:
                result: list[models.Movie] = []
                stmt = (
                    sa.select(orm_models.FilmWork)
                    .order_by(orm_models.FilmWork.embeddings.cosine_distance(embedded_description.root))
                    .limit(5)
                )
                response = await session.execute(stmt)
                neighbours = response.scalars()
                for neighbour in neighbours:
                    result.append(models.Movie(**neighbour.__dict__))
                return result
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)
