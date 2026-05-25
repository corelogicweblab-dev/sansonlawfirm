# SANSON Legal OS — Deployment (final)

## Two platforms only

| What | Platform | URL |
|------|----------|-----|
| **Website (Next.js)** | **Netlify** | `https://YOUR-SITE.netlify.app` |
| **API (FastAPI)** | **Render (Docker)** | https://sansonlawfirm.onrender.com |

**Never deploy Next.js to Render.**  
**Never deploy Python API to Netlify.**

---

## Render — API (one-time setup)

### Option A: New service from Blueprint (recommended)

1. Render → **New** → **Blueprint**
2. Connect repo `corelogicweblab-dev/sansonlawfirm`
3. Apply `render.yaml` (Docker, `backend/Dockerfile`)
4. Add **`DATABASE_URL`** (Supabase) in Environment
5. Deploy

### Option B: Fix existing service

1. **Settings** → **General**
   - **Environment:** `Docker`
   - **Dockerfile Path:** `backend/Dockerfile`
   - **Docker Context:** `backend`
   - **Root Directory:** *(leave empty when using Docker)*
2. **Delete** from Build & Deploy:
   - `npm install`, `npm run build`, any Node build command
3. **Start Command:** *(empty — Dockerfile CMD runs `start.sh`)*
4. **Health Check Path:** `/api/v1/health`
5. **Environment variables:**

   | Key | Value |
   |-----|--------|
   | `DATABASE_URL` | Supabase URI (`postgresql+asyncpg://...`) |
   | `DATABASE_SSL` | `true` |
   | `JWT_SECRET` | long random string |
   | `CORS_ORIGINS` | your Netlify URL |

6. **Manual Deploy**

### Verify API

```text
https://sansonlawfirm.onrender.com/api/v1/health
```

---

## Netlify — Website (one-time setup)

1. Import GitHub repo
2. **Build settings — all empty** (use repo `netlify.toml`):
   - Base directory: *(empty)*
   - Build command: *(empty)*
   - Publish directory: *(empty)*
3. Env (or use `netlify.toml`):
   - `NEXT_PUBLIC_API_URL` = `https://sansonlawfirm.onrender.com`
   - `NEXT_PUBLIC_WS_URL` = `wss://sansonlawfirm.onrender.com`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = from Supabase
4. **Clear cache and deploy**

---

## Database (Supabase)

1. SQL Editor → run `infrastructure/docker/init.sql`
2. Copy connection string → Render `DATABASE_URL`

---

## If Render log shows Next.js / npm

Wrong service or wrong settings. You are deploying the **web app** on Render.

Fix: switch to **Docker** + `backend/Dockerfile` (see above), or delete service and recreate from Blueprint.
