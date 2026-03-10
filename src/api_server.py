import os
from contextlib import asynccontextmanager
import re

from fastapi import FastAPI, Request, Response
from starlette.types import ASGIApp, Receive, Scope, Send

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
from .routes.user.user_home_refresh import user_home_refresh
from .routes.user.story.post_user_story import post_user_story
from .routes.user.get_user_areas import get_user_areas
from .routes.user.story.post_user_story_log import post_user_story_log

class DecryptBodyMiddleware:
    """Pure ASGI middleware to decrypt incoming octet-stream bodies (msgpack + AES)."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        state = scope.setdefault("state", {})
        state["decrypted_body"] = None

        # Check content-type from headers
        headers = dict(scope.get("headers", []))
        content_type = headers.get(b"content-type", b"").decode("utf-8", errors="replace")
        path = scope.get("path", "/")

        if content_type == "application/octet-stream":
            # Collect the full request body
            body_chunks = []
            body_complete = False
            
            if re.compile(r'^/api/user/\d{18}/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$').match(path):
                state['decrypted_body'] = {} # Post user param causes somme problems when decrypting, we do not store user param
                await self.app(scope, receive, send)
                return

            async def receive_wrapper():
                nonlocal body_complete
                message = await receive()
                if message["type"] == "http.request":
                    body = message.get("body", b"")
                    if body:
                        body_chunks.append(body)
                    if not message.get("more_body", False):
                        body_complete = True
                return message

            # Read the body by consuming receive messages
            while not body_complete:
                await receive_wrapper()

            body_bytes = b"".join(body_chunks)
            if body_bytes and len(body_bytes) > 0:
                try:
                    state["decrypted_body"] = decrypt(body_bytes)
                except Exception as e:
                    logger.error(f"Failed to decrypt body: {e}")

            # Since we consumed the body, we need to replay it for downstream
            body_sent = False

            async def replay_receive():
                nonlocal body_sent
                if not body_sent:
                    body_sent = True
                    return {"type": "http.request", "body": body_bytes, "more_body": False}
                # After body is sent, pass through to original receive for disconnect etc.
                return await receive()

            await self.app(scope, replay_receive, send)
        else:
            await self.app(scope, receive, send)



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
    
    app.add_api_route("/api/information", get_informations_route, methods=["GET"])
    
    app.add_api_route("/api/user", register_user_route, methods=["POST"])

    app.add_api_route("/api/suitemasterfile/{version}/{fileName}", suite_master_file_route, methods=["GET"])
    
    app.add_api_route("/api/suite/user/{userId}", get_suite_user, methods=['GET'])

    app.add_api_route("/api/user/na/{userId}/legal/ageinfo", user_age_info_route, methods=["GET"])
    app.add_api_route('/api/user/{userId}/home/refresh', user_home_refresh, methods=['PUT'])

    app.add_api_route("/api/user/{userId}/auth", user_auth_route, methods=["PUT"])
    app.add_api_route("/api/user/{userId}/tutorial", set_tutorial_status_route, methods=["PATCH"])
    app.add_api_route("/api/user/{userId}", patch_user_route, methods=["PATCH"])

    app.add_api_route("/api/user/{userId}/live", start_live_route, methods=["POST"])
    app.add_api_route("/api/user/{userId}/live/{liveId}", finish_live_route, methods=["PUT"])
    
    app.add_api_route('/api/user/{userId}/story/{storyType}/episode/{episodeId}', post_user_story, methods=['POST'])
    app.add_api_route('/api/user/{userId}/story/{storyType}/episode/{episodeId}/log', post_user_story_log, methods=['POST'])

    # Catch-all param route - must be LAST among /api/user/{userId}/... POST routes
    app.add_api_route("/api/user/{userId}/{id}", post_user_param, methods=["POST"])
    
    app.add_api_route('/api/user/{userId}/area', get_user_areas, methods=['GET'])

    return app
