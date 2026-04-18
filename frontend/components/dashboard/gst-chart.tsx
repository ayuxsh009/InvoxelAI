"use client";

import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function GSTChart({ data }: { data: Array<{ month: string; cgst: number; sgst: number; igst: number }> }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Monthly GST Summary</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="cgst" fill="#f97316" radius={[8, 8, 0, 0]} />
              <Bar dataKey="sgst" fill="#f59e0b" radius={[8, 8, 0, 0]} />
              <Bar dataKey="igst" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
