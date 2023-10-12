import uuid

import pydantic


class RequestLastSessionId(pydantic.BaseModel):
    """Request for a new session ID."""

    channel: str
    user_id: str
    minutes_ago: int


class RequestChatMessage(pydantic.BaseModel):
    """A chat message."""

    session_id: uuid.UUID
    user_id: str
    channel: str
    message: dict[str, str]


class RequestChatHistory(pydantic.BaseModel):
    """Request for chat history."""

    session_id: uuid.UUID


class Message(pydantic.BaseModel):
    """A chat message."""

    role: str
    content: str
