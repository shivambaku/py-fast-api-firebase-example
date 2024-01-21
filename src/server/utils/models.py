from pydantic import BaseModel


class UserModel(BaseModel):
    id: str
    email: str
    is_admin: bool = False
