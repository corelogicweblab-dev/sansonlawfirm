# SANSON Legal OS

AI-powered centralized enterprise legal management ecosystem for **SANSON Law Firm**.

## Architecture

```
/apps/web       → Next.js (Netlify)
/backend        → FastAPI (Render)
/mobile         → Expo (Phase 4)
/packages
  /types        → Shared TypeScript types
  /shared       → Shared constants & helpers
  /utils        → Utility functions
/infrastructure
  /docker       → Docker Compose (Postgres, Redis, Qdrant, MinIO)
  /nginx        → Reverse proxy configuration
```

## Business Logic

**AI-first legal triage** — clients interact with the AI legal assistant first (free consultation layer). Booking is NOT for consultation. Clients only formally proceed with legal services when they choose "Proceed with Legal Action."

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web | Next.js, TypeScript, Tailwind CSS |
| Mobile | React Native (Expo) |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Realtime | Redis Pub/Sub + WebSockets |
| AI | OpenAI API (+ optional Ollama) |
| Vector DB | Qdrant |
| Storage | S3-compatible (MinIO) |
| Auth | JWT + Refresh Tokens + RBAC |

## Quick Start

### 1. Environment

```bash
cp .env.example .env
# Edit .env with your secrets (JWT_SECRET, OPENAI_API_KEY, etc.)
```

### 2. Infrastructure (Docker)

```bash
npm run docker:up
```

Starts: PostgreSQL, Redis, Qdrant, MinIO

### 3. Backend

> **Requires Python 3.12** (recommended). Python 3.14 may fail on some native dependencies — use Docker or pyenv for 3.12.

```bash
cd backend
python3.12 -m venv .venv    # use Python 3.12
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8100
```

API docs: http://localhost:8100/api/v1/docs

### 4. Web App

```bash
npm install                 # from monorepo root
npm run dev:web
```

Web app: **http://localhost:3100**

### Test URLs (alternate ports — hindi na kailangan ng 3000/8000)

| Service | URL |
|---------|-----|
| **Web app** | http://localhost:3100 |
| **API** | http://localhost:8100 |
| **API docs (Swagger)** | http://localhost:8100/api/v1/docs |
| **Health check** | http://localhost:8100/api/v1/health |
| **PostgreSQL** | `localhost:5433` |
| **Redis** | `localhost:6380` |
| **MinIO console** | http://localhost:9011 |

Kung may conflict pa rin, baguhin ang `WEB_PORT` / `API_PORT` sa `.env` file.

### Default Admin

- Email: `admin@sansonlaw.ph`
- Password: `Admin@123456` (change immediately in production)

## User Roles & Dashboards

| Role | Dashboard Path |
|------|---------------|
| Client | `/dashboard/client` |
| Lawyer | `/dashboard/lawyer` |
| Paralegal | `/dashboard/paralegal` |
| Admin | `/dashboard/admin` |

## API Modules

- `POST /api/v1/auth/register` — Client registration
- `POST /api/v1/auth/login` — Login
- `POST /api/v1/auth/refresh` — Token refresh
- `GET  /api/v1/auth/me` — Current user
- `GET  /api/v1/cases` — List cases (role-filtered)
- `POST /api/v1/cases/proceed` — Client proceeds with legal action
- `GET  /api/v1/notifications` — Notifications
- `GET  /api/v1/analytics/dashboard` — Admin analytics
- `WS   /ws/{token}` — Realtime WebSocket

## Development Phases

- [x] **Phase 1** — Project setup, auth, roles, database, dashboards
- [ ] **Phase 2** — AI chatbot, case system, uploads, notifications
- [ ] **Phase 3** — AI summaries, smart search, OCR, vector search
- [ ] **Phase 4** — Mobile app, realtime sync, performance
- [ ] **Phase 5** — Security hardening, DevOps, production deployment

## Theme

Premium black backgrounds · Modern pink accents · Glassmorphism · Neon pink highlights

## Production URLs

| Service | URL |
|---------|-----|
| **API (Render)** | https://sansonlawfirm.onrender.com |
| **Database (Supabase)** | https://zoauzxvkjthgokjurkze.supabase.co |
| **Web (Netlify)** | Your Netlify site (e.g. `https://sansonlawfirm.netlify.app`) |

## Deploy

**[DEPLOYMENT.md](DEPLOYMENT.md)** — Render (Docker API) · Netlify (Web) · Supabase (DB)

Render uses **Docker** (`backend/Dockerfile`). Never run `npm` on Render.

## License

Proprietary — SANSON Law Firm
