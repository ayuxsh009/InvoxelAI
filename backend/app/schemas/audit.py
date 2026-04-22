from datetime import datetime

from app.schemas.common import ORMModel


class AuditLogOut(ORMModel):
    id: int
    user_id: int | None
    action: str
    entity: str
    entity_id: str | None
    details: str | None
    created_at: datetime
