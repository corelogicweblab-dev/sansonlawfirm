import type { UserRole } from "@sanson/types";

export const ROLE_DASHBOARD_PATHS: Record<UserRole, string> = {
  client: "/dashboard/client",
  lawyer: "/dashboard/lawyer",
  paralegal: "/dashboard/paralegal",
  admin: "/dashboard/admin",
};

export const ROLE_LABELS: Record<UserRole, string> = {
  client: "Client Portal",
  lawyer: "Lawyer Dashboard",
  paralegal: "Paralegal Dashboard",
  admin: "Admin Console",
};

export function formatCaseNumber(num: string): string {
  return num.toUpperCase();
}

export function getInitials(firstName: string, lastName: string): string {
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
}
