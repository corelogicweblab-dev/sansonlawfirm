export type UserRole = "client" | "lawyer" | "paralegal" | "admin";

export type CaseCategory =
  | "criminal"
  | "civil"
  | "labor"
  | "family"
  | "cybercrime"
  | "administrative"
  | "other";

export type CasePriority = "low" | "medium" | "high" | "urgent";

export type CaseStatusName =
  | "ai_intake"
  | "pending_review"
  | "under_review"
  | "active"
  | "on_hold"
  | "closed"
  | "declined";

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone?: string;
  avatar_url?: string;
  role: UserRole;
  role_display: string;
  is_active: boolean;
  is_verified: boolean;
  locale: string;
  last_login_at?: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface APIResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}

export interface Case {
  id: string;
  case_number: string;
  title: string;
  description?: string;
  category?: CaseCategory;
  priority: CasePriority;
  status_name: CaseStatusName;
  status_display: string;
  intake_summary?: string;
  is_actionable?: boolean;
  formally_proceeded: boolean;
  proceeded_at?: string;
  client_id: string;
  assigned_lawyer_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: string;
  type: string;
  title: string;
  body?: string;
  data?: Record<string, unknown>;
  is_read: boolean;
  created_at: string;
}

export interface DashboardStats {
  total_cases: number;
  total_users: number;
  active_cases: number;
  pending_reviews: number;
  ai_usage_tokens: number;
}
