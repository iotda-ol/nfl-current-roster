"""
Free Agents service – combines nfl_data_py roster data (FA status) with
structured web scraping via BeautifulSoup for additional context.
"""
from __future__ import annotations

import datetime
import logging
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models.free_agent import FreeAgent
from app.schemas.free_agent import FreeAgentRead

logger = logging.getLogger(__name__)

CURRENT_SEASON = 2025
_FA_URL = "https://www.spotrac.com/nfl/free-agents/"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; NFLDashboard/1.0; "
        "+https://github.com/iotda-ol/nfl-current-roster)"
    )
}

# Position group mapping
_POSITION_GROUP_MAP: dict[str, str] = {
    "QB": "QB",
    "RB": "RB", "FB": "RB",
    "WR": "WR", "TE": "TE",
    "OT": "OL", "OG": "OL", "C": "OL", "OL": "OL",
    "DE": "DL", "DT": "DL", "NT": "DL", "DL": "DL",
    "LB": "LB", "ILB": "LB", "OLB": "LB", "MLB": "LB",
    "CB": "DB", "S": "DB", "FS": "DB", "SS": "DB", "DB": "DB",
    "EDGE": "DL",
    "K": "ST", "P": "ST", "LS": "ST",
}


def _safe_str(val) -> Optional[str]:
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return None
    return str(val)


def _safe_int(val) -> Optional[int]:
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _calc_age(birth_date: Optional[str]) -> Optional[int]:
    """Return age in years from a 'YYYY-MM-DD' birth date string."""
    if not birth_date:
        return None
    try:
        bd = datetime.date.fromisoformat(birth_date)
        today = datetime.date.today()
        return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    except (ValueError, TypeError):
        return None


def _scrape_fa_contract_data() -> dict:
    """Attempt to scrape free agent contract values from Spotrac.

    Returns a dict mapping player name -> contract value string.
    Falls back gracefully to empty dict on any error.
    """
    contract_map: dict = {}
    try:
        resp = requests.get(_FA_URL, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        rows = soup.select("table.datatable tbody tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name_el = cols[0].find("a")
                player_name = name_el.get_text(strip=True) if name_el else cols[0].get_text(strip=True)
                contract_val = cols[2].get_text(strip=True) if len(cols) > 2 else ""
                if player_name:
                    contract_map[player_name] = contract_val
    except Exception as exc:
        logger.warning("Could not scrape FA contract data: %s", exc)
    return contract_map


def sync_free_agents(db: Session, season: int = CURRENT_SEASON) -> int:
    """Pull free agents from nfl_data_py (status == 'FA') and upsert into the DB."""
    import nfl_data_py as nfl  # lazy import – only needed during sync

    try:
        df = nfl.import_rosters([season], columns=[
            "player_id", "player_name", "position", "team", "status",
            "years_exp", "college", "height", "weight", "birth_date",
            "headshot_url", "first_name", "last_name",
        ])
    except Exception as exc:
        logger.error("Failed to import rosters for FA sync: %s", exc)
        raise

    # Filter to free agents: explicit FA status codes or missing team assignment
    fa_df = df[
        df["status"].isin(["FA", "RFA", "UFA", "EXE"])
        | df["team"].isna()
        | (df["team"].astype(str).str.strip() == "")
    ].copy()

    contract_map = _scrape_fa_contract_data()

    count = 0
    for _, row in fa_df.iterrows():
        pid = _safe_str(row.get("player_id"))
        if not pid:
            continue

        record = db.query(FreeAgent).filter(FreeAgent.player_id == pid).first()
        if record is None:
            record = FreeAgent(player_id=pid)
            db.add(record)

        full_name = _safe_str(row.get("player_name"))
        birth_date = _safe_str(row.get("birth_date"))
        position = _safe_str(row.get("position"))

        record.full_name = full_name
        record.position = position
        record.position_group = _POSITION_GROUP_MAP.get(position or "", None)
        record.years_exp = _safe_int(row.get("years_exp"))
        record.age = _calc_age(birth_date)
        record.college = _safe_str(row.get("college"))
        record.height = _safe_str(row.get("height"))
        record.weight = _safe_int(row.get("weight"))
        record.last_team = _safe_str(row.get("team"))
        record.headshot_url = _safe_str(row.get("headshot_url"))
        if full_name and full_name in contract_map:
            record.contract_value = contract_map[full_name]
        count += 1

    db.commit()
    logger.info("Synced %d free agents for season %d", count, season)
    return count


def get_free_agents(
    db: Session,
    position: Optional[str] = None,
    search: Optional[str] = None,
) -> List[FreeAgentRead]:
    query = db.query(FreeAgent)
    if position:
        query = query.filter(FreeAgent.position == position.upper())
    if search:
        query = query.filter(FreeAgent.full_name.ilike(f"%{search}%"))
    agents = query.order_by(FreeAgent.full_name).all()
    return [FreeAgentRead.model_validate(a) for a in agents]
