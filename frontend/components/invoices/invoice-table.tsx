"use client";

import { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { invoiceApi } from "@/lib/api";
import type { Invoice, InvoiceStatus } from "@/types";
import { InvoiceDetailModal } from "@/components/invoices/invoice-detail-modal";

export function InvoiceTable() {
  const [data, setData] = useState<Invoice[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Invoice | null>(null);
  const [status, setStatus] = useState<InvoiceStatus | "">("");
  const [gstValid, setGstValid] = useState<"" | "true" | "false">("");
  const [duplicateOnly, setDuplicateOnly] = useState(false);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await invoiceApi.list({
        page,
        page_size: 10,
        q: q || undefined,
        status: status || undefined,
        gst_valid: gstValid ? gstValid === "true" : undefined,
        duplicate_only: duplicateOnly ? true : undefined,
        start_date: startDate || undefined,
        end_date: endDate || undefined
      });
      setData(res.results);
      setTotal(res.total);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page]);

  return (
    <div className="space-y-4 rounded-2xl border border-border bg-card p-4">
      <div className="flex flex-col gap-3">
        <div className="flex flex-col gap-2 sm:flex-row">
          <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search vendor / invoice / GSTIN" />
          <Button onClick={() => { setPage(1); fetchData(); }}>Search</Button>
        </div>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
          <select
            className="h-10 rounded-md border border-border bg-background px-3 text-sm"
            value={status}
            onChange={(e) => setStatus(e.target.value as InvoiceStatus | "")}
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="paid">Paid</option>
            <option value="flagged">Flagged</option>
          </select>
          <select
            className="h-10 rounded-md border border-border bg-background px-3 text-sm"
            value={gstValid}
            onChange={(e) => setGstValid(e.target.value as "" | "true" | "false")}
          >
            <option value="">GST Validity</option>
            <option value="true">Valid</option>
            <option value="false">Invalid</option>
          </select>
          <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={duplicateOnly}
              onChange={(e) => setDuplicateOnly(e.target.checked)}
            />
            Duplicates only
          </label>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-muted-foreground">
              <th className="p-2">Invoice</th>
              <th className="p-2">Vendor</th>
              <th className="p-2">GST</th>
              <th className="p-2">Total</th>
              <th className="p-2">Status</th>
              <th className="p-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <tr key={i} className="border-b border-border">
                    <td colSpan={6} className="p-2"><Skeleton className="h-8 w-full" /></td>
                  </tr>
                ))
              : data.map((inv) => (
                  <tr key={inv.id} className="border-b border-border">
                    <td className="p-2">{inv.invoice_number || inv.id}</td>
                    <td className="p-2">{inv.vendor_name || "-"}</td>
                    <td className="p-2">{((inv.cgst || 0) + (inv.sgst || 0) + (inv.igst || 0)).toFixed(2)}</td>
                    <td className="p-2">{inv.grand_total?.toFixed(2) || "0.00"}</td>
                    <td className="p-2">
                      <div className="flex flex-wrap gap-2">
                        <Badge className={inv.status === "paid" ? "border-emerald-300 text-emerald-700" : inv.status === "flagged" ? "border-amber-300 text-amber-700" : ""}>
                          {inv.status}
                        </Badge>
                        <Badge>{inv.gst_valid ? "Valid GSTIN" : "Invalid GSTIN"}</Badge>
                        <Badge>{inv.gst_calculation_correct ? "Tax OK" : "Tax Error"}</Badge>
                        {inv.duplicate_of_id ? <Badge>Duplicate</Badge> : null}
                      </div>
                    </td>
                    <td className="p-2">
                      <Button variant="outline" size="sm" onClick={() => setSelected(inv)}>View</Button>
                    </td>
                  </tr>
                ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">Total: {total}</p>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Prev</Button>
          <Button variant="outline" size="sm" onClick={() => setPage((p) => p + 1)}>Next</Button>
        </div>
      </div>

      <InvoiceDetailModal
        open={!!selected}
        onOpenChange={(o) => !o && setSelected(null)}
        invoice={selected}
        onStatusUpdated={(updated) => {
          setData((prev) => prev.map((inv) => (inv.id === updated.id ? updated : inv)));
          setSelected(updated);
        }}
      />
    </div>
  );
}
