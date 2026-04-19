"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { chatApi } from "@/lib/api";

export function ChatPanel() {
  const [message, setMessage] = useState("Show invoices where GST > 5000");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Invoice Query Assistant</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex gap-2">
          <Input value={message} onChange={(e) => setMessage(e.target.value)} />
          <Button
            disabled={loading}
            onClick={async () => {
              setLoading(true);
              try {
                const data = await chatApi.query(message);
                setResult(data);
              } finally {
                setLoading(false);
              }
            }}
          >
            Run
          </Button>
        </div>
        {result ? (
          <div className="space-y-2 rounded-xl bg-muted p-4 text-sm">
            <p><b>Interpreted:</b> {result.interpreted_filter}</p>
            <p><b>Matches:</b> {result.count}</p>
            <ul className="space-y-1">
              {result.invoices.map((inv: any) => (
                <li key={inv.id}>#{inv.id} {inv.vendor_name} | GST {inv.gst}</li>
              ))}
            </ul>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
