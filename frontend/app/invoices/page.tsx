import { ExportButtons } from "@/components/dashboard/export-buttons";
import { InvoiceTable } from "@/components/invoices/invoice-table";
import { ProtectedShell } from "@/components/layout/protected-shell";

export default function InvoicesPage() {
  return (
    <ProtectedShell>
      <div className="space-y-4">
        <ExportButtons />
        <InvoiceTable />
      </div>
    </ProtectedShell>
  );
}
