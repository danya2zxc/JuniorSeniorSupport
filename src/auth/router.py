from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import Token
from src.auth.service import authenticate_user, create_access_token
from src.users.dependencies import get_user_crud
from src.users.service import UserCRUD

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    user = await authenticate_user(
        user_crud, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
