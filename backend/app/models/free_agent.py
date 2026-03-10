from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.models.base import Base


class FreeAgent(Base):
    __tablename__ = "free_agents"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200))
    position = Column(String(20), index=True)
    position_group = Column(String(20))
    age = Column(Integer)
    years_exp = Column(Integer)
    college = Column(String(100))
    height = Column(String(10))
    weight = Column(Integer)
    last_team = Column(String(10))
    contract_value = Column(String(50))
    headshot_url = Column(String(500))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
