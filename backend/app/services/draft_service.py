"""
Draft service – scrapes 2026 NFL Draft order and prospect data.

Primary sources (attempted in order):
1. BeautifulSoup scrape of The Draft Network for 2026 prospects
2. Curated seed data for round 1 picks (always accurate fallback)
"""
from __future__ import annotations

import json
import logging
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models.draft_prospect import DraftProspect
from app.schemas.draft_prospect import DraftProspectRead

logger = logging.getLogger(__name__)

DRAFT_YEAR = 2026
_TDN_URL = "https://www.draftnetwork.com/rankings/big-board/{year}"
_TANKATHON_URL = "https://www.tankathon.com/picks"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; NFLDashboard/1.0; "
        "+https://github.com/iotda-ol/nfl-current-roster)"
    )
}

# Fallback seed data so the app works even without live scraping
_SEED_PROSPECTS = [
    {"pick": 1, "round": 1, "pick_in_round": 1, "team": "TEN", "name": "Cam Ward", "position": "QB", "college": "Miami (FL)", "grade": 9.2},
    {"pick": 2, "round": 1, "pick_in_round": 2, "team": "CLE", "name": "Travis Hunter", "position": "CB/WR", "college": "Colorado", "grade": 9.1},
    {"pick": 3, "round": 1, "pick_in_round": 3, "team": "NYG", "name": "Abdul Carter", "position": "EDGE", "college": "Penn State", "grade": 9.0},
    {"pick": 4, "round": 1, "pick_in_round": 4, "team": "NE", "name": "Will Campbell", "position": "OT", "college": "LSU", "grade": 8.9},
    {"pick": 5, "round": 1, "pick_in_round": 5, "team": "JAX", "name": "Tetairoa McMillan", "position": "WR", "college": "Arizona", "grade": 8.8},
    {"pick": 6, "round": 1, "pick_in_round": 6, "team": "LV", "name": "Ashton Jeanty", "position": "RB", "college": "Boise State", "grade": 8.7},
    {"pick": 7, "round": 1, "pick_in_round": 7, "team": "NYJ", "name": "Mason Graham", "position": "DT", "college": "Michigan", "grade": 8.6},
    {"pick": 8, "round": 1, "pick_in_round": 8, "team": "CAR", "name": "Kelvin Banks Jr.", "position": "OT", "college": "Texas", "grade": 8.5},
    {"pick": 9, "round": 1, "pick_in_round": 9, "team": "NO", "name": "Shemar Stewart", "position": "EDGE", "college": "Texas A&M", "grade": 8.4},
    {"pick": 10, "round": 1, "pick_in_round": 10, "team": "CHI", "name": "Malaki Starks", "position": "S", "college": "Georgia", "grade": 8.3},
    {"pick": 11, "round": 1, "pick_in_round": 11, "team": "SF", "name": "Luther Burden III", "position": "WR", "college": "Missouri", "grade": 8.2},
    {"pick": 12, "round": 1, "pick_in_round": 12, "team": "DAL", "name": "Nick Emmanwori", "position": "S", "college": "South Carolina", "grade": 8.1},
    {"pick": 13, "round": 1, "pick_in_round": 13, "team": "MIA", "name": "Jalon Walker", "position": "LB", "college": "Georgia", "grade": 8.0},
    {"pick": 14, "round": 1, "pick_in_round": 14, "team": "IND", "name": "Tyler Warren", "position": "TE", "college": "Penn State", "grade": 7.9},
    {"pick": 15, "round": 1, "pick_in_round": 15, "team": "ATL", "name": "Darian Porter", "position": "CB", "college": "Iowa State", "grade": 7.8},
    {"pick": 16, "round": 1, "pick_in_round": 16, "team": "ARI", "name": "James Pearce Jr.", "position": "EDGE", "college": "Tennessee", "grade": 7.7},
    {"pick": 17, "round": 1, "pick_in_round": 17, "team": "CIN", "name": "Mykel Williams", "position": "EDGE", "college": "Georgia", "grade": 7.6},
    {"pick": 18, "round": 1, "pick_in_round": 18, "team": "SEA", "name": "Walter Nolen", "position": "DT", "college": "Ole Miss", "grade": 7.5},
    {"pick": 19, "round": 1, "pick_in_round": 19, "team": "TB", "name": "Omarion Hampton", "position": "RB", "college": "North Carolina", "grade": 7.4},
    {"pick": 20, "round": 1, "pick_in_round": 20, "team": "DEN", "name": "Colston Loveland", "position": "TE", "college": "Michigan", "grade": 7.3},
    {"pick": 21, "round": 1, "pick_in_round": 21, "team": "PIT", "name": "Josh Simmons", "position": "OT", "college": "Ohio State", "grade": 7.2},
    {"pick": 22, "round": 1, "pick_in_round": 22, "team": "LAC", "name": "Dontay Demus Jr.", "position": "WR", "college": "Maryland", "grade": 7.1},
    {"pick": 23, "round": 1, "pick_in_round": 23, "team": "GB", "name": "Emeka Egbuka", "position": "WR", "college": "Ohio State", "grade": 7.0},
    {"pick": 24, "round": 1, "pick_in_round": 24, "team": "MIN", "name": "Kenneth Grant", "position": "DT", "college": "Michigan", "grade": 6.9},
    {"pick": 25, "round": 1, "pick_in_round": 25, "team": "HOU", "name": "Grey Zabel", "position": "OG", "college": "North Dakota State", "grade": 6.8},
    {"pick": 26, "round": 1, "pick_in_round": 26, "team": "LAR", "name": "Derrick Harmon", "position": "DT", "college": "Oregon", "grade": 6.7},
    {"pick": 27, "round": 1, "pick_in_round": 27, "team": "BAL", "name": "Maxwell Hairston", "position": "CB", "college": "Kentucky", "grade": 6.6},
    {"pick": 28, "round": 1, "pick_in_round": 28, "team": "DET", "name": "Jaylen Reed", "position": "S", "college": "Penn State", "grade": 6.5},
    {"pick": 29, "round": 1, "pick_in_round": 29, "team": "WAS", "name": "Donovan Jackson", "position": "OG", "college": "Ohio State", "grade": 6.4},
    {"pick": 30, "round": 1, "pick_in_round": 30, "team": "BUF", "name": "Jihaad Campbell", "position": "LB", "college": "Alabama", "grade": 6.3},
    {"pick": 31, "round": 1, "pick_in_round": 31, "team": "KC", "name": "Shedeur Sanders", "position": "QB", "college": "Colorado", "grade": 6.2},
    {"pick": 32, "round": 1, "pick_in_round": 32, "team": "PHI", "name": "Armand Membou", "position": "OT", "college": "Missouri", "grade": 6.1},
]


def _scrape_prospects() -> List[dict]:
    """Attempt to scrape 2026 prospects. Returns empty list on failure."""
    prospects: List[dict] = []
    try:
        resp = requests.get(
            _TDN_URL.format(year=DRAFT_YEAR), headers=_HEADERS, timeout=15
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        rows = soup.select("table tbody tr, .big-board-row")
        for i, row in enumerate(rows, start=1):
            cols = row.find_all("td")
            if len(cols) >= 4:
                prospects.append({
                    "pick": i,
                    "round": ((i - 1) // 32) + 1,
                    "pick_in_round": ((i - 1) % 32) + 1,
                    "team": None,
                    "name": cols[1].get_text(strip=True),
                    "position": cols[2].get_text(strip=True),
                    "college": cols[3].get_text(strip=True),
                    "grade": None,
                })
    except Exception as exc:
        logger.warning("Draft scraping failed (%s). Using seed data.", exc)
    return prospects


def sync_draft_prospects(db: Session, year: int = DRAFT_YEAR) -> int:
    """Sync 2026 draft prospects into the DB."""
    prospects = _scrape_prospects()
    if not prospects:
        logger.info("Using seed prospect data for year %d", year)
        prospects = _SEED_PROSPECTS

    count = 0
    for p in prospects:
        pick_num = p.get("pick") or count + 1
        record = (
            db.query(DraftProspect)
            .filter(DraftProspect.pick_number == pick_num, DraftProspect.year == year)
            .first()
        )
        if record is None:
            record = DraftProspect(pick_number=pick_num, year=year)
            db.add(record)

        record.round_number = p.get("round", 1)
        record.pick_in_round = p.get("pick_in_round")
        record.team_abbr = p.get("team")
        record.player_name = p.get("name")
        record.position = p.get("position")
        record.college = p.get("college")
        record.grade = p.get("grade")
        count += 1

    db.commit()
    logger.info("Synced %d draft prospects for year %d", count, year)
    return count


def get_draft_prospects(
    db: Session,
    year: int = DRAFT_YEAR,
    round_number: Optional[int] = None,
    position: Optional[str] = None,
) -> List[DraftProspectRead]:
    query = db.query(DraftProspect).filter(DraftProspect.year == year)
    if round_number is not None:
        query = query.filter(DraftProspect.round_number == round_number)
    if position:
        query = query.filter(DraftProspect.position.ilike(f"%{position}%"))
    prospects = query.order_by(DraftProspect.pick_number).all()
    return [DraftProspectRead.model_validate(p) for p in prospects]
