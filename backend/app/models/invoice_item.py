from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), index=True)
    description: Mapped[str | None] = mapped_column(String(255))
    hsn_sac_code: Mapped[str | None] = mapped_column(String(30), index=True)
    quantity: Mapped[int | None] = mapped_column(Integer)
    taxable_amount: Mapped[float | None] = mapped_column(Float)
    cgst: Mapped[float | None] = mapped_column(Float)
    sgst: Mapped[float | None] = mapped_column(Float)
    igst: Mapped[float | None] = mapped_column(Float)
    total_amount: Mapped[float | None] = mapped_column(Float)

    invoice = relationship("Invoice", back_populates="items")
