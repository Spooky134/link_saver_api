from fastapi import APIRouter

from app.auth.dependencies import CurrentUserDep
from app.user.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def users_me(current_user: CurrentUserDep):
    return current_user
