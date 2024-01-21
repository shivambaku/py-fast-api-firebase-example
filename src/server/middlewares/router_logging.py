import json
import logging
import time
from typing import Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware


class RouterLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, *, logger: logging.Logger) -> None:
        self.logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        self.logger.debug("Router Logging Middleware")

        request_id = str(uuid4())
        logging_dict: dict[str, object] = {
            "X-API-Request-ID": request_id,
        }

        response, response_dict = await self.log_response(
            call_next, request, request_id
        )
        request_dict = await self.log_request(request)

        logging_dict["response"] = response_dict
        logging_dict["request"] = request_dict

        self.logger.info(logging_dict)

        return response

    async def log_request(self, request: Request) -> dict[str, object]:
        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging: dict[str, object] = {
            "method": request.method,
            "path": request.url.path,
            "ip": request.client.host if request.client else None,
        }

        return request_logging

    async def log_response(
        self, call_next: Callable, request: Request, request_id: str
    ) -> tuple[Response, dict[str, object]]:
        start_time = time.perf_counter()

        try:
            response: Response = await call_next(request)
        except Exception as e:
            raise e

        response.headers["X-API-Request-ID"] = request_id

        end_time = time.perf_counter()
        time_taken_seconds = end_time - start_time
        time_taken_ms = int(round(time_taken_seconds * 1000))

        response_dict: dict[str, object] = {
            "status_code": response.status_code,
            "time_taken_ms": time_taken_ms,
        }

        response_body = [chunk async for chunk in response.__dict__["body_iterator"]]
        response.__setattr__(
            "body_iterator", iterate_in_threadpool(iter(response_body))
        )
        try:
            response_body = json.loads(response_body[0].decode())
        except Exception:
            response_body = str(response_body)

        response_dict["body"] = response_body

        return response, response_dict
