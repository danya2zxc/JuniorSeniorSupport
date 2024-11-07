from models.users_model import User
from schemas.users_schema import UserCreate
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserCRUD:
    def __init__(self, db: Session):
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
        new_user = User(**user_data.dict())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
