from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.users.enums import RegisterRole, Role


class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    password: str
    role: RegisterRole = RegisterRole.JUNIOR

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(),
        password: str = Form(),
        role: RegisterRole = Form(),
        first_name: str | None = Form(default=None),
        last_name: str | None = Form(default=None),
    ):
        return cls(
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )


class UserResponse(UserBase):
    date_joined: datetime
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role: RegisterRole | None = None
    email: EmailStr | None = None

    @classmethod
    def as_form(
        cls,
        first_name: str | None = Form(default=None),
        last_name: str | None = Form(default=None),
        role: RegisterRole | None = Form(default=None),
        email: EmailStr | None = Form(default=None),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
        )

    model_config = ConfigDict(from_attributes=True)


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

    @classmethod
    def as_form(
        cls,
        old_password: str = Form(..., min_length=6),
        new_password: str = Form(..., min_length=6),
    ):
        return cls(
            old_password=old_password,
            new_password=new_password,
        )
