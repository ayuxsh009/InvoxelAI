from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.invoice import InvoiceFilterParams, InvoiceStatus
from app.services.export_service import export_csv, export_excel, export_json

router = APIRouter()


@router.get("/csv")
async def download_csv(
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
        page=1,
        page_size=1,
    )
    payload = await export_csv(db, filters)
    return Response(
        content=payload,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=invoices.csv"},
    )


@router.get("/excel")
async def download_excel(
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
        page=1,
        page_size=1,
    )
    payload = await export_excel(db, filters)
    return Response(
        content=payload,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=invoices.xlsx"},
    )


@router.get("/json")
async def download_json(
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
        page=1,
        page_size=1,
    )
    payload = await export_json(db, filters)
    return Response(
        content=payload,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=invoices.json"},
    )
