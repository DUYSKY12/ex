import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Enum, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_number = Column(String, unique=True, nullable=False)
    type = Column(Enum("single", "double", "suite", name="room_type"), nullable=False)
    price_per_night = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    capacity = Column(Integer, nullable=False)
    images = Column(ARRAY(String), default=[])
    status = Column(
        Enum("available", "booked", "maintenance", name="room_status"),
        default="available",
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
