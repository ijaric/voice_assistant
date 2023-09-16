import faker


class UserFakerClient:
    def __init__(self, faker_client: faker.Faker):
        self._faker_client = faker_client

    def get_name(self) -> str:
        return self._faker_client.name()

    def get_email(self) -> str:
        return self._faker_client.email()


class UserFakerClient2:
    def __init__(self, faker_client: faker.Faker):
        self._faker_client = faker_client

    def get_name(self) -> str:
        return self._faker_client.full_name()

    def get_email(self) -> str:
        return self._faker_client.email()
