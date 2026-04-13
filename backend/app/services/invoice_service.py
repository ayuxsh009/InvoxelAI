from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.invoice import Invoice
from app.models.user import User
from app.schemas.invoice import InvoiceFilterParams
from app.services.correction_service import apply_ai_corrections
from app.services.duplicate_service import detect_duplicate_invoice
from app.validators.gst import is_valid_gstin
from app.validators.tax import is_gst_calculation_correct


async def create_invoice_from_extraction(
    db: AsyncSession,
    user: User,
    file_name: str,
    file_path: str,
    extraction: dict,
) -> Invoice:
    parsed = extraction["parsed"]
    raw = extraction["raw"]

    parsed, notes = apply_ai_corrections(parsed)
    duplicate_id = await detect_duplicate_invoice(db, parsed)
    gst_valid = is_valid_gstin(parsed.get("gstin"))
    gst_calc_ok = is_gst_calculation_correct(
        parsed.get("taxable_amount"),
        parsed.get("cgst"),
        parsed.get("sgst"),
        parsed.get("igst"),
        parsed.get("grand_total"),
    )

    invoice = Invoice(
        uploaded_by=user.id,
        file_name=file_name,
        file_path=file_path,
        vendor_name=parsed.get("vendor_name"),
        gstin=parsed.get("gstin"),
        invoice_number=parsed.get("invoice_number"),
        invoice_date=parsed.get("invoice_date"),
        hsn_sac_codes=parsed.get("hsn_sac_codes"),
        taxable_amount=parsed.get("taxable_amount"),
        cgst=parsed.get("cgst"),
        sgst=parsed.get("sgst"),
        igst=parsed.get("igst"),
        grand_total=parsed.get("grand_total"),
        ocr_confidence=raw.get("confidence", 0.0),
        gst_valid=gst_valid,
        gst_calculation_correct=gst_calc_ok,
        duplicate_of_id=duplicate_id,
        ai_correction_notes=notes,
        raw_ocr_json=raw,
    )
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def list_invoices(db: AsyncSession, filters: InvoiceFilterParams) -> tuple[int, list[Invoice]]:
    clauses = []
    if filters.q:
        q = f"%{filters.q.strip()}%"
        clauses.append(
            or_(
                Invoice.vendor_name.ilike(q),
                Invoice.invoice_number.ilike(q),
                Invoice.gstin.ilike(q),
            )
        )

    if filters.month:
        clauses.append(func.extract("month", Invoice.invoice_date) == filters.month)
    if filters.year:
        clauses.append(func.extract("year", Invoice.invoice_date) == filters.year)

    if filters.min_gst is not None:
        clauses.append((func.coalesce(Invoice.cgst, 0) + func.coalesce(Invoice.sgst, 0) + func.coalesce(Invoice.igst, 0)) >= filters.min_gst)
    if filters.max_gst is not None:
        clauses.append((func.coalesce(Invoice.cgst, 0) + func.coalesce(Invoice.sgst, 0) + func.coalesce(Invoice.igst, 0)) <= filters.max_gst)

    query = select(Invoice).options(selectinload(Invoice.items))
    count_query = select(func.count(Invoice.id))
    if clauses:
        query = query.where(and_(*clauses))
        count_query = count_query.where(and_(*clauses))

    total = (await db.execute(count_query)).scalar_one()
    offset = (filters.page - 1) * filters.page_size
    result = await db.execute(
        query.order_by(Invoice.created_at.desc()).offset(offset).limit(filters.page_size)
    )
    return int(total), list(result.scalars().all())


async def get_invoice(db: AsyncSession, invoice_id: int) -> Invoice:
    result = await db.execute(
        select(Invoice).options(selectinload(Invoice.items)).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
