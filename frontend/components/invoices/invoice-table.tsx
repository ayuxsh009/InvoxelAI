"use client";

import { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { invoiceApi } from "@/lib/api";
import type { Invoice } from "@/types";
import { InvoiceDetailModal } from "@/components/invoices/invoice-detail-modal";

export function InvoiceTable() {
  const [data, setData] = useState<Invoice[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Invoice | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await invoiceApi.list({ page, page_size: 10, q: q || undefined });
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
      <div className="flex flex-col gap-2 sm:flex-row">
        <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search vendor / invoice / GSTIN" />
        <Button onClick={() => { setPage(1); fetchData(); }}>Search</Button>
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
                      <div className="flex gap-2">
                        <Badge>{inv.gst_valid ? "Valid GSTIN" : "Invalid GSTIN"}</Badge>
                        <Badge>{inv.gst_calculation_correct ? "Tax OK" : "Tax Error"}</Badge>
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

      <InvoiceDetailModal open={!!selected} onOpenChange={(o) => !o && setSelected(null)} invoice={selected} />
    </div>
  );
}
