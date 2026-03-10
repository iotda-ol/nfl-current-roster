from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PlayerBase(BaseModel):
    player_id: str
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    position_group: Optional[str] = None
    team: Optional[str] = None
    jersey_number: Optional[int] = None
    status: Optional[str] = None
    years_exp: Optional[int] = None
    college: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    birth_date: Optional[str] = None
    headshot_url: Optional[str] = None
    depth_chart_position: Optional[str] = None
    depth_chart_order: Optional[int] = None
    season: Optional[int] = None


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: Optional[datetime] = None
