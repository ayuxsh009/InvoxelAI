from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


async def log_action(
    db: AsyncSession,
    action: str,
    entity: str,
    entity_id: str | None,
    details: str | None,
    user_id: int | None,
) -> None:
    audit = AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id,
        details=details,
        user_id=user_id,
    )
    db.add(audit)
    await db.commit()
