from fastapi import Depends, HTTPException, status

from src.auth.dependencies import get_current_user
from src.users.enums import Role
from src.users.models import User


class RoleChecker:
    def __init__(self, *roles: Role, error_message: str | None = None):
        self.roles = roles
        self.error_message = error_message

    async def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.error_message or "Access denied",
            )
        return current_user
