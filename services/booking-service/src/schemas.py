from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date

class BookingCreate(BaseModel):
    room_id: UUID
    check_in: date
    check_out: date

class ConfirmBookingRequest(BaseModel):
    payment_id: UUID

class BookingResponse(BaseModel):
    id: UUID
    user_id: UUID
    room_id: UUID
    check_in: date
    check_out: date
    total_price: float
    payment_id: Optional[UUID] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingListResponse(BaseModel):
    data: List[BookingResponse]
    total: int
    page: int
    limit: int
