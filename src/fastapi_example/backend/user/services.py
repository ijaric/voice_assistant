import typing

import backend.user.models as models


class UserClientProtocol(typing.Protocol):
    def get_name(self) -> str:
        ...


class UserService:
    def __init__(self, user_client: UserClientProtocol):
        self._user_client = user_client

    def get_one(self, entity_id: int) -> models.User:
        return models.User(id=entity_id, name=self._user_client.get_name())
