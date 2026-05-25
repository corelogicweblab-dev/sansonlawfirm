# Deploy SANSON Legal OS — GitHub → Netlify

## 1. Connect GitHub to Netlify

1. Log in to [Netlify](https://app.netlify.com/)
2. **Add new site** → **Import an existing project**
3. Choose **GitHub** → authorize → select **`corelogicweblab-dev/sansonlawfirm`**
4. Netlify reads `netlify.toml` from the repo automatically

## 2. Build settings (auto from `netlify.toml`)

| Setting | Value |
|---------|--------|
| Branch | `main` |
| Build command | `npm ci && npm run build --workspace=@sanson/web` |
| Publish | Handled by `@netlify/plugin-nextjs` |
| Node | 22 |

**Base directory** must be empty in Netlify UI (let `netlify.toml` set `base = "apps/web"`).

If UI shows `apps/mobile`, change it to **blank** or `apps/web` — wrong base causes the `apps/mobile/dist` error.

## 3. Environment variables (required)

In **Site configuration → Environment variables**, add:

| Variable | Value | Notes |
|----------|-------|--------|
| `NEXT_PUBLIC_API_URL` | `https://sansonlawfirm.onrender.com` | Set in `netlify.toml` |
| `NEXT_PUBLIC_WS_URL` | `wss://sansonlawfirm.onrender.com` | Set in `netlify.toml` |
| `NEXT_PUBLIC_APP_NAME` | `SANSON Legal OS` | Optional |

> Already configured in `netlify.toml`. Override in Netlify UI if needed.

**Production API:** https://sansonlawfirm.onrender.com

## 4. Deploy

Click **Deploy site**. Each push to `main` triggers a new deploy.

## 5. Custom domain (optional)

**Domain management** → Add custom domain → follow DNS instructions.

## 6. CORS on backend

Add your Netlify URL to backend `CORS_ORIGINS`, e.g.:

```
https://sansonlawfirm.netlify.app,https://your-custom-domain.com
```

## Troubleshooting

- **Build fails on workspaces** — Ensure build runs from repo root (not `apps/web` only).
- **API calls fail** — Check `NEXT_PUBLIC_API_URL` and backend CORS.
- **Blank page** — Check Netlify deploy log; confirm `@netlify/plugin-nextjs` ran.
