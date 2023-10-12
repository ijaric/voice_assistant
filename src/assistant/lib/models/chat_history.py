import pydantic


class RequestLastSessionId(pydantic.BaseModel):
    """Request for a new session ID."""

    channel: str
    user_id: str
    minutes_ago: int
