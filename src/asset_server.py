import json
import os
from datetime import datetime

import httpx
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, FileResponse

from .config import config
from .utils.crypt import encrypt
from .utils.asset_domain import match_asset_domain
from .middlewares.api_logger import ApiLoggerMiddleware
from .services.logger import logger

_android_data = None


def _get_android_data():
    global _android_data
    if _android_data is None:
        with open("assets/android.json", "r") as f:
            _android_data = json.load(f)
    return _android_data


def create_asset_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)

    app.add_middleware(ApiLoggerMiddleware)

    @app.get("/api/version/{version}/os/{platform}")
    async def get_asset_version(request: Request, version: str, platform: str):
        hostname = request.headers.get("host", "").split(":")[0]
        match = match_asset_domain(hostname)

        if not match or match.type != "assetbundleInfoUrl" or platform != "android":
            return Response(
                content=encrypt({
                    "httpStatus": 404,
                    "errorCode": "not_found",
                    "errorMessage": "",
                }),
                status_code=404,
                media_type="application/octet-stream",
            )

        return Response(
            content=encrypt(_get_android_data()),
            media_type="application/octet-stream",
        )

    @app.get("/{version}/{hash}/{platform}/{assetPath:path}")
    async def get_asset(request: Request, version: str, hash: str, platform: str, assetPath: str):
        hostname = request.headers.get("host", "").split(":")[0]
        match = match_asset_domain(hostname)

        latest = config.versions[config.latestVersion]
        if (
            not match
            or match.type != "assetbundleUrl"
            or platform != "android"
            or version != latest.assetVersion
        ):
            return Response(
                content=encrypt({
                    "httpStatus": 404,
                    "errorCode": "not_found",
                    "errorMessage": "",
                }),
                status_code=404,
                media_type="application/octet-stream",
            )

        local_path = f"assets/{assetPath}"
        if not os.path.exists(local_path):
            try:
                now = datetime.now()
                t = f"{now.year}{now.month:02d}{now.day}{now.hour}{now.minute}{now.second}"
                url = f"{config.upstreamAssetUrl}/{platform}/{assetPath}?t={t}"

                async with httpx.AsyncClient() as client:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        raise Exception(f"{resp.status_code}: {resp.text}")

                    # Ensure directory exists
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(resp.content)

                logger.info(f"Successfully downloaded: {assetPath}")
            except Exception as e:
                logger.error(f"Failed to download {assetPath}: {e}")

        if os.path.exists(local_path):
            return FileResponse(os.path.realpath(local_path))
        else:
            return Response(
                content=encrypt({
                    "httpStatus": 404,
                    "errorCode": "not_found",
                    "errorMessage": "",
                }),
                status_code=404,
                media_type="application/octet-stream",
            )

    return app
