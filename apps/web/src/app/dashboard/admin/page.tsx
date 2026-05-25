"use client";

import { useEffect, useState } from "react";
import { Users, FolderOpen, Activity, Cpu } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { StatCard } from "@/components/dashboard/stat-card";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { api } from "@/lib/api";
import type { DashboardStats } from "@sanson/types";

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    api.getAnalytics().then((res) => {
      if (res.data) setStats(res.data);
    }).catch(() => {});
  }, []);

  return (
    <DashboardShell
      role="admin"
      title="Admin Console"
      subtitle="System management, analytics, and security monitoring"
    >
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Users" value={stats?.total_users ?? "—"} icon={Users} />
        <StatCard title="Total Cases" value={stats?.total_cases ?? "—"} icon={FolderOpen} />
        <StatCard title="Active Cases" value={stats?.active_cases ?? "—"} icon={Activity} />
        <StatCard title="AI Tokens Used" value={stats?.ai_usage_tokens ?? 0} icon={Cpu} />
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        {[
          { title: "User Management", desc: "Manage users, roles, and permissions" },
          { title: "Audit Logs", desc: "Track all system activity and access" },
          { title: "Security Monitoring", desc: "Monitor authentication and API security" },
        ].map((item) => (
          <Card key={item.title}>
            <CardHeader>
              <CardTitle>{item.title}</CardTitle>
              <CardDescription>{item.desc}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </div>
    </DashboardShell>
  );
}
