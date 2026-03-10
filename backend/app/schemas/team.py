from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    team_abbr: str
    team_name: str
    team_nick: Optional[str] = None
    team_conf: Optional[str] = None
    team_division: Optional[str] = None
    team_color: Optional[str] = None
    team_color2: Optional[str] = None
    team_logo_wikipedia: Optional[str] = None
    team_wordmark: Optional[str] = None
    team_conference_logo: Optional[str] = None
    team_league_logo: Optional[str] = None
    team_logo_espn: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: Optional[datetime] = None
