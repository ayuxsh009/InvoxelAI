import re

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice


async def run_chat_query(db: AsyncSession, message: str) -> dict:
    text = message.lower().strip()
    gst_match = re.search(r"gst\s*(>|<|>=|<=|=)\s*(\d+(?:\.\d+)?)", text)

    query = select(Invoice)
    interpreted = "No filter"

    if gst_match:
        op, amount_str = gst_match.group(1), gst_match.group(2)
        amount = float(amount_str)
        gst_expr = func.coalesce(Invoice.cgst, 0) + func.coalesce(Invoice.sgst, 0) + func.coalesce(
            Invoice.igst, 0
        )

        if op == ">":
            query = query.where(gst_expr > amount)
        elif op == "<":
            query = query.where(gst_expr < amount)
        elif op == ">=":
            query = query.where(gst_expr >= amount)
        elif op == "<=":
            query = query.where(gst_expr <= amount)
        else:
            query = query.where(gst_expr == amount)
        interpreted = f"total_gst {op} {amount}"

    result = await db.execute(query.order_by(Invoice.created_at.desc()).limit(50))
    invoices = result.scalars().all()

    return {
        "interpreted_filter": interpreted,
        "count": len(invoices),
        "invoices": [
            {
                "id": i.id,
                "vendor_name": i.vendor_name,
                "invoice_number": i.invoice_number,
                "grand_total": i.grand_total,
                "gst": (i.cgst or 0) + (i.sgst or 0) + (i.igst or 0),
            }
            for i in invoices
        ],
    }
