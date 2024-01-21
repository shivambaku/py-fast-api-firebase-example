from fastapi import APIRouter
from server.apis.users.dependencies import UserDepends

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/")
async def get(user_model: UserDepends):
    return user_model
