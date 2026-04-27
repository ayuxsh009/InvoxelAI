export type UserRole = "admin" | "accountant";
export type InvoiceStatus = "pending" | "paid" | "flagged";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
}

export interface Invoice {
  id: number;
  file_name: string;
  vendor_name?: string;
  gstin?: string;
  invoice_number?: string;
  invoice_date?: string;
  taxable_amount?: number;
  cgst?: number;
  sgst?: number;
  igst?: number;
  grand_total?: number;
  status: InvoiceStatus;
  paid_at?: string | null;
  ocr_confidence?: number;
  gst_valid: boolean;
  gst_calculation_correct: boolean;
  duplicate_of_id?: number | null;
  ai_correction_notes?: string | null;
  created_at: string;
}

export interface InvoiceListResponse {
  total: number;
  page: number;
  page_size: number;
  results: Invoice[];
}

export interface DashboardData {
  summary: {
    total_invoices: number;
    total_taxable_amount: number;
    total_gst: number;
    total_grand_total: number;
  };
  monthly_gst: Array<{
    month: string;
    cgst: number;
    sgst: number;
    igst: number;
    total_gst: number;
  }>;
}
