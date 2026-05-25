# Supabase — SANSON Legal OS Database

**Project URL:** https://zoauzxvkjthgokjurkze.supabase.co

## 1. Get database connection string

1. Open [Supabase Dashboard](https://supabase.com/dashboard/project/zoauzxvkjthgokjurkze)
2. **Project Settings** → **Database**
3. Copy **Connection string** → **URI** (mode: **Session** for FastAPI)
4. Replace `[YOUR-PASSWORD]` with your database password

Example (async FastAPI):

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@db.zoauzxvkjthgokjurkze.supabase.co:5432/postgres
DATABASE_SSL=true
```

> You can paste `postgresql://...` from Supabase — the backend auto-converts to `postgresql+asyncpg://`.

**Pooler (optional, high traffic):** use port `6543` and the pooler host from the dashboard.

## 2. Run database schema

1. Supabase → **SQL Editor** → **New query**
2. Paste contents of `infrastructure/docker/init.sql`
3. **Run**

This creates all tables, roles, case statuses, and the default admin user.

## 3. Render environment variables

In [Render](https://dashboard.render.com/) → **sansonlawfirm** → **Environment**:

| Variable | Value |
|----------|--------|
| `DATABASE_URL` | Your Supabase URI (`postgresql+asyncpg://...`) |
| `DATABASE_SSL` | `true` |
| `SUPABASE_URL` | `https://zoauzxvkjthgokjurkze.supabase.co` |
| `JWT_SECRET` | Strong random string |
| `CORS_ORIGINS` | Your Netlify URL + localhost |

Redeploy Render after saving.

## 4. API keys (optional — Phase 2+)

From Supabase → **Project Settings** → **API**:

| Variable | Use |
|----------|-----|
| `SUPABASE_ANON_KEY` | Future client features / storage |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-only admin tasks (never expose to browser) |

## 5. Verify

- https://sansonlawfirm.onrender.com/api/v1/health
- Login: `admin@sansonlaw.ph` / `Admin@123456` (after running `init.sql`)

## Local dev with Supabase

In project root `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@db.zoauzxvkjthgokjurkze.supabase.co:5432/postgres
DATABASE_SSL=true
SUPABASE_URL=https://zoauzxvkjthgokjurkze.supabase.co
```

Then run backend: `npm run dev:backend`
