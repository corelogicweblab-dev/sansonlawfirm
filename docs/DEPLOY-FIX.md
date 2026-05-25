# Deploy Fix (structural — May 2026)

## What changed in the repo

| Before | After |
|--------|--------|
| `apps/backend` | **`backend/`** (Render expects this) |
| `apps/mobile` in monorepo | **`mobile/`** (not deployed to Netlify) |
| Netlify built wrong package | **`base = apps/web`** only |

---

## Render

**Root Directory:** `backend` (matches folder name now)

1. Render → **sansonlawfirm** → **Settings** → Root Directory = `backend`
2. Environment: `DATABASE_URL`, `DATABASE_SSL=true`, `JWT_SECRET`
3. **Manual Deploy**

Test: https://sansonlawfirm.onrender.com/api/v1/health

---

## Netlify

1. **Site configuration** → **Build & deploy** → **Build settings**
2. Click **Manage** or **Edit** → **Clear ALL overrides:**
   - Base directory: **empty** (netlify.toml sets `apps/web`)
   - Build command: **empty**
   - Publish directory: **empty**
3. **Deploys** → **Trigger deploy** → **Clear cache and deploy site**

Test: open your `*.netlify.app` URL

---

## Still failing?

Delete the Netlify site and re-import from GitHub (fresh settings), or send a screenshot of **Build settings** page.
