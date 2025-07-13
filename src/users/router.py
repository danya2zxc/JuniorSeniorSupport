from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.auth.dependencies import get_current_user
from src.shared.permissions import RoleChecker
from src.users.dependencies import get_user_crud
from src.users.enums import Role
from src.users.models import User
from src.users.schemas import (
    UserCreate,
    UserPasswordUpdate,
    UserResponse,
    UserUpdate,
)
from src.users.service import UserCRUD

router = APIRouter(prefix="/users")


@router.get("", response_model=List[UserResponse])
async def users_list(
    skip: int = 0,
    limit: int = 100,
    user_crud: UserCRUD = Depends(get_user_crud),
    current_user: User = Depends(RoleChecker(Role.ADMIN)),
):
    return await user_crud.get_all(skip, limit)


@router.get("/me", response_model=UserResponse)
async def user_me(
    user_crud: UserCRUD = Depends(get_user_crud),
    current_user: User = Depends(get_current_user),
):
    user = await user_crud.get_by_email(current_user.email)

    return user


@router.get("/{user_id}", response_model=UserResponse)
async def user_get_by_id(
    user_id: int,
    user_crud: UserCRUD = Depends(get_user_crud),
    _: User = Depends(get_current_user),
):
    user = await user_crud.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def user_create(
    user_data: UserCreate = Depends(UserCreate.as_form),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    existing_user = await user_crud.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return await user_crud.create_user(user_data)


@router.patch("/me", response_model=UserResponse)
async def me_update(
    user_data: UserUpdate,
    user_crud: UserCRUD = Depends(get_user_crud),
    current_user: User = Depends(get_current_user),
):
    user = await user_crud.update_user(current_user.id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def user_update(
    user_id: int,
    user_data: UserUpdate,
    user_crud: UserCRUD = Depends(get_user_crud),
    _: User = Depends(RoleChecker(Role.ADMIN)),
):
    user = await user_crud.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{user_id}", status_code=204)
async def user_delete(
    user_id: int,
    user_crud: UserCRUD = Depends(get_user_crud),
    _: User = Depends(RoleChecker(Role.ADMIN)),
):
    user = await user_crud.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return


@router.delete("/me")
async def delete_me(
    current_user: User = Depends(get_current_user),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    await user_crud.delete_user(current_user.id)

    return


@router.patch("/me/password")
async def update_my_password(
    password_data: UserPasswordUpdate = Depends(UserPasswordUpdate.as_form),
    current_user: User = Depends(get_current_user),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    await user_crud.change_password(
        current_user.id, password_data.old_password, password_data.new_password
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Password updated successfully"},
    )
