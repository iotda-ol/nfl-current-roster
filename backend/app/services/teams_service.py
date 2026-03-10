"""
Teams service – fetches NFL team data using nfl_data_py and persists to the DB.
"""
from __future__ import annotations

import logging
from typing import List, Optional

import nfl_data_py as nfl
from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate, TeamRead

logger = logging.getLogger(__name__)

_RENAME_MAP = {
    "team_abbr": "team_abbr",
    "team_name": "team_name",
    "team_nick": "team_nick",
    "team_conf": "team_conf",
    "team_division": "team_division",
    "team_color": "team_color",
    "team_color2": "team_color2",
    "team_logo_wikipedia": "team_logo_wikipedia",
    "team_wordmark": "team_wordmark",
    "team_conference_logo": "team_conference_logo",
    "team_league_logo": "team_league_logo",
    "team_logo_espn": "team_logo_espn",
}


def _safe_str(val) -> Optional[str]:
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return None
    return str(val)


def sync_teams(db: Session) -> int:
    """Pull fresh team data from nfl_data_py and upsert into the DB.

    Returns the number of records upserted.
    """
    try:
        df = nfl.import_team_desc()
    except Exception as exc:
        logger.error("Failed to import team descriptions: %s", exc)
        raise

    count = 0
    for _, row in df.iterrows():
        abbr = _safe_str(row.get("team_abbr"))
        if not abbr:
            continue

        record = db.query(Team).filter(Team.team_abbr == abbr).first()
        if record is None:
            record = Team(team_abbr=abbr)
            db.add(record)

        record.team_name = _safe_str(row.get("team_name")) or abbr
        record.team_nick = _safe_str(row.get("team_nick"))
        record.team_conf = _safe_str(row.get("team_conf"))
        record.team_division = _safe_str(row.get("team_division"))
        record.team_color = _safe_str(row.get("team_color"))
        record.team_color2 = _safe_str(row.get("team_color2"))
        record.team_logo_wikipedia = _safe_str(row.get("team_logo_wikipedia"))
        record.team_wordmark = _safe_str(row.get("team_wordmark"))
        record.team_conference_logo = _safe_str(row.get("team_conference_logo"))
        record.team_league_logo = _safe_str(row.get("team_league_logo"))
        record.team_logo_espn = _safe_str(row.get("team_logo_espn"))
        count += 1

    db.commit()
    logger.info("Synced %d teams", count)
    return count


def get_all_teams(db: Session) -> List[TeamRead]:
    teams = db.query(Team).order_by(Team.team_name).all()
    return [TeamRead.model_validate(t) for t in teams]


def get_team(db: Session, team_abbr: str) -> Optional[TeamRead]:
    team = db.query(Team).filter(Team.team_abbr == team_abbr.upper()).first()
    if team is None:
        return None
    return TeamRead.model_validate(team)
