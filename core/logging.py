from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import time
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        print(f"method: {request.method}, path: {request.url.path}, status: {response.status_code}, duration: {duration}")
        return response