from src.shared.security import verify_password
from src.users.service import UserCRUD


async def authenticate_user(user_crud: UserCRUD, email: str, password: str):
    user = await user_crud.get_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
