import typing

import aiogram.dispatcher.middlewares as dispatcher_middlewares


class EnvironmentMiddleware(dispatcher_middlewares.LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs: typing.Any):
        super().__init__()
        self.kwargs = kwargs

    async def pre_process(self, obj: typing.Any, data: dict[typing.Any, typing.Any], *args: typing.Any):
        data.update(**self.kwargs)
