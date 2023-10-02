import pydantic


class BrokerMessagePayload(pydantic.BaseModel):
    """
    Message payload.

    Attributes:
        message: Message text.
        direction: Message direction (Telegram, Mobile app, etc.).
        sender: Message sender (who should I send the answer to).
    """

    message: str
    direction: str
    sender: str


class BrokerMessage(pydantic.BaseModel):
    """
    Message.

    Attributes:
        payload: Message payload.
        queue: Queue name.
    """

    payload: BrokerMessagePayload
    queue: str
