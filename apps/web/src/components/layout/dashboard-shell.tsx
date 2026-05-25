"use client";

import { Bell } from "lucide-react";
import { Sidebar } from "./sidebar";
import type { UserRole } from "@sanson/types";

interface DashboardShellProps {
  role: UserRole;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
}

export function DashboardShell({
  role,
  title,
  subtitle,
  children,
  actions,
}: DashboardShellProps) {
  return (
    <div className="min-h-screen bg-[var(--background)]">
      <Sidebar role={role} />
      <div className="ml-64 min-h-screen">
        <header className="sticky top-0 z-30 flex items-center justify-between border-b border-pink-500/10 bg-[var(--sidebar)]/80 px-8 py-4 backdrop-blur-xl">
          <div>
            <h1 className="text-xl font-bold text-foreground">{title}</h1>
            {subtitle && <p className="text-sm text-[var(--muted)]">{subtitle}</p>}
          </div>
          <div className="flex items-center gap-4">
            {actions}
            <button className="relative rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-white/5 hover:text-pink-400">
              <Bell className="h-5 w-5" />
              <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-pink-500 animate-pulse-pink" />
            </button>
          </div>
        </header>
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
}
