"use client";

import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import type { Invoice } from "@/types";

export function InvoiceDetailModal({
  open,
  onOpenChange,
  invoice
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  invoice: Invoice | null;
}) {
  if (!invoice) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <h3 className="mb-4 text-xl font-bold">Invoice #{invoice.invoice_number || invoice.id}</h3>
        <div className="grid gap-2 text-sm">
          <p><b>Vendor:</b> {invoice.vendor_name || "-"}</p>
          <p><b>GSTIN:</b> {invoice.gstin || "-"}</p>
          <p><b>Date:</b> {invoice.invoice_date || "-"}</p>
          <p><b>Taxable:</b> Rs {invoice.taxable_amount || 0}</p>
          <p><b>CGST:</b> Rs {invoice.cgst || 0}</p>
          <p><b>SGST:</b> Rs {invoice.sgst || 0}</p>
          <p><b>IGST:</b> Rs {invoice.igst || 0}</p>
          <p><b>Total:</b> Rs {invoice.grand_total || 0}</p>
          <p><b>OCR Confidence:</b> {((invoice.ocr_confidence || 0) * 100).toFixed(1)}%</p>
          <div className="flex gap-2 pt-2">
            <Badge>{invoice.gst_valid ? "GSTIN Valid" : "GSTIN Invalid"}</Badge>
            <Badge>{invoice.gst_calculation_correct ? "GST Correct" : "GST Mismatch"}</Badge>
            {invoice.duplicate_of_id ? <Badge>Duplicate #{invoice.duplicate_of_id}</Badge> : null}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
