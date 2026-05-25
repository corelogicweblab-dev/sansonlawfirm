"use client";

import { FolderOpen, AlertTriangle, Clock, CheckCircle } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { StatCard } from "@/components/dashboard/stat-card";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function LawyerDashboard() {
  return (
    <DashboardShell
      role="lawyer"
      title="Lawyer Dashboard"
      subtitle="Qualified cases and AI-assisted legal work"
    >
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Assigned Cases" value={0} icon={FolderOpen} />
        <StatCard title="Urgent Matters" value={0} icon={AlertTriangle} trend="neutral" />
        <StatCard title="Pending Reviews" value={0} icon={Clock} />
        <StatCard title="Active Cases" value={0} icon={CheckCircle} />
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Smart Search</CardTitle>
            <CardDescription>
              Semantic AI search across clients, cases, evidence, documents, and AI summaries.
            </CardDescription>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>AI Legal Assistant</CardTitle>
            <CardDescription>
              Draft documents, spot issues, and organize evidence with AI assistance.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </DashboardShell>
  );
}
