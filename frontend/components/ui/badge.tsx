import { cn } from "@/lib/utils";

export function Badge({ className, children }: { className?: string; children: React.ReactNode }) {
  return <span className={cn("rounded-full border border-border px-2.5 py-1 text-xs font-medium", className)}>{children}</span>;
}
