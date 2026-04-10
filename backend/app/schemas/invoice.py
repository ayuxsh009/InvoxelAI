from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class InvoiceItemOut(ORMModel):
    id: int
    description: str | None = None
    hsn_sac_code: str | None = None
    quantity: int | None = None
    taxable_amount: float | None = None
    cgst: float | None = None
    sgst: float | None = None
    igst: float | None = None
    total_amount: float | None = None


class InvoiceCreateFromOCR(BaseModel):
    vendor_name: str | None = None
    gstin: str | None = None
    invoice_number: str | None = None
    invoice_date: date | None = None
    hsn_sac_codes: str | None = None
    taxable_amount: float | None = None
    cgst: float | None = None
    sgst: float | None = None
    igst: float | None = None
    grand_total: float | None = None
    ocr_confidence: float | None = None
    raw_ocr_json: dict | None = None


class InvoiceOut(ORMModel):
    id: int
    file_name: str
    vendor_name: str | None = None
    gstin: str | None = None
    invoice_number: str | None = None
    invoice_date: date | None = None
    hsn_sac_codes: str | None = None
    taxable_amount: float | None = None
    cgst: float | None = None
    sgst: float | None = None
    igst: float | None = None
    grand_total: float | None = None
    ocr_confidence: float | None = None
    gst_valid: bool
    gst_calculation_correct: bool
    duplicate_of_id: int | None = None
    ai_correction_notes: str | None = None
    raw_ocr_json: dict | None = None
    created_at: datetime
    updated_at: datetime
    items: list[InvoiceItemOut] = []


class InvoiceFilterParams(BaseModel):
    q: str | None = None
    month: int | None = Field(default=None, ge=1, le=12)
    year: int | None = Field(default=None, ge=2020, le=2100)
    min_gst: float | None = None
    max_gst: float | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class InvoiceListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[InvoiceOut]
