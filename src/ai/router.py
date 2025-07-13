from fastapi import APIRouter, Depends

from src.ai.service import GPTCRUD
from src.shared.permissions import RoleChecker
from src.users.enums import Role
from src.users.models import User

router = APIRouter(
    prefix="/assistant",
)


@router.post("/ask")
async def ask_gpt(
    question: str,
    gpt_crud: GPTCRUD = Depends(GPTCRUD),
    current_user: User = Depends(
        RoleChecker(
            Role.JUNIOR,
            error_message="Access denied: only registered juniors can use assistant.",  # noqa: E501
        )
    ),
):
    await gpt_crud.check_limit(current_user.id)

    response = await gpt_crud.ask_gpt(question, user_id=current_user.id)
    return response
