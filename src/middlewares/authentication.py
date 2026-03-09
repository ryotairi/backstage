import re
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response
from ..utils.crypt import encrypt
from ..models.user import User

PUBLIC_PATHS = [
    re.compile(r"^/api/system$"),
    re.compile(r"^/api/information$"),
    re.compile(r"^/api/user$"),
    re.compile(r"^/api/user/\d+/auth(\?.+)?$"),
]


class AuthenticationMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")

        # Check if path is public
        for pattern in PUBLIC_PATHS:
            if pattern.search(path):
                scope.setdefault("state", {})["user_id"] = None
                await self.app(scope, receive, send)
                return

        # Extract x-session-token from headers
        headers = dict(scope.get("headers", []))
        credential = headers.get(b"x-session-token", b"").decode("utf-8", errors="replace") or None

        if not credential:
            response = Response(
                content=encrypt({
                    "httpStatus": 401,
                    "errorCode": "",
                    "errorMessage": "",
                }),
                status_code=401,
                media_type="application/octet-stream",
            )
            await response(scope, receive, send)
            return

        user = await User.filter(credential=credential).first()
        if not user:
            response = Response(
                content=encrypt({
                    "httpStatus": 401,
                    "errorCode": "",
                    "errorMessage": "",
                }),
                status_code=401,
                media_type="application/octet-stream",
            )
            await response(scope, receive, send)
            return

        scope.setdefault("state", {})["user_id"] = user.userId
        await self.app(scope, receive, send)
