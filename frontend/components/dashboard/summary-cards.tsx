import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function SummaryCards({
  totalInvoices,
  taxable,
  gst,
  grand
}: {
  totalInvoices: number;
  taxable: number;
  gst: number;
  grand: number;
}) {
  const cards = [
    { label: "Total Invoices", value: totalInvoices.toLocaleString() },
    { label: "Taxable Amount", value: `Rs ${taxable.toLocaleString()}` },
    { label: "Total GST", value: `Rs ${gst.toLocaleString()}` },
    { label: "Grand Total", value: `Rs ${grand.toLocaleString()}` }
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.label}>
          <CardHeader>
            <CardTitle className="text-sm text-muted-foreground">{card.label}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-extrabold">{card.value}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
