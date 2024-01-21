from dotenv import load_dotenv
from fastapi import FastAPI

from server.apis.users.routes import router as user_router
from server.middlewares.exception_handler import ExceptionHandlerMiddleware
from server.middlewares.router_logging import RouterLoggingMiddleware
from server.utils.logging import logger

load_dotenv()

app = FastAPI()

app.add_middleware(RouterLoggingMiddleware, logger=logger)
app.add_middleware(ExceptionHandlerMiddleware, logger=logger)


@app.get("/")
async def root() -> dict:
    return {"ping": "pong"}


app.include_router(user_router)
