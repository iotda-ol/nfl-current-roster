from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.free_agent import FreeAgentRead
from app.services.free_agents_service import get_free_agents, sync_free_agents

router = APIRouter()


@router.get("/", response_model=List[FreeAgentRead], summary="List current free agents")
def list_free_agents(
    position: Optional[str] = Query(None, description="Filter by position (e.g. QB, WR)"),
    search: Optional[str] = Query(None, description="Search by player name"),
    db: Session = Depends(get_db),
):
    """Return the list of current free agents, with optional filtering."""
    return get_free_agents(db, position=position, search=search)


@router.post("/sync", summary="Sync free agent data")
def sync_free_agents_endpoint(db: Session = Depends(get_db)):
    """Trigger a manual sync of free agent data."""
    count = sync_free_agents(db)
    return {"synced": count}
