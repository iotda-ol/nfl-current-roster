# 🏈 NFL Data Dashboard

A full-stack application for exploring real-time NFL roster data, current free agents, and the upcoming 2026 NFL Draft.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12+, FastAPI, SQLAlchemy 2, PostgreSQL, Alembic |
| **Data Ingestion** | nfl_data_py, BeautifulSoup4 |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, Shadcn/UI |
| **Data Fetching** | TanStack Query (React Query) |
| **Infrastructure** | Docker, Docker Compose |

---

## Project Structure

```
nfl-current-roster/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/       # FastAPI route handlers
│   │   │   ├── teams.py         # GET /api/teams
│   │   │   ├── rosters.py       # GET /api/rosters/{team_abbr}
│   │   │   ├── free_agents.py   # GET /api/free-agents
│   │   │   └── draft.py         # GET /api/draft/prospects
│   │   ├── core/
│   │   │   └── config.py        # Pydantic Settings
│   │   ├── db/
│   │   │   └── session.py       # SQLAlchemy engine & session
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── team.py
│   │   │   ├── player.py
│   │   │   ├── free_agent.py
│   │   │   └── draft_prospect.py
│   │   ├── schemas/             # Pydantic schemas (type-safe API contracts)
│   │   │   ├── team.py
│   │   │   ├── player.py
│   │   │   ├── free_agent.py
│   │   │   └── draft_prospect.py
│   │   ├── services/            # Data ingestion & business logic
│   │   │   ├── teams_service.py
│   │   │   ├── roster_service.py
│   │   │   ├── free_agents_service.py
│   │   │   └── draft_service.py
│   │   └── main.py              # FastAPI application entry point
│   ├── tests/
│   │   └── test_api.py          # Pytest API tests (SQLite in-memory)
│   ├── sync_db.py               # Standalone DB sync script
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout with sidebar
│   │   │   ├── page.tsx         # Home / dashboard overview
│   │   │   ├── teams/[abbr]/    # Team roster page
│   │   │   ├── free-agents/     # Free agency table
│   │   │   └── draft-room/      # 2026 Draft Room
│   │   ├── components/
│   │   │   ├── layout/          # Sidebar, QueryProvider
│   │   │   └── ui/              # Reusable UI components
│   │   ├── hooks/
│   │   │   └── useNflData.ts    # TanStack Query hooks
│   │   ├── lib/
│   │   │   ├── api.ts           # Typed fetch helpers
│   │   │   └── utils.ts
│   │   └── types/
│   │       └── index.ts         # TypeScript types mirroring Pydantic models
│   ├── Dockerfile
│   └── next.config.mjs
└── docker-compose.yml
```

---

## Quick Start with Docker Compose

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone and start

```bash
git clone https://github.com/iotda-ol/nfl-current-roster.git
cd nfl-current-roster
docker compose up --build
```

This will:
1. Start a **PostgreSQL** database
2. Start the **FastAPI** backend on `http://localhost:8000`
3. Run the **sync** job to populate the database with teams, rosters, free agents, and draft prospects
4. Start the **Next.js** frontend on `http://localhost:3000`

### 2. Open the app

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (Redoc) | http://localhost:8000/redoc |

---

## Local Development (without Docker)

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your local DATABASE_URL

# Start the API server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy and configure environment
cp .env.local.example .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start dev server
npm run dev
```

---

## Database Synchronization

The `sync_db.py` script populates the PostgreSQL cache from upstream data sources.

```bash
cd backend

# Sync everything
python sync_db.py

# Sync only specific resources
python sync_db.py --teams
python sync_db.py --rosters
python sync_db.py --free-agents
python sync_db.py --draft
```

**Data Sources:**
| Resource | Source |
|----------|--------|
| Teams | `nfl_data_py.import_team_desc()` |
| Rosters | `nfl_data_py.import_rosters()` |
| Free Agents | `nfl_data_py` roster data (status=FA) + web scraping (Spotrac) |
| Draft Prospects | Web scraping (The Draft Network) + curated seed data |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/teams/` | List all NFL teams |
| `GET` | `/api/teams/{abbr}` | Get team by abbreviation |
| `POST` | `/api/teams/sync` | Sync team data |
| `GET` | `/api/rosters/{team_abbr}` | Get team roster (optional `?season=2024`) |
| `GET` | `/api/rosters/player/{player_id}` | Get player details |
| `POST` | `/api/rosters/sync` | Sync roster data |
| `GET` | `/api/free-agents/` | List free agents (optional `?position=QB&search=brady`) |
| `POST` | `/api/free-agents/sync` | Sync free agent data |
| `GET` | `/api/draft/prospects` | List draft prospects (optional `?year=2026&round_number=1&position=QB`) |
| `POST` | `/api/draft/sync` | Sync draft prospect data |
| `GET` | `/health` | Health check |

---

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

Tests use an in-memory SQLite database — no PostgreSQL required.

---

## Type Safety

The TypeScript types in `frontend/src/types/index.ts` mirror the Pydantic models in `backend/app/schemas/`. The TanStack Query hooks in `frontend/src/hooks/useNflData.ts` are fully typed end-to-end, ensuring the frontend and backend stay in sync.

---

## Frontend Pages

| Page | Path | Description |
|------|------|-------------|
| Dashboard | `/` | Overview with navigation cards |
| Team Roster | `/teams/[abbr]` | Roster grouped by position |
| Free Agents | `/free-agents` | Searchable table with position filter |
| Draft Room | `/draft-room` | 2026 draft order with grades and filters |
