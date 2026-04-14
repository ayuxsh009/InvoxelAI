from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice


async def dashboard_summary(db: AsyncSession) -> dict:
    result = await db.execute(
        select(
            func.count(Invoice.id),
            func.coalesce(func.sum(Invoice.taxable_amount), 0.0),
            func.coalesce(func.sum(func.coalesce(Invoice.cgst, 0) + func.coalesce(Invoice.sgst, 0) + func.coalesce(Invoice.igst, 0)), 0.0),
            func.coalesce(func.sum(Invoice.grand_total), 0.0),
        )
    )
    total_invoices, total_taxable, total_gst, total_grand = result.one()
    return {
        "total_invoices": int(total_invoices or 0),
        "total_taxable_amount": float(total_taxable or 0.0),
        "total_gst": float(total_gst or 0.0),
        "total_grand_total": float(total_grand or 0.0),
    }


async def monthly_gst_summary(db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(
            func.to_char(Invoice.invoice_date, "YYYY-MM").label("month"),
            func.coalesce(func.sum(Invoice.cgst), 0.0),
            func.coalesce(func.sum(Invoice.sgst), 0.0),
            func.coalesce(func.sum(Invoice.igst), 0.0),
        )
        .where(Invoice.invoice_date.is_not(None))
        .group_by("month")
        .order_by("month")
    )

    rows = []
    for month, cgst, sgst, igst in result.all():
        rows.append(
            {
                "month": month,
                "cgst": float(cgst or 0),
                "sgst": float(sgst or 0),
                "igst": float(igst or 0),
                "total_gst": float((cgst or 0) + (sgst or 0) + (igst or 0)),
            }
        )
    return rows
