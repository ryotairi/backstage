import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ..services.logger import logger


class ApiLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        method = request.method
        host = request.headers.get("host", "")
        path = request.url.path

        logger.info(f"--> {method} {host}{path}")

        response: Response = await call_next(request)

        duration_ms = int((time.time() - start) * 1000)
        status = response.status_code

        if status >= 400:
            logger.error(f"<-- {method} {host}{path} {status} ({duration_ms}ms)")
        else:
            logger.info(f"<-- {method} {host}{path} {status} ({duration_ms}ms)")

        return response
