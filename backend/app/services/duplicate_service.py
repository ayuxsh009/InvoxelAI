from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice


async def detect_duplicate_invoice(db: AsyncSession, data: dict) -> int | None:
    if not data.get("invoice_number"):
        return None

    result = await db.execute(
        select(Invoice).where(
            Invoice.invoice_number == data.get("invoice_number"),
            Invoice.grand_total == data.get("grand_total"),
            Invoice.invoice_date == data.get("invoice_date"),
        )
    )
    # Multiple historical matches can exist; treat the latest one as duplicate target.
    existing = result.scalars().first()
    return existing.id if existing else None
