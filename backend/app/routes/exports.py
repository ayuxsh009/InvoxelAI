from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, UserRole
from app.services.export_service import export_csv, export_excel, export_json

router = APIRouter()


@router.get("/csv")
async def download_csv(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    payload = await export_csv(db)
    return Response(
        content=payload,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=invoices.csv"},
    )


@router.get("/excel")
async def download_excel(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    payload = await export_excel(db)
    return Response(
        content=payload,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=invoices.xlsx"},
    )


@router.get("/json")
async def download_json(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.accountant)),
):
    payload = await export_json(db)
    return Response(
        content=payload,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=invoices.json"},
    )
