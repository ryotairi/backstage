from starlette.requests import Request
from starlette.responses import Response
from ..utils.crypt import encrypt
from ..config import config


async def get_informations_route(request: Request) -> Response:
    return Response(
        content=encrypt({
            "informations": [info.model_dump() for info in config.informations],
        }),
        media_type="application/octet-stream",
    )
