# SANSON Legal OS — Render API

**Production API:** https://sansonlawfirm.onrender.com

## Required environment variables (Render Dashboard)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Supabase URI — see [SUPABASE.md](./SUPABASE.md) |
| `DATABASE_SSL` | `true` (required for Supabase) |
| `SUPABASE_URL` | `https://zoauzxvkjthgokjurkze.supabase.co` |
| `JWT_SECRET` | Long random string (32+ chars) |
| `CORS_ORIGINS` | Comma-separated frontend URLs |

### Example `CORS_ORIGINS`

```
http://localhost:3100,https://sansonlawfirm.netlify.app,https://YOUR-NETLIFY-SITE.netlify.app
```

## Health check

- Root: https://sansonlawfirm.onrender.com/
- API: https://sansonlawfirm.onrender.com/api/v1/health
- Docs: https://sansonlawfirm.onrender.com/api/v1/docs

## Deploy from GitHub

1. Render Dashboard → **New** → **Blueprint** (or Web Service)
2. Connect `corelogicweblab-dev/sansonlawfirm`
3. Uses `render.yaml` — **Root Directory:** `apps/backend`
4. Add Postgres database and link `DATABASE_URL`

## Free tier note

Render free services **spin down** after inactivity. First request may take 30–60 seconds (cold start).

## Netlify ↔ Render

Frontend on Netlify must use:

```
NEXT_PUBLIC_API_URL=https://sansonlawfirm.onrender.com
NEXT_PUBLIC_WS_URL=wss://sansonlawfirm.onrender.com
```

Configured in `netlify.toml` — redeploy Netlify after pushing.
