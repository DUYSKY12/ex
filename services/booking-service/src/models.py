import uuid
from sqlalchemy import Column, String, Float, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    room_id = Column(UUID(as_uuid=True), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    payment_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String, default="pending") # pending, confirmed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
