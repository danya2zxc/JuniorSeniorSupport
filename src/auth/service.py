from datetime import datetime, timedelta, timezone

import jwt

from src.auth.security import verify_password
from src.config import settings
from src.users.service import UserCRUD


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def authenticate_user(user_crud: UserCRUD, email: str, password: str):
    user = await user_crud.get_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
