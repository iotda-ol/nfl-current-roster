from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.draft_prospect import DraftProspectRead
from app.services.draft_service import DRAFT_YEAR, get_draft_prospects, sync_draft_prospects

router = APIRouter()


@router.get(
    "/prospects",
    response_model=List[DraftProspectRead],
    summary="List 2026 NFL Draft prospects",
)
def list_draft_prospects(
    year: int = Query(DRAFT_YEAR, description="Draft year"),
    round_number: Optional[int] = Query(None, description="Filter by round number"),
    position: Optional[str] = Query(None, description="Filter by position"),
    db: Session = Depends(get_db),
):
    """Return all draft prospects for the given year, sorted by pick order."""
    return get_draft_prospects(db, year=year, round_number=round_number, position=position)


@router.post("/sync", summary="Sync 2026 draft prospect data")
def sync_draft_endpoint(year: int = DRAFT_YEAR, db: Session = Depends(get_db)):
    """Trigger a manual sync of draft prospect data."""
    count = sync_draft_prospects(db, year=year)
    return {"synced": count, "year": year}
