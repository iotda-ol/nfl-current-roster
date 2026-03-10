from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.player import PlayerRead
from app.services.roster_service import (
    CURRENT_SEASON,
    get_player,
    get_roster_by_team,
    sync_rosters,
)

router = APIRouter()


@router.get("/{team_abbr}", response_model=List[PlayerRead], summary="Get roster for a team")
def get_team_roster(
    team_abbr: str,
    season: int = CURRENT_SEASON,
    db: Session = Depends(get_db),
):
    """Return the roster for the given team abbreviation and season."""
    players = get_roster_by_team(db, team_abbr, season)
    return players


@router.get("/player/{player_id}", response_model=PlayerRead, summary="Get player details")
def get_player_details(player_id: str, db: Session = Depends(get_db)):
    player = get_player(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail=f"Player '{player_id}' not found.")
    return player


@router.post("/sync", summary="Sync roster data from nfl_data_py")
def sync_rosters_endpoint(season: int = CURRENT_SEASON, db: Session = Depends(get_db)):
    """Trigger a manual roster sync for the given season."""
    count = sync_rosters(db, season)
    return {"synced": count, "season": season}
