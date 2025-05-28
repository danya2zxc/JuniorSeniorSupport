from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.issues.service import IssueCRUD, MessageCRUD


def get_issue_crud(
    db: AsyncSession = Depends(get_async_session),
) -> IssueCRUD:
    return IssueCRUD(db=db)


def get_message_crud(
    db: AsyncSession = Depends(get_async_session),
) -> MessageCRUD:
    return MessageCRUD(db=db)
