import io

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice


async def _fetch_invoice_rows(db: AsyncSession) -> list[dict]:
    result = await db.execute(select(Invoice).order_by(Invoice.created_at.desc()))
    invoices = result.scalars().all()
    rows: list[dict] = []
    for inv in invoices:
        rows.append(
            {
                "id": inv.id,
                "vendor_name": inv.vendor_name,
                "gstin": inv.gstin,
                "invoice_number": inv.invoice_number,
                "invoice_date": str(inv.invoice_date) if inv.invoice_date else None,
                "taxable_amount": inv.taxable_amount,
                "cgst": inv.cgst,
                "sgst": inv.sgst,
                "igst": inv.igst,
                "grand_total": inv.grand_total,
                "gst_valid": inv.gst_valid,
                "gst_calculation_correct": inv.gst_calculation_correct,
                "ocr_confidence": inv.ocr_confidence,
                "created_at": inv.created_at.isoformat() if inv.created_at else None,
            }
        )
    return rows


async def export_csv(db: AsyncSession) -> bytes:
    rows = await _fetch_invoice_rows(db)
    df = pd.DataFrame(rows)
    return df.to_csv(index=False).encode("utf-8")


async def export_excel(db: AsyncSession) -> bytes:
    rows = await _fetch_invoice_rows(db)
    df = pd.DataFrame(rows)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="invoices")
    return buffer.getvalue()


async def export_json(db: AsyncSession) -> bytes:
    rows = await _fetch_invoice_rows(db)
    return pd.DataFrame(rows).to_json(orient="records", indent=2).encode("utf-8")
