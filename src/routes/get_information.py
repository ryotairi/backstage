from starlette.requests import Request
from starlette.responses import Response
import json
from ..utils.crypt import encrypt
from ..config import config

_reg_data = None

def _get_reg_data():
    global _reg_data
    if _reg_data is None:
        with open("./json/reg.json", "r") as f:
            _reg_data = json.load(f)
    return _reg_data

async def get_informations_route(request: Request) -> Response:
    reg_data = _get_reg_data()
    
    return Response(
        content=encrypt({
            "informations": [info.model_dump() for info in config.informations],
        }),
        media_type="application/octet-stream",
    )
