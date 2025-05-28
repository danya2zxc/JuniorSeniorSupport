from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.schemas import TokenData
from src.config import settings
from src.users.dependencies import get_user_crud
from src.users.service import UserCRUD

oauth2_scheme_required = OAuth2PasswordBearer(
    tokenUrl="api/auth/login", auto_error=True
)
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="api/auth/login", auto_error=False
)


async def get_current_user(
    token: str = Depends(oauth2_scheme_required),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(
        token, settings.secret_key, algorithms=[settings.algorithm]
    )
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
    token_data = TokenData(email=email)
    user = await user_crud.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def optional_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)],
    user_crud: UserCRUD = Depends(get_user_crud),
):
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email = payload.get("sub")
        if email is None:
            return None
        return await user_crud.get_by_email(email)
    except Exception:
        return None
