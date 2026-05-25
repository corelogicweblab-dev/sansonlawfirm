"use client";

import { FolderOpen, MessageSquare, Bell, FileText } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { StatCard } from "@/components/dashboard/stat-card";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function ClientDashboard() {
  return (
    <DashboardShell
      role="client"
      title="Client Portal"
      subtitle="Your AI-powered legal intake and case tracking"
    >
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Active Cases" value={0} icon={FolderOpen} change="No cases yet" />
        <StatCard title="AI Sessions" value={0} icon={MessageSquare} change="Start your first chat" />
        <StatCard title="Documents" value={0} icon={FileText} />
        <StatCard title="Notifications" value={0} icon={Bell} />
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Start AI Legal Consultation</CardTitle>
            <CardDescription>
              Our AI assistant is your first consultation layer — free and available 24/7.
              Describe your legal concern and we&apos;ll organize everything for our team.
            </CardDescription>
          </CardHeader>
          <Link href="/dashboard/client/chat">
            <Button>
              <MessageSquare className="h-4 w-4" />
              Open AI Legal Chat
            </Button>
          </Link>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Proceed with Legal Action</CardTitle>
            <CardDescription>
              When you&apos;re ready to formally engage our legal services, you can proceed
              from your case page. This is separate from the free AI consultation.
            </CardDescription>
          </CardHeader>
          <Link href="/dashboard/client/cases">
            <Button variant="secondary">View My Cases</Button>
          </Link>
        </Card>
      </div>
    </DashboardShell>
  );
}
