import time
from starlette.requests import Request
from starlette.responses import Response
from ..utils.crypt import encrypt
from ..config import config


async def get_system_route(request: Request) -> Response:
    return Response(
        content=encrypt({
            "serverDate": int(time.time() * 1000),
            "timezone": "UTC",
            "profile": "production",
            "maintenanceStatus": config.maintenanceStatus,
            "appVersions": [v.model_dump() for v in config.versions],
        }),
        media_type="application/octet-stream",
    )
