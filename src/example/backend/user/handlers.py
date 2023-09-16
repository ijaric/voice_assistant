import backend.user.services as user_services
import backend.utils.http as http_utils


class UserHandler1:
    def __init__(self, user_service: user_services.UserService):
        self._user_service = user_service

    def get_one(self) -> http_utils.Response:
        user = self._user_service.get_one(entity_id=1)
        return http_utils.get_response_from_dataclass(user)


class UserHandler2:
    def __init__(self, user_service: user_services.UserService):
        self._user_service = user_service

    def get_one(self) -> http_utils.Response:
        user = self._user_service.get_one(entity_id=2)
        return http_utils.get_response_from_dataclass(user)
