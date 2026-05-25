import type { APIResponse, AuthTokens, User } from "@sanson/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8100";
const API_VERSION = "v1";

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = `${API_URL}/api/${API_VERSION}`;
  }

  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    const token = this.getToken();
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || "Request failed");
    }

    return data;
  }

  async login(email: string, password: string) {
    return this.request<{ user: User; tokens: AuthTokens }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  async register(payload: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    phone?: string;
  }) {
    return this.request<{ user: User; tokens: AuthTokens }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ ...payload, role: "client" }),
    });
  }

  async getMe() {
    return this.request<User>("/auth/me");
  }

  async refreshToken(refreshToken: string) {
    return this.request<AuthTokens>("/auth/refresh", {
      method: "POST",
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
  }

  async getCases() {
    return this.request<import("@sanson/types").Case[]>("/cases");
  }

  async proceedWithLegalAction(caseId: string) {
    return this.request<import("@sanson/types").Case>("/cases/proceed", {
      method: "POST",
      body: JSON.stringify({ case_id: caseId }),
    });
  }

  async getNotifications(unreadOnly = false) {
    return this.request<import("@sanson/types").Notification[]>(
      `/notifications?unread_only=${unreadOnly}`
    );
  }

  async getAnalytics() {
    return this.request<import("@sanson/types").DashboardStats>("/analytics/dashboard");
  }

  getWsUrl(token: string): string {
    const wsBase = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8100";
    return `${wsBase}/ws/${token}`;
  }
}

export const api = new ApiClient();
