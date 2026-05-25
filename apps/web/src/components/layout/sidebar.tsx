"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  MessageSquare,
  FolderOpen,
  Bell,
  Users,
  Settings,
  Search,
  FileText,
  BarChart3,
  Shield,
  ClipboardList,
  LogOut,
  Scale,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";
import type { UserRole } from "@sanson/types";
import { getInitials } from "@sanson/shared";

interface NavItem {
  label: string;
  href: string;
  icon: React.ElementType;
}

const NAV_CONFIG: Record<UserRole, NavItem[]> = {
  client: [
    { label: "Dashboard", href: "/dashboard/client", icon: LayoutDashboard },
    { label: "AI Legal Chat", href: "/dashboard/client/chat", icon: MessageSquare },
    { label: "My Cases", href: "/dashboard/client/cases", icon: FolderOpen },
    { label: "Documents", href: "/dashboard/client/documents", icon: FileText },
    { label: "Notifications", href: "/dashboard/client/notifications", icon: Bell },
  ],
  lawyer: [
    { label: "Dashboard", href: "/dashboard/lawyer", icon: LayoutDashboard },
    { label: "Cases", href: "/dashboard/lawyer/cases", icon: FolderOpen },
    { label: "Smart Search", href: "/dashboard/lawyer/search", icon: Search },
    { label: "AI Assistant", href: "/dashboard/lawyer/ai", icon: MessageSquare },
    { label: "Documents", href: "/dashboard/lawyer/documents", icon: FileText },
    { label: "Notifications", href: "/dashboard/lawyer/notifications", icon: Bell },
  ],
  paralegal: [
    { label: "Dashboard", href: "/dashboard/paralegal", icon: LayoutDashboard },
    { label: "Intake Queue", href: "/dashboard/paralegal/intake", icon: ClipboardList },
    { label: "Cases", href: "/dashboard/paralegal/cases", icon: FolderOpen },
    { label: "Tasks", href: "/dashboard/paralegal/tasks", icon: FileText },
    { label: "Notifications", href: "/dashboard/paralegal/notifications", icon: Bell },
  ],
  admin: [
    { label: "Dashboard", href: "/dashboard/admin", icon: LayoutDashboard },
    { label: "Users", href: "/dashboard/admin/users", icon: Users },
    { label: "Analytics", href: "/dashboard/admin/analytics", icon: BarChart3 },
    { label: "Audit Logs", href: "/dashboard/admin/audit", icon: Shield },
    { label: "Settings", href: "/dashboard/admin/settings", icon: Settings },
  ],
};

interface SidebarProps {
  role: UserRole;
}

export function Sidebar({ role }: SidebarProps) {
  const pathname = usePathname();
  const { user, clearAuth } = useAuthStore();
  const navItems = NAV_CONFIG[role];

  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-pink-500/10 bg-[var(--sidebar)]">
      <div className="flex items-center gap-3 border-b border-pink-500/10 px-6 py-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-pink-600 to-pink-400 shadow-lg shadow-pink-500/30">
          <Scale className="h-5 w-5 text-white" />
        </div>
        <div>
          <p className="text-sm font-bold tracking-wide text-foreground">SANSON</p>
          <p className="text-xs text-[var(--muted)]">Legal OS</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all duration-200",
                isActive
                  ? "bg-pink-500/15 text-pink-400 shadow-sm shadow-pink-500/10"
                  : "text-[var(--muted)] hover:bg-white/5 hover:text-foreground"
              )}
            >
              <Icon className={cn("h-4 w-4", isActive && "text-pink-400")} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-pink-500/10 p-4">
        <div className="mb-3 flex items-center gap-3 rounded-lg bg-white/5 px-3 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-pink-600 to-pink-400 text-xs font-bold text-white">
            {user ? getInitials(user.first_name, user.last_name) : "?"}
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="truncate text-sm font-medium">{user?.full_name}</p>
            <p className="truncate text-xs text-[var(--muted)] capitalize">{user?.role_display}</p>
          </div>
        </div>
        <button
          onClick={() => {
            clearAuth();
            window.location.href = "/login";
          }}
          className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-[var(--muted)] transition-colors hover:bg-red-500/10 hover:text-red-400"
        >
          <LogOut className="h-4 w-4" />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
