"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { authApi } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@invoxel.ai");
  const [password, setPassword] = useState("Admin@1234");
  const [loading, setLoading] = useState(false);

  return (
    <main className="mx-auto flex min-h-screen max-w-md items-center p-6">
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-2xl">Sign in</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <Input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
          <Button
            className="w-full"
            disabled={loading}
            onClick={async () => {
              setLoading(true);
              try {
                const res = await authApi.login({ email, password });
                localStorage.setItem("token", res.access_token);
                router.push("/dashboard");
              } finally {
                setLoading(false);
              }
            }}
          >
            {loading ? "Signing in..." : "Sign in"}
          </Button>
          <p className="text-sm text-muted-foreground">
            New user? <Link className="text-primary" href="/register">Create account</Link>
          </p>
        </CardContent>
      </Card>
    </main>
  );
}
