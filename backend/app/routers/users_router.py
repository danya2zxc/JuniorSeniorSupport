from typing import List

from crud.user_crud import UserCRUD
from database import get_async_session
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from schemas.users_schema import UserCreate, UserResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_async_session)
):
    users_crud = UserCRUD(db)
    users = await users_crud.get_all(skip, limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_async_session)):
    users_crud = UserCRUD(db)
    user = await users_crud.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_async_session)):
    user_crud = UserCRUD(db)
    existing_user = await user_crud.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    new_user = await user_crud.create_user(user_data)
    return new_user
