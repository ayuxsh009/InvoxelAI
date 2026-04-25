from datetime import date

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.invoice import (
    InvoiceFilterParams,
    InvoiceListResponse,
    InvoiceOut,
    InvoiceStatus,
    InvoiceStatusUpdate,
)
from app.services.audit_service import log_action
from app.services.invoice_service import (
    create_invoice_from_extraction,
    get_invoice,
    list_invoices,
    update_invoice_status,
)
from app.services.ocr_service import OCRService
from app.utils.file import save_upload_file

router = APIRouter()
ocr_service = OCRService()


@router.post("/upload", response_model=InvoiceOut)
async def upload_invoice(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    file_name, file_path = await save_upload_file(file)
    extraction = ocr_service.run(file_path)
    invoice = await create_invoice_from_extraction(db, current_user, file_name, file_path, extraction)
    # Re-fetch with eager-loaded relationships to avoid async lazy-load during response serialization.
    invoice = await get_invoice(db, invoice.id)
    await log_action(
        db,
        "upload_invoice",
        "invoice",
        str(invoice.id),
        f"Uploaded and extracted invoice {invoice.invoice_number}",
        current_user.id,
    )
    return invoice


@router.get("", response_model=InvoiceListResponse)
async def get_invoices(
    q: str | None = Query(default=None),
    status: InvoiceStatus | None = Query(default=None),
    gst_valid: bool | None = Query(default=None),
    duplicate_only: bool = Query(default=False),
    month: int | None = Query(default=None),
    year: int | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    min_gst: float | None = Query(default=None),
    max_gst: float | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    filters = InvoiceFilterParams(
        q=q,
        status=status,
        gst_valid=gst_valid,
        duplicate_only=duplicate_only,
        month=month,
        year=year,
        start_date=start_date,
        end_date=end_date,
        min_gst=min_gst,
        max_gst=max_gst,
        page=page,
        page_size=page_size,
    )
    total, rows = await list_invoices(db, filters)
    return InvoiceListResponse(total=total, page=page, page_size=page_size, results=rows)


@router.get("/{invoice_id}", response_model=InvoiceOut)
async def get_invoice_by_id(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    return await get_invoice(db, invoice_id)


@router.patch("/{invoice_id}/status", response_model=InvoiceOut)
async def patch_invoice_status(
    invoice_id: int,
    payload: InvoiceStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    invoice = await update_invoice_status(db, invoice_id, payload.status, payload.paid_at)
    await log_action(
        db,
        "update_invoice_status",
        "invoice",
        str(invoice.id),
        f"Updated invoice status to {invoice.status}",
        current_user.id,
    )
    return invoice
