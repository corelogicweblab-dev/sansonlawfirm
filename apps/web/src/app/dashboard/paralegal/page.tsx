"use client";

import { ClipboardList, FolderOpen, CheckSquare, Users } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { StatCard } from "@/components/dashboard/stat-card";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function ParalegalDashboard() {
  return (
    <DashboardShell
      role="paralegal"
      title="Paralegal Dashboard"
      subtitle="Intake review, evidence organization, and case preparation"
    >
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Intake Queue" value={0} icon={ClipboardList} change="Awaiting review" />
        <StatCard title="Active Cases" value={0} icon={FolderOpen} />
        <StatCard title="Pending Tasks" value={0} icon={CheckSquare} />
        <StatCard title="Lawyer Coordination" value={0} icon={Users} />
      </div>

      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Intake Review Queue</CardTitle>
          <CardDescription>
            Cases where clients have formally proceeded with legal services appear here
            for intake review and evidence organization.
          </CardDescription>
        </CardHeader>
      </Card>
    </DashboardShell>
  );
}
