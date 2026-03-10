from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class DraftProspectBase(BaseModel):
    pick_number: int
    round_number: int
    pick_in_round: Optional[int] = None
    team_abbr: Optional[str] = None
    player_name: Optional[str] = None
    position: Optional[str] = None
    college: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    age: Optional[float] = None
    games: Optional[int] = None
    stats_json: Optional[str] = None
    grade: Optional[float] = None
    notes: Optional[str] = None
    year: int = 2026

    @property
    def stats(self) -> Dict[str, Any]:
        if self.stats_json:
            try:
                return json.loads(self.stats_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}


class DraftProspectCreate(DraftProspectBase):
    pass


class DraftProspectRead(DraftProspectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: Optional[datetime] = None
