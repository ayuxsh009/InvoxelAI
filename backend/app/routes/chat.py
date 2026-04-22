from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.services.chat_service import run_chat_query

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse)
async def query_invoices(
    payload: ChatQueryRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    return await run_chat_query(db, payload.message)
