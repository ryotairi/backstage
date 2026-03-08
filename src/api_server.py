from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .config import config
from .utils.crypt import decrypt, encrypt
from .middlewares.api_logger import ApiLoggerMiddleware
from .middlewares.authentication import AuthenticationMiddleware
from .services.logger import logger

from .routes.get_system import get_system_route
from .routes.get_information import get_informations_route
from .routes.register_user import register_user_route
from .routes.user_auth import user_auth_route
from .routes.set_tutorial_status import set_tutorial_status_route
from .routes.suite_master_file import suite_master_file_route
from .routes.legal.user_age_info import user_age_info_route
from .routes.live.start_live import start_live_route
from .routes.live.finish_live import finish_live_route
from .routes.user.patch_user import patch_user_route
from .routes.user.get_suite_user import get_suite_user
from .routes.user.post_user_param import post_user_param

class DecryptBodyMiddleware(BaseHTTPMiddleware):
    """Middleware to decrypt incoming octet-stream bodies (msgpack + AES)."""

    async def dispatch(self, request: Request, call_next):
        request.state.decrypted_body = None
        content_type = request.headers.get("content-type", "")
        if content_type == "application/octet-stream":
            body_bytes = await request.body()
            if body_bytes and len(body_bytes) > 0:
                try:
                    request.state.decrypted_body = decrypt(body_bytes)
                except Exception as e:
                    logger.error(f"Failed to decrypt body: {e}")
        return await call_next(request)


def create_api_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)

    # Add middleware (order matters - last added = first executed)
    app.add_middleware(DecryptBodyMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(ApiLoggerMiddleware)

    # Error handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}", exc_info=True)
        return Response(
            content=encrypt({
                "httpStatus": 500,
                "errorCode": "internal_server_error",
                "errorMessage": "",
            }),
            status_code=500,
            media_type="application/octet-stream",
        )

    # Routes
    app.add_api_route("/api/system", get_system_route, methods=["GET"])
    app.add_api_route("/api/informations", get_informations_route, methods=["GET"])
    app.add_api_route("/api/user", register_user_route, methods=["POST"])

    app.add_api_route("/api/suitemasterfile/{version}/{fileName}", suite_master_file_route, methods=["GET"])
    
    app.add_api_route("/api/suite/user/{userId}", get_suite_user, methods=['GET'])

    app.add_api_route("/api/user/na/{userId}/legal/ageinfo", user_age_info_route, methods=["GET"])
    app.add_api_route("/api/user/{userId}/{id}", post_user_param, methods=["POST"])

    app.add_api_route("/api/user/{userId}/auth", user_auth_route, methods=["PUT"])
    app.add_api_route("/api/user/{userId}/tutorial", set_tutorial_status_route, methods=["PATCH"])
    app.add_api_route("/api/user/{userId}", patch_user_route, methods=["PATCH"])

    app.add_api_route("/api/user/{userId}/live", start_live_route, methods=["POST"])
    app.add_api_route("/api/user/{userId}/live/{liveId}", finish_live_route, methods=["POST"])

    return app
