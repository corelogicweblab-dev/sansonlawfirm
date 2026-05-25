import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/register"];
const AUTH_PATHS = ["/login", "/register"];

const ROLE_PATHS: Record<string, string> = {
  client: "/dashboard/client",
  lawyer: "/dashboard/lawyer",
  paralegal: "/dashboard/paralegal",
  admin: "/dashboard/admin",
};

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.includes(".")
  ) {
    return NextResponse.next();
  }

  const isPublic = PUBLIC_PATHS.some(
    (p) => pathname === p || pathname.startsWith(p + "/")
  );
  const isAuthPage = AUTH_PATHS.includes(pathname);
  const isDashboard = pathname.startsWith("/dashboard");

  // Client-side auth is handled via localStorage — middleware allows through
  // Full server-side JWT validation will be added in Phase 5
  if (isDashboard || isPublic || isAuthPage) {
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
