"use client";

import api from "@/lib/api";
import { Button } from "@/components/ui/button";

async function download(path: string, filename: string) {
  const response = await api.get(path, { responseType: "blob" });
  const url = URL.createObjectURL(new Blob([response.data]));
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function ExportButtons() {
  return (
    <div className="flex flex-wrap gap-2">
      <Button variant="outline" size="sm" onClick={() => download("/exports/csv", "invoices.csv")}>Export CSV</Button>
      <Button variant="outline" size="sm" onClick={() => download("/exports/excel", "invoices.xlsx")}>Export Excel</Button>
      <Button variant="outline" size="sm" onClick={() => download("/exports/json", "invoices.json")}>Export JSON</Button>
    </div>
  );
}
