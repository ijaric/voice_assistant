import logging

import uvicorn

import lib.app.app as app_module
from lib.app import settings as app_settings

logger = logging.getLogger(__name__)


app_instance = app_module.Application()
app = app_instance.create_app()
settings = app_settings.get_settings()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
