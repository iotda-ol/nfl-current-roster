"""
Unit tests for the NFL Dashboard backend.

These tests use an in-memory SQLite database so they work without a live
PostgreSQL instance (or internet access to nfl_data_py).
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import get_db
from app.main import app
from app.models.base import Base
from app.models.draft_prospect import DraftProspect
from app.models.free_agent import FreeAgent
from app.models.player import Player
from app.models.team import Team

# ---------------------------------------------------------------------------
# Test database setup (SQLite in-memory)
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Helper: seed data
# ---------------------------------------------------------------------------

def _seed_team(db):
    team = Team(team_abbr="NE", team_name="New England Patriots", team_conf="AFC", team_division="AFC East")
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def _seed_player(db):
    player = Player(
        player_id="00-0123456",
        full_name="Tom Brady",
        position="QB",
        team="NE",
        season=2024,
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def _seed_free_agent(db):
    fa = FreeAgent(
        player_id="fa-001",
        full_name="John Doe",
        position="WR",
        last_team="NE",
    )
    db.add(fa)
    db.commit()
    db.refresh(fa)
    return fa


def _seed_draft_prospect(db):
    prospect = DraftProspect(
        pick_number=1,
        round_number=1,
        pick_in_round=1,
        player_name="Cam Ward",
        position="QB",
        college="Miami (FL)",
        year=2026,
    )
    db.add(prospect)
    db.commit()
    db.refresh(prospect)
    return prospect


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Teams endpoints
# ---------------------------------------------------------------------------

def test_list_teams_empty(client):
    resp = client.get("/api/teams/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_teams_with_data(client, db):
    _seed_team(db)
    resp = client.get("/api/teams/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["team_abbr"] == "NE"
    assert data[0]["team_name"] == "New England Patriots"


def test_get_team_found(client, db):
    _seed_team(db)
    resp = client.get("/api/teams/NE")
    assert resp.status_code == 200
    assert resp.json()["team_abbr"] == "NE"


def test_get_team_not_found(client):
    resp = client.get("/api/teams/XX")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Rosters endpoints
# ---------------------------------------------------------------------------

def test_get_roster_empty(client):
    resp = client.get("/api/rosters/NE")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_roster_with_data(client, db):
    _seed_player(db)
    resp = client.get("/api/rosters/NE?season=2024")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Tom Brady"


def test_get_player_not_found(client):
    resp = client.get("/api/rosters/player/nonexistent-id")
    assert resp.status_code == 404


def test_get_player_found(client, db):
    _seed_player(db)
    resp = client.get("/api/rosters/player/00-0123456")
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Tom Brady"


def test_search_players_found(client, db):
    _seed_player(db)
    resp = client.get("/api/rosters/search?q=Tom")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Tom Brady"


def test_search_players_no_results(client, db):
    _seed_player(db)
    resp = client.get("/api/rosters/search?q=nobody")
    assert resp.status_code == 200
    assert resp.json() == []


def test_search_players_query_too_short(client):
    resp = client.get("/api/rosters/search?q=T")
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Free agents endpoints
# ---------------------------------------------------------------------------

def test_list_free_agents_empty(client):
    resp = client.get("/api/free-agents/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_free_agents_with_data(client, db):
    _seed_free_agent(db)
    resp = client.get("/api/free-agents/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "John Doe"


def test_free_agents_position_filter(client, db):
    _seed_free_agent(db)
    resp = client.get("/api/free-agents/?position=QB")
    assert resp.status_code == 200
    assert resp.json() == []

    resp2 = client.get("/api/free-agents/?position=WR")
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1


def test_free_agents_search(client, db):
    _seed_free_agent(db)
    resp = client.get("/api/free-agents/?search=john")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp2 = client.get("/api/free-agents/?search=nobody")
    assert resp2.status_code == 200
    assert resp2.json() == []


# ---------------------------------------------------------------------------
# Draft endpoints
# ---------------------------------------------------------------------------

def test_list_draft_prospects_empty(client):
    resp = client.get("/api/draft/prospects")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_draft_prospects_with_data(client, db):
    _seed_draft_prospect(db)
    resp = client.get("/api/draft/prospects?year=2026")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["player_name"] == "Cam Ward"
    assert data[0]["pick_number"] == 1


def test_draft_prospects_position_filter(client, db):
    _seed_draft_prospect(db)
    resp = client.get("/api/draft/prospects?year=2026&position=QB")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp2 = client.get("/api/draft/prospects?year=2026&position=WR")
    assert resp2.status_code == 200
    assert resp2.json() == []


def test_draft_prospects_round_filter(client, db):
    _seed_draft_prospect(db)
    resp = client.get("/api/draft/prospects?year=2026&round_number=1")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp2 = client.get("/api/draft/prospects?year=2026&round_number=2")
    assert resp2.status_code == 200
    assert resp2.json() == []


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

def test_team_schema():
    from app.schemas.team import TeamRead
    team = TeamRead(id=1, team_abbr="NE", team_name="Patriots")
    assert team.team_abbr == "NE"


def test_player_schema():
    from app.schemas.player import PlayerRead
    player = PlayerRead(id=1, player_id="p1", full_name="Test Player", position="QB")
    assert player.position == "QB"


def test_free_agent_schema():
    from app.schemas.free_agent import FreeAgentRead
    fa = FreeAgentRead(id=1, player_id="fa1", full_name="Test FA", position="WR")
    assert fa.position == "WR"


def test_free_agent_age_field(db):
    """Free agents with a birth_date should have age populated after sync."""
    from app.services.free_agents_service import _calc_age
    import datetime
    today = datetime.date.today()
    birth = today.replace(year=today.year - 30)
    assert _calc_age(birth.isoformat()) == 30
    assert _calc_age(None) is None
    assert _calc_age("invalid-date") is None


def test_draft_prospect_schema():
    from app.schemas.draft_prospect import DraftProspectRead
    dp = DraftProspectRead(id=1, pick_number=1, round_number=1, player_name="Test Player")
    assert dp.pick_number == 1
    assert dp.stats == {}
