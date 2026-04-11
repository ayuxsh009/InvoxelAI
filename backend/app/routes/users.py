from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserOut

router = APIRouter()


@router.get("/profile", response_model=UserOut)
async def profile(current_user: User = Depends(require_roles(UserRole.admin, UserRole.accountant))):
    return current_user
