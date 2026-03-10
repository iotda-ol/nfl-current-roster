from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.models.base import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200))
    first_name = Column(String(100))
    last_name = Column(String(100))
    position = Column(String(20), index=True)
    position_group = Column(String(20))
    team = Column(String(10), index=True)
    jersey_number = Column(Integer)
    status = Column(String(20))
    years_exp = Column(Integer)
    college = Column(String(100))
    height = Column(String(10))
    weight = Column(Integer)
    birth_date = Column(String(20))
    headshot_url = Column(String(500))
    depth_chart_position = Column(String(20))
    depth_chart_order = Column(Integer)
    season = Column(Integer, index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
