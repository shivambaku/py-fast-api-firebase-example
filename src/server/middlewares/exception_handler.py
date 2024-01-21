import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from server.utils.exceptions import ClientException
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, *, logger: logging.Logger) -> None:
        self.logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        self.logger.debug("Exception Handling Middleware")

        try:
            return await call_next(request)
        except ClientException as e:
            return self.consume_and_log_client_error(e)
        except Exception as e:
            return self.consume_and_log_internal_errors(e)

    def consume_and_log_client_error(self, e: ClientException):
        return JSONResponse(
            status_code=e.status_code,
            content={
                "detail": str(e),
            },
        )

    def consume_and_log_internal_errors(self, e: Exception):
        self.logger.exception(msg=e.__class__.__name__, exc_info=e)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error.",
            },
        )
