import re

from dateutil import parser as date_parser
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice


async def run_chat_query(db: AsyncSession, message: str) -> dict:
    text = message.strip()
    lower = text.lower()
    gst_match = re.search(r"gst\s*(>|<|>=|<=|=)\s*(\d+(?:\.\d+)?)", lower)
    vendor_match = re.search(r"(?:vendor|supplier)\s*[:=]\s*([\w\s&\-\.]+)", text, re.I)
    date_range_match = re.search(
        r"(?:from|since)\s*([0-9]{4}-[0-9]{2}-[0-9]{2})(?:\s*(?:to|until)\s*([0-9]{4}-[0-9]{2}-[0-9]{2}))?",
        lower,
    )

    query = select(Invoice)
    interpreted_parts: list[str] = []

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
        interpreted_parts.append(f"total_gst {op} {amount}")

    if vendor_match:
        vendor = vendor_match.group(1).strip()
        if vendor:
            query = query.where(Invoice.vendor_name.ilike(f"%{vendor}%"))
            interpreted_parts.append(f"vendor contains '{vendor}'")

    if date_range_match:
        start = date_range_match.group(1)
        end = date_range_match.group(2)
        try:
            start_date = date_parser.parse(start).date()
        except (ValueError, TypeError):
            start_date = None
        end_date = None
        if end:
            try:
                end_date = date_parser.parse(end).date()
            except (ValueError, TypeError):
                end_date = None

        if start_date:
            query = query.where(Invoice.invoice_date >= start_date)
            interpreted_parts.append(f"from {start_date.isoformat()}")
        if end_date:
            query = query.where(Invoice.invoice_date <= end_date)
            interpreted_parts.append(f"to {end_date.isoformat()}")

    result = await db.execute(query.order_by(Invoice.created_at.desc()).limit(50))
    invoices = result.scalars().all()

    interpreted = ", ".join(interpreted_parts) if interpreted_parts else "No filter"

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
