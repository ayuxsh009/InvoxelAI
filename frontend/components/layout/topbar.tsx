"use client";

import { LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Button } from "@/components/ui/button";

export function Topbar() {
  const router = useRouter();

  return (
    <header className="flex items-center justify-between border-b border-border p-4">
      <div>
        <h2 className="text-xl font-bold">Invoice Intelligence Center</h2>
        <p className="text-sm text-muted-foreground">Track extraction quality, GST accuracy, and compliance.</p>
      </div>
      <div className="flex items-center gap-2">
        <ThemeToggle />
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            localStorage.removeItem("token");
            router.push("/login");
          }}
          className="gap-2"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </Button>
      </div>
    </header>
  );
}
