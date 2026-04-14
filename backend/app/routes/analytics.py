from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.analytics import DashboardResponse, DashboardSummary, MonthlyGSTEntry
from app.services.analytics_service import dashboard_summary, monthly_gst_summary

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    summary = await dashboard_summary(db)
    monthly = await monthly_gst_summary(db)
    return DashboardResponse(
        summary=DashboardSummary(**summary),
        monthly_gst=[MonthlyGSTEntry(**m) for m in monthly],
    )
