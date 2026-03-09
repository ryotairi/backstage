import time
from starlette.types import ASGIApp, Receive, Scope, Send
from ..services.logger import logger
import json

class ApiLoggerMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.time()
        method = scope.get("method", "")
        path = scope.get("path", "")

        # Extract host from headers
        headers = dict(scope.get("headers", []))
        host = headers.get(b"host", b"").decode("utf-8", errors="replace")

        logger.info(f"--> {method} {host}{path}")

        status_code = 0

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", 0)
            await send(message)

        await self.app(scope, receive, send_wrapper)

        duration_ms = int((time.time() - start) * 1000)

        # Log decrypted body if available
        decrypted_body = scope.get("state", {}).get("decrypted_body", None)
        body_str = ""
        if decrypted_body is not None:
            try:
                body_str = json.dumps(decrypted_body) if not isinstance(decrypted_body, str) else decrypted_body
            except Exception:
                body_str = str(decrypted_body)
        
        if status_code == 400 or status_code == 422:
            logger.error(f"<-- {method} {host}{path} {status_code}: {body_str}")

        if status_code >= 400:
            logger.error(f"<-- {method} {host}{path} {status_code} ({duration_ms}ms)")
        else:
            logger.info(f"<-- {method} {host}{path} {status_code} ({duration_ms}ms)")
