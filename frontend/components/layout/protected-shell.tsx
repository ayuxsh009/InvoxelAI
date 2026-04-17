"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";

export function ProtectedShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, [router]);

  return (
    <div className="min-h-screen md:flex">
      <Sidebar />
      <div className="flex-1">
        <Topbar />
        <main className="p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
