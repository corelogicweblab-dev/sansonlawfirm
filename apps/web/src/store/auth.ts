import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AuthTokens, User } from "@sanson/types";
import { ROLE_DASHBOARD_PATHS } from "@sanson/shared";

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  setAuth: (user: User, tokens: AuthTokens) => void;
  clearAuth: () => void;
  getDashboardPath: () => string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      setAuth: (user, tokens) => {
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", tokens.access_token);
          localStorage.setItem("refresh_token", tokens.refresh_token);
        }
        set({ user, tokens, isAuthenticated: true });
      },
      clearAuth: () => {
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
        set({ user: null, tokens: null, isAuthenticated: false });
      },
      getDashboardPath: () => {
        const role = get().user?.role;
        return role ? ROLE_DASHBOARD_PATHS[role] : "/login";
      },
    }),
    { name: "sanson-auth" }
  )
);
