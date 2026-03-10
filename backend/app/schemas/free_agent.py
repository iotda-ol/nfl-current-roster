from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FreeAgentBase(BaseModel):
    player_id: str
    full_name: Optional[str] = None
    position: Optional[str] = None
    position_group: Optional[str] = None
    age: Optional[int] = None
    years_exp: Optional[int] = None
    college: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    last_team: Optional[str] = None
    contract_value: Optional[str] = None
    headshot_url: Optional[str] = None


class FreeAgentCreate(FreeAgentBase):
    pass


class FreeAgentRead(FreeAgentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: Optional[datetime] = None
