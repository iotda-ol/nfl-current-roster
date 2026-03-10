from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import draft, free_agents, rosters, teams
from app.core.config import settings
from app.db.session import engine
from app.models import base  # noqa: F401 – ensures models are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (Alembic handles migrations in production)
    base.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="NFL Data Dashboard API",
    description="REST API for NFL teams, rosters, free agents, and draft prospects.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(rosters.router, prefix="/api/rosters", tags=["Rosters"])
app.include_router(free_agents.router, prefix="/api/free-agents", tags=["Free Agents"])
app.include_router(draft.router, prefix="/api/draft", tags=["Draft"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
