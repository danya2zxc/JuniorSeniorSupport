from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.service import UserCRUD


def get_user_crud(
    db: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD(db=db)
