"""
Roster service – fetches current NFL roster data using nfl_data_py.
"""
from __future__ import annotations

import logging
from typing import List, Optional

import nfl_data_py as nfl
from sqlalchemy.orm import Session

from app.models.player import Player
from app.schemas.player import PlayerRead

logger = logging.getLogger(__name__)

CURRENT_SEASON = 2024


def _safe_str(val) -> Optional[str]:
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return None
    return str(val)


def _safe_int(val) -> Optional[int]:
    try:
        v = int(val)
        return v
    except (TypeError, ValueError):
        return None


def sync_rosters(db: Session, season: int = CURRENT_SEASON) -> int:
    """Pull roster data for the given season and upsert into the DB."""
    try:
        df = nfl.import_seasonal_rosters([season], columns=[
            "season", "player_id", "player_name", "position", "team", "jersey_number",
            "status", "years_exp", "college", "height", "weight", "birth_date",
            "headshot_url", "depth_chart_position",
            "first_name", "last_name",
        ])
    except Exception as exc:
        logger.error("Failed to import rosters: %s", exc)
        raise

    count = 0
    for _, row in df.iterrows():
        pid = _safe_str(row.get("player_id"))
        if not pid:
            continue

        record = db.query(Player).filter(Player.player_id == pid).first()
        if record is None:
            record = Player(player_id=pid)
            db.add(record)

        record.full_name = _safe_str(row.get("player_name"))
        record.first_name = _safe_str(row.get("first_name"))
        record.last_name = _safe_str(row.get("last_name"))
        record.position = _safe_str(row.get("position"))
        record.team = _safe_str(row.get("team"))
        record.jersey_number = _safe_int(row.get("jersey_number"))
        record.status = _safe_str(row.get("status"))
        record.years_exp = _safe_int(row.get("years_exp"))
        record.college = _safe_str(row.get("college"))
        record.height = _safe_str(row.get("height"))
        record.weight = _safe_int(row.get("weight"))
        record.birth_date = _safe_str(row.get("birth_date"))
        record.headshot_url = _safe_str(row.get("headshot_url"))
        record.depth_chart_position = _safe_str(row.get("depth_chart_position"))
        record.depth_chart_order = None
        record.season = season
        count += 1

    db.commit()
    logger.info("Synced %d roster players for season %d", count, season)
    return count


def get_roster_by_team(db: Session, team_abbr: str, season: int = CURRENT_SEASON) -> List[PlayerRead]:
    players = (
        db.query(Player)
        .filter(Player.team == team_abbr.upper(), Player.season == season)
        .order_by(Player.position, Player.depth_chart_order)
        .all()
    )
    return [PlayerRead.model_validate(p) for p in players]


def get_player(db: Session, player_id: str) -> Optional[PlayerRead]:
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        return None
    return PlayerRead.model_validate(player)
