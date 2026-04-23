import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
from src.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_number = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False) # single, double, suite
    price_per_night = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    capacity = Column(Integer, default=2)
    images = Column(ARRAY(String), default=[])
    status = Column(String, default="available") # available, booked, maintenance
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
