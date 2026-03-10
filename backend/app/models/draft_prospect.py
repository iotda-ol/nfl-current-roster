from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.models.base import Base


class DraftProspect(Base):
    __tablename__ = "draft_prospects"

    id = Column(Integer, primary_key=True, index=True)
    pick_number = Column(Integer, index=True)
    round_number = Column(Integer, index=True)
    pick_in_round = Column(Integer)
    team_abbr = Column(String(10), index=True)
    player_name = Column(String(200))
    position = Column(String(20), index=True)
    college = Column(String(100))
    height = Column(String(10))
    weight = Column(Integer)
    age = Column(Float)
    # Collegiate stats
    games = Column(Integer)
    stats_json = Column(String(2000))  # JSON string of key stats
    # Scout ratings
    grade = Column(Float)
    notes = Column(String(500))
    year = Column(Integer, default=2026)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
