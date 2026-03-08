import json
import re
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import config

_agegate_data = None


def _get_agegate():
    global _agegate_data
    if _agegate_data is None:
        with open("./json/agegate.json", "r") as f:
            _agegate_data = json.load(f)
    return _agegate_data


def create_web_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.get("/json/legals_version.json")
    async def legals_version():
        return JSONResponse({"L": 1, "C": 2})

    @app.get("/json/agegate.json")
    async def agegate():
        return JSONResponse(_get_agegate())

    # Match /json/legals_XX.json where XX is a 2-letter language code
    @app.get("/json/{filename}")
    async def legals_file(filename: str):
        if re.match(r"^legals_[a-z]{2}\.json$", filename):
            return JSONResponse({
                "PP": config.legal.privacyPolicy,
                "TOU": config.legal.termsOfUse,
            })
        return JSONResponse({"error": "not found"}, status_code=404)

    return app
