from sqlalchemy import Column, DateTime, Integer, String, func

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_abbr = Column(String(10), unique=True, nullable=False, index=True)
    team_name = Column(String(100), nullable=False)
    team_nick = Column(String(100))
    team_conf = Column(String(10))
    team_division = Column(String(50))
    team_color = Column(String(10))
    team_color2 = Column(String(10))
    team_logo_wikipedia = Column(String(500))
    team_wordmark = Column(String(500))
    team_conference_logo = Column(String(500))
    team_league_logo = Column(String(500))
    team_logo_espn = Column(String(500))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
