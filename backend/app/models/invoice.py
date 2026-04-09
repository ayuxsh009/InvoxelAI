from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    vendor_name: Mapped[str | None] = mapped_column(String(255))
    gstin: Mapped[str | None] = mapped_column(String(15), index=True)
    invoice_number: Mapped[str | None] = mapped_column(String(100), index=True)
    invoice_date: Mapped[date | None] = mapped_column(Date)
    hsn_sac_codes: Mapped[str | None] = mapped_column(Text)

    taxable_amount: Mapped[float | None] = mapped_column(Float)
    cgst: Mapped[float | None] = mapped_column(Float)
    sgst: Mapped[float | None] = mapped_column(Float)
    igst: Mapped[float | None] = mapped_column(Float)
    grand_total: Mapped[float | None] = mapped_column(Float)

    ocr_confidence: Mapped[float | None] = mapped_column(Float)
    gst_valid: Mapped[bool] = mapped_column(default=False)
    gst_calculation_correct: Mapped[bool] = mapped_column(default=False)
    duplicate_of_id: Mapped[int | None] = mapped_column(ForeignKey("invoices.id"), nullable=True)
    ai_correction_notes: Mapped[str | None] = mapped_column(Text)
    raw_ocr_json: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
