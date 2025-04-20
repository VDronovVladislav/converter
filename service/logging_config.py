import logging
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class HTTPLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware, логирующий тело запроса и ответа на уровне DEBUG.
    Подключается только при debug=True.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        body = await request.body()
        logger.debug(f"Request body: {body!r}")

        async def receive() -> dict:
            return {"type": "http.request", "body": body}
        request._receive = receive

        response = await call_next(request)
        resp_body = b""
        async for chunk in response.body_iterator:
            resp_body += chunk
        logger.debug(f"Response body: {resp_body!r}")

        async def new_body_iterator():
            yield resp_body
        response.body_iterator = new_body_iterator()
        return response
