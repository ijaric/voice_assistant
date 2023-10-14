import logging
import uuid

import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.ext.asyncio as sa_asyncio

import lib.models as models
import lib.orm_models as orm_models


class ChatHistoryRepository:
    def __init__(self, pg_async_session: sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession]) -> None:
        self.pg_async_session = pg_async_session
        self.logger = logging.getLogger(__name__)

    async def get_last_session_id(self, request: models.RequestLastSessionId) -> uuid.UUID | None:
        """Get a current session ID if exists."""

        self.logger.debug("get_last_session_id: %s", request)
        try:
            async with self.pg_async_session() as session:
                statement = (
                    sa.select(orm_models.ChatHistory)
                    .filter_by(channel=request.channel, user_id=request.user_id)
                    .filter(
                        (
                            sa.func.extract("epoch", sa.text("NOW()"))
                            - sa.func.extract("epoch", orm_models.ChatHistory.created)
                        )
                        / 60
                        <= request.minutes_ago
                    )
                    .order_by(orm_models.ChatHistory.created.desc())
                    .limit(1)
                )
                result = await session.execute(statement)

                chat_session = result.scalars().first()
                if chat_session:
                    return chat_session.session_id
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)

    async def get_messages_by_sid(self, request: models.RequestChatHistory) -> list[models.Message] | None:
        """Get all messages of a chat by session ID."""

        self.logger.debug("get_messages_by_sid: %s", request)
        try:
            async with self.pg_async_session() as session:
                messages: list[models.Message] = []
                statement = (
                    sa.select(orm_models.ChatHistory)
                    .filter_by(session_id=request.session_id)
                    .order_by(orm_models.ChatHistory.created.asc())
                )
                print("get_messages_by_sid:", statement)
                result = await session.execute(statement)
                for row in result.scalars().all():
                    # TODO: Было бы интересно понять почему pyright ругается ниже и как правильно вызывать компоненты
                    messages.append(models.Message(role=row.content["role"], content=row.content["content"]))  # type: ignore[reportGeneralTypeIssues]
                return messages
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)

    async def add_message(self, request: models.RequestChatMessage) -> None:
        """Add a message to the chat history."""

        self.logger.debug("add_message: %s", request)
        try:
            async with self.pg_async_session() as session:
                chat_history = orm_models.ChatHistory(
                    id=uuid.uuid4(),
                    session_id=request.session_id,
                    user_id=request.user_id,
                    channel=request.channel,
                    content=request.message,
                )
                session.add(chat_history)
                await session.commit()
                # TODO: Add refresh to session and return added object
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)
