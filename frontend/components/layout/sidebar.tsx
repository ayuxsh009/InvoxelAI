"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, FileText, Home, MessageSquare, UploadCloud } from "lucide-react";

import { cn } from "@/lib/utils";

const nav = [
  { href: "/dashboard", label: "Dashboard", icon: Home },
  { href: "/upload", label: "Upload", icon: UploadCloud },
  { href: "/invoices", label: "Invoices", icon: FileText },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/chat", label: "AI Chat", icon: MessageSquare }
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-full border-b border-border bg-card md:w-64 md:border-b-0 md:border-r">
      <div className="flex items-center gap-2 px-5 py-4">
        <div className="h-8 w-8 rounded-xl bg-primary" />
        <div>
          <p className="text-sm font-medium text-muted-foreground">InvoxelAI</p>
          <h1 className="text-lg font-extrabold">GST OCR</h1>
        </div>
      </div>
      <nav className="grid grid-cols-2 gap-2 p-3 md:grid-cols-1">
        {nav.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-2 rounded-xl px-3 py-2 text-sm",
                active ? "bg-primary text-primary-foreground" : "hover:bg-muted"
              )}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
