from enums.role import Role
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    role: Role
    hashed_password: str
    last_name: str

    class Config:
        orm_mode = True
