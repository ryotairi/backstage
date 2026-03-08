from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from .config import config
from .utils.crypt import encrypt
from .middlewares.api_logger import ApiLoggerMiddleware


def create_version_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)

    app.add_middleware(ApiLoggerMiddleware)

    @app.get("/{appVersion}/{appHash}")
    async def get_version(appVersion: str, appHash: str):
        key = f"{appVersion}/{appHash}"
        version_data = config.versionData.get(key)
        if version_data:
            data = version_data.model_dump()
        else:
            data = {}
        return Response(
            content=encrypt(data),
            media_type="application/octet-stream",
        )

    return app
