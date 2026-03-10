from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.team import TeamRead
from app.services.teams_service import get_all_teams, get_team, sync_teams

router = APIRouter()


@router.get("/", response_model=List[TeamRead], summary="List all NFL teams")
def list_teams(db: Session = Depends(get_db)):
    """Return all NFL teams ordered by name."""
    return get_all_teams(db)


@router.get("/{team_abbr}", response_model=TeamRead, summary="Get a team by abbreviation")
def read_team(team_abbr: str, db: Session = Depends(get_db)):
    """Return a single team by its abbreviation (e.g. `NE`, `KC`)."""
    team = get_team(db, team_abbr)
    if team is None:
        raise HTTPException(status_code=404, detail=f"Team '{team_abbr}' not found.")
    return team


@router.post("/sync", summary="Sync team data from nfl_data_py")
def sync_teams_endpoint(db: Session = Depends(get_db)):
    """Trigger a manual sync of team data from the upstream source."""
    count = sync_teams(db)
    return {"synced": count}
