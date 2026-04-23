from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class RoomBase(BaseModel):
    room_number: str
    type: str
    price_per_night: float
    description: Optional[str] = None
    capacity: int
    images: List[str] = []

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    type: Optional[str] = None
    price_per_night: Optional[float] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    images: Optional[List[str]] = None

class RoomStatusUpdate(BaseModel):
    status: str

class RoomResponse(RoomBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RoomListResponse(BaseModel):
    data: List[RoomResponse]
    total: int
    page: int
    limit: int
