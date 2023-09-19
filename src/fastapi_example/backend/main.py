import logging

import backend.user.handlers as user_handlers
import backend.user.repositories as user_repositories
import backend.user.services as user_services
import faker

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self._faker_client = faker.Faker()
        self._user_faker_client2 = user_repositories.UserFakerClient2(
            self._faker_client
        )
        self._user_service = user_services.UserService(self._user_faker_client2)

        self._handler1 = user_handlers.UserHandler1(self._user_service)
        self._handler2 = user_handlers.UserHandler2(self._user_service)
        logging.basicConfig(level=logging.INFO)

    def run(self):
        logger.info(self._handler1.get_one())
        logger.info(self._handler2.get_one())

    def close(self):
        logger.info("Closing app...")
        del self._faker_client


if __name__ == "__main__":
    app = App()
    try:
        app.run()
    finally:
        app.close()
