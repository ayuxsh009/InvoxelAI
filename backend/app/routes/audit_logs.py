from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.audit_log import AuditLog
from app.models.user import User, UserRole
from app.schemas.audit import AuditLogFilterParams, AuditLogListResponse, AuditLogOut

router = APIRouter()


@router.get("", response_model=AuditLogListResponse)
async def list_audit_logs(
    action: str | None = Query(default=None),
    entity: str | None = Query(default=None),
    user_id: int | None = Query(default=None),
    q: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    filters = AuditLogFilterParams(
        action=action,
        entity=entity,
        user_id=user_id,
        q=q,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )

    clauses = []
    if filters.action:
        clauses.append(AuditLog.action == filters.action)
    if filters.entity:
        clauses.append(AuditLog.entity == filters.entity)
    if filters.user_id is not None:
        clauses.append(AuditLog.user_id == filters.user_id)
    if filters.q:
        like = f"%{filters.q.strip()}%"
        clauses.append(or_(AuditLog.details.ilike(like), AuditLog.entity_id.ilike(like)))
    if filters.start_date:
        clauses.append(AuditLog.created_at >= filters.start_date)
    if filters.end_date:
        clauses.append(AuditLog.created_at <= filters.end_date)

    query = select(AuditLog).order_by(AuditLog.created_at.desc())
    count_query = select(func.count(AuditLog.id))
    if clauses:
        query = query.where(and_(*clauses))
        count_query = count_query.where(and_(*clauses))

    total = (await db.execute(count_query)).scalar_one()
    offset = (filters.page - 1) * filters.page_size
    result = await db.execute(query.offset(offset).limit(filters.page_size))
    return AuditLogListResponse(
        total=int(total or 0),
        page=filters.page,
        page_size=filters.page_size,
        results=list(result.scalars().all()),
    )
