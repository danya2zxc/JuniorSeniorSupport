from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.mailing.service import ActivationService
from src.shared.security import get_password_hash, verify_password
from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        query = select(User).filter(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate):
        user_dict = user_data.model_dump(exclude={"password"})
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            **user_dict,
            hashed_password=hashed_password,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        activation = ActivationService()
        token = activation.create_token(user_data.email)
        activation.send_user_activation_email(user_data.email, token)
        activation.save_activation_information(new_user.id, token)

        return new_user

    async def update_user(self, user_id: int, update_data: UserUpdate):
        user = await self.get_by_id(user_id=user_id)
        if user is None:
            return None
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def change_password(
        self, user_id: int, old_password: str, new_password: str
    ):
        user = await self.get_by_id(user_id=user_id)
        if user is None:
            return None
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=403, detail="Incorrect password")
        if old_password == new_password:
            raise HTTPException(
                status_code=400,
                detail="New password must be different from old password",
            )

        user.hashed_password = get_password_hash(new_password)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        user = await self.get_by_id(user_id)
        if user is None:
            return None
        await self.db.delete(user)
        await self.db.commit()
        return user

    async def mark_as_verified(self, user_id: int):
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(404, "User not found")
        user.is_verified = True
        await self.db.commit()
        return user
