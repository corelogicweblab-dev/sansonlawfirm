"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Scale } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function RegisterPage() {
  const router = useRouter();
  const { setAuth } = useAuthStore();
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.register(form);
      if (res.data) {
        setAuth(res.data.user, res.data.tokens);
        router.push("/dashboard/client/chat");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--background)] p-4">
      <div className="relative w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-pink-600 to-pink-400">
            <Scale className="h-7 w-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold">Create Account</h1>
          <p className="text-sm text-[var(--muted)]">
            Start your free AI legal consultation
          </p>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Register</CardTitle>
            <CardDescription>
              Your first step is our AI intake — not a booking
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="mb-1.5 block text-sm text-[var(--muted)]">First Name</label>
                <Input
                  value={form.first_name}
                  onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="mb-1.5 block text-sm text-[var(--muted)]">Last Name</label>
                <Input
                  value={form.last_name}
                  onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                  required
                />
              </div>
            </div>
            <div>
              <label className="mb-1.5 block text-sm text-[var(--muted)]">Email</label>
              <Input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm text-[var(--muted)]">Phone (optional)</label>
              <Input
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm text-[var(--muted)]">Password</label>
              <Input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
                minLength={8}
              />
            </div>
            {error && (
              <p className="rounded-lg bg-red-500/10 px-3 py-2 text-sm text-red-400">{error}</p>
            )}
            <Button type="submit" className="w-full" loading={loading}>
              Create Account & Start AI Chat
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-[var(--muted)]">
            Already have an account?{" "}
            <Link href="/login" className="text-pink-400 hover:underline">
              Sign In
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
