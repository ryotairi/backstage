import json
import os
from starlette.requests import Request
from starlette.responses import Response
from ..utils.crypt import encrypt


async def suite_master_file_route(request: Request, version: str, fileName: str) -> Response:
    if not fileName or not os.path.exists(f"suitemasterfile/{fileName}"):
        return Response(
            content=encrypt({"httpStatus": 404, "errorCode": "not_found", "errorMessage": ""}),
            status_code=404,
            media_type="application/octet-stream",
        )

    with open(f"suitemasterfile/{fileName}", "r") as f:
        data = json.load(f)

    return Response(
        content=encrypt(data),
        media_type="application/octet-stream",
    )
