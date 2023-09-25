import asyncio
import logging

import uvicorn

import lib.app.app as app_module
import lib.app.settings as app_settings

logger = logging.getLogger(__name__)


async def main():
    try:
        app_instance = app_module.Application()
        app = app_instance.create_app()
        settings = app_settings.get_settings()

        logger.info("Starting FastAPI application")

        config = uvicorn.Config(app=app, host=settings.api.host, port=settings.api.port, lifespan="on", reload=True)
        server = uvicorn.Server(config)

        await server.serve()

    except KeyboardInterrupt:
        logger.info("Exited with keyboard interruption")
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
