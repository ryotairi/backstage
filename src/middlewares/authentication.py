import re
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ..utils.crypt import encrypt
from ..models.user import User

PUBLIC_PATHS = [
    re.compile(r"^/api/system$"),
    re.compile(r"^/api/informations$"),
    re.compile(r"^/api/user$"),
    re.compile(r"^/api/user/\d+/auth(\?.+)?$"),
]


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Check if path is public
        for pattern in PUBLIC_PATHS:
            if pattern.search(path):
                request.state.user_id = None
                return await call_next(request)

        credential = request.headers.get("x-session-token")
        if not credential:
            return Response(
                content=encrypt({
                    "httpStatus": 401,
                    "errorCode": "",
                    "errorMessage": "",
                }),
                status_code=401,
                media_type="application/octet-stream",
            )

        user = await User.filter(credential=credential).first()
        if not user:
            return Response(
                content=encrypt({
                    "httpStatus": 401,
                    "errorCode": "",
                    "errorMessage": "",
                }),
                status_code=401,
                media_type="application/octet-stream",
            )

        request.state.user_id = user.userId
        return await call_next(request)
