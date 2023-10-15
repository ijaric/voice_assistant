import uuid

import pydantic


class AgentCreateRequestModel(pydantic.BaseModel):
    text: str
    user_id: str
    channel: str


class AgentCreateResponseModel(pydantic.BaseModel):
    text: str
