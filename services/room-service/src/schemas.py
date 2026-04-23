from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

class RoomOut(BaseModel):
    id: UUID
    room_number: str
    type: str
    price_per_night: float
    description: Optional[str] = None
    capacity: int
    images: List[str] = []
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class CreateRoomRequest(BaseModel):
    room_number: str
    type: str
    price_per_night: float
    description: Optional[str] = None
    capacity: int
    images: Optional[List[str]] = []

class UpdateRoomRequest(BaseModel):
    room_number: Optional[str] = None
    type: Optional[str] = None
    price_per_night: Optional[float] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    images: Optional[List[str]] = None

class UpdateStatusRequest(BaseModel):
    status: str
