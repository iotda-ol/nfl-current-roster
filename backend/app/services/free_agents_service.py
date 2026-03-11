"""
Free Agents service – combines nfl_data_py roster data (FA status) with
structured web scraping via BeautifulSoup for additional context.
"""
from __future__ import annotations

import logging
from typing import List, Optional

import nfl_data_py as nfl
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models.free_agent import FreeAgent
from app.schemas.free_agent import FreeAgentRead

logger = logging.getLogger(__name__)

CURRENT_SEASON = 2024
_FA_URL = "https://www.spotrac.com/nfl/free-agents/"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; NFLDashboard/1.0; "
        "+https://github.com/iotda-ol/nfl-current-roster)"
    )
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
                contract_map[player_name] = contract_val
    except Exception as exc:
        logger.warning("Could not scrape FA contract data: %s", exc)
    return contract_map


def sync_free_agents(db: Session, season: int = CURRENT_SEASON) -> int:
    """Pull free agents from nfl_data_py (status == 'FA') and upsert into the DB."""
    try:
        df = nfl.import_seasonal_rosters([season], columns=[
            "season", "player_id", "player_name", "position", "team", "status",
            "years_exp", "college", "height", "weight", "birth_date",
            "headshot_url", "first_name", "last_name",
        ])
    except Exception as exc:
        logger.error("Failed to import rosters for FA sync: %s", exc)
        raise

    # Filter to free agents (status FA or no team)
    fa_df = df[df["status"].isin(["FA", "RFA", "UFA"]) | df["team"].isna()].copy()

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
        record.full_name = full_name
        record.position = _safe_str(row.get("position"))
        record.years_exp = _safe_int(row.get("years_exp"))
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
