import asyncio
import json
from datetime import date
from pathlib import Path

from sqlalchemy import delete

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.audit_log import AuditLog
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.user import User, UserRole

DATA_PATH = Path(__file__).resolve().parents[1] / "sample_data" / "invoices.json"


async def seed() -> None:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        invoices = json.load(f)

    async with AsyncSessionLocal() as db:
        await db.execute(delete(AuditLog))
        await db.execute(delete(InvoiceItem))
        await db.execute(delete(Invoice))
        await db.execute(delete(User))
        await db.commit()

        admin = User(
            name="Admin User",
            email="admin@invoxel.ai",
            password_hash=get_password_hash("Admin@1234"),
            role=UserRole.admin,
        )
        accountant = User(
            name="Accountant User",
            email="accountant@invoxel.ai",
            password_hash=get_password_hash("Accountant@1234"),
            role=UserRole.accountant,
        )
        db.add_all([admin, accountant])
        await db.commit()
        await db.refresh(admin)

        for inv in invoices:
            invoice = Invoice(
                uploaded_by=admin.id,
                file_name=inv["file_name"],
                file_path=f"uploads/{inv['file_name']}",
                vendor_name=inv["vendor_name"],
                gstin=inv["gstin"],
                invoice_number=inv["invoice_number"],
                invoice_date=date.fromisoformat(inv["invoice_date"]),
                hsn_sac_codes=", ".join(inv["hsn_sac_codes"]),
                taxable_amount=inv["taxable_amount"],
                cgst=inv["cgst"],
                sgst=inv["sgst"],
                igst=inv["igst"],
                grand_total=inv["grand_total"],
                ocr_confidence=inv["ocr_confidence"],
                gst_valid=True,
                gst_calculation_correct=inv["gst_calculation_correct"],
                ai_correction_notes=inv.get("ai_correction_notes"),
                raw_ocr_json=inv.get("raw_ocr_json", {}),
            )
            db.add(invoice)
            await db.flush()

            item = InvoiceItem(
                invoice_id=invoice.id,
                description="Primary line item",
                hsn_sac_code=inv["hsn_sac_codes"][0] if inv["hsn_sac_codes"] else None,
                quantity=1,
                taxable_amount=inv["taxable_amount"],
                cgst=inv["cgst"],
                sgst=inv["sgst"],
                igst=inv["igst"],
                total_amount=inv["grand_total"],
            )
            db.add(item)

        db.add(
            AuditLog(
                user_id=admin.id,
                action="seed",
                entity="invoice",
                entity_id=None,
                details="Seeded sample invoices and items",
            )
        )
        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
