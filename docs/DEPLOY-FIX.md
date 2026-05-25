# Fix Render + Netlify Deploy Errors

## Render — `Root directory "backend" does not exist`

**Cause:** Dashboard Root Directory is set to `backend` but code is in `apps/backend`.

**Fix:**
1. [Render Dashboard](https://dashboard.render.com/) → **sansonlawfirm** → **Settings**
2. **Root Directory** → change to: `apps/backend`
3. **Save** → **Manual Deploy**

`render.yaml` already has `rootDir: apps/backend` — UI must match.

---

## Netlify — `turbo: command not found` / `@sanson/mobile`

**Cause:** Netlify UI overrides `netlify.toml` with wrong build command.

**Fix:**
1. [Netlify](https://app.netlify.com/) → your site → **Site configuration** → **Build & deploy**
2. **Build settings** → **Edit settings**
3. Set:
   - **Base directory:** *(leave empty)*
   - **Package directory:** `apps/web` *(if shown)*
   - **Build command:** *(empty — use repo `netlify.toml`)*
   - **Publish directory:** *(empty)*
4. **Save** → **Deploy site** → **Clear cache and deploy**

Correct build (from repo):

```bash
npm ci
npm run build:netlify
```

This builds **`@sanson/web`** only (not mobile).

---

## After both succeed

| Service | URL |
|---------|-----|
| Web | Your `*.netlify.app` URL |
| API | https://sansonlawfirm.onrender.com |
| DB | https://zoauzxvkjthgokjurkze.supabase.co |

Render env: `DATABASE_URL`, `DATABASE_SSL=true`, `JWT_SECRET`
