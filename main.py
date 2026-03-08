#!/usr/bin/env python3
"""
libresekai - Python implementation
Runs all four servers (API, Web, Version, Assets) concurrently.
"""

import asyncio
import os
import uvicorn

from tortoise import Tortoise

from src.config import config
from src.services.logger import logger
from src.api_server import create_api_app
from src.web_server import create_web_app
from src.version_server import create_version_app
from src.asset_server import create_asset_app

DATABASE_URL = config.databaseUrl or os.environ.get("DATABASE_URL", "")

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["src.models"],
            "default_connection": "default",
        },
    },
}

async def run_server(app, host: str, port: int, name: str):
    """Run a uvicorn server for the given app."""
    config_uv = uvicorn.Config(app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config_uv)
    logger.info(f"{name} server listening on port {port}")
    await server.serve()

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    logger.info("Database initialised")

async def main():
    await init_db()
    
    api_app = create_api_app()
    web_app = create_web_app()
    version_app = create_version_app()
    asset_app = create_asset_app()

    await asyncio.gather(
        run_server(api_app, "::", config.apiPort, "API"),
        run_server(web_app, "::", config.webPort, "Web"),
        run_server(version_app, "::", config.versionPort, "Version"),
        run_server(asset_app, "::", config.assetsPort, "Assets"),
    )


if __name__ == "__main__":
    asyncio.run(main())
