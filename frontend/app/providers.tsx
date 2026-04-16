"use client";

import { ThemeProvider } from "@/components/layout/theme-provider";
import { AppToaster } from "@/components/ui/toaster";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
      <AppToaster />
    </ThemeProvider>
  );
}
