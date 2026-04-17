"use client";

import { useEffect, useState } from "react";

import { ProtectedShell } from "@/components/layout/protected-shell";
import { GSTChart } from "@/components/dashboard/gst-chart";
import { SummaryCards } from "@/components/dashboard/summary-cards";
import { analyticsApi } from "@/lib/api";
import type { DashboardData } from "@/types";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    analyticsApi.dashboard().then(setData);
  }, []);

  return (
    <ProtectedShell>
      {data ? (
        <div className="space-y-6">
          <SummaryCards
            totalInvoices={data.summary.total_invoices}
            taxable={data.summary.total_taxable_amount}
            gst={data.summary.total_gst}
            grand={data.summary.total_grand_total}
          />
          <GSTChart data={data.monthly_gst} />
        </div>
      ) : (
        <p>Loading dashboard...</p>
      )}
    </ProtectedShell>
  );
}
