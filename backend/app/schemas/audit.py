from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class AuditLogOut(ORMModel):
    id: int
    user_id: int | None
    action: str
    entity: str
    entity_id: str | None
    details: str | None
    created_at: datetime


class AuditLogFilterParams(BaseModel):
    action: str | None = None
    entity: str | None = None
    user_id: int | None = None
    q: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)


class AuditLogListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[AuditLogOut]
