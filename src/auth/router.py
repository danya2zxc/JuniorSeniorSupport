# import uuid
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import Token
from src.auth.service import authenticate_user
from src.mailing.service import ActivationService
from src.shared.security import create_access_token
from src.users.dependencies import get_user_crud
from src.users.schemas import UserCreate, UserResponse
from src.users.service import UserCRUD

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token)
async def login(
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


@router.post("/signup", response_model=UserResponse)
async def signup(
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


@router.post("/resend-activation-email")
async def resend_activation_email(
    email: str, user_crud: UserCRUD = Depends(get_user_crud)
):
    user = await user_crud.get_by_email(email)
    if not user:
        raise HTTPException(404, "User not found")
    if user.is_verified:
        raise HTTPException(400, "User is already verified email")

    activation = ActivationService()
    token = activation.create_token(email)

    activation.send_user_activation_email(email, token)
    activation.save_activation_information(user.id, token)


@router.patch("/complete-activation", status_code=200)
async def complete_activation(
    token: uuid.UUID, user_crud: UserCRUD = Depends(get_user_crud)
):

    result = ActivationService().validate_activation(token)
    if not result:
        raise HTTPException(
            status_code=404, detail="Invalid or expired activation link"
        )

    user = await user_crud.mark_as_verified(result["user_id"])
    return {"message": f"User {user.email} verified"}
