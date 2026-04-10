from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_invoices: int
    total_taxable_amount: float
    total_gst: float
    total_grand_total: float


class MonthlyGSTEntry(BaseModel):
    month: str
    cgst: float
    sgst: float
    igst: float
    total_gst: float


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    monthly_gst: list[MonthlyGSTEntry]
