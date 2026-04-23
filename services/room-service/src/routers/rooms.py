from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, not_, exists
from typing import Optional, List
from datetime import date
from uuid import UUID
from src.database import get_db
from src.models import Room
from src.schemas import RoomOut, CreateRoomRequest, UpdateRoomRequest, UpdateStatusRequest

router = APIRouter(prefix="/rooms", tags=["rooms"])

VALID_STATUSES = {"available", "booked", "maintenance"}
VALID_TYPES = {"single", "double", "suite"}

def require_admin(x_user_role: Optional[str] = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

@router.get("", response_model=List[RoomOut])
def get_rooms(
    status: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Room)
    if status:
        query = query.filter(Room.status == status)
    if type:
        query = query.filter(Room.type == type)
    total = query.count()
    rooms = query.offset((page - 1) * limit).limit(limit).all()
    return rooms

@router.get("/available", response_model=List[RoomOut])
def get_available_rooms(
    check_in: date = Query(...),
    check_out: date = Query(...),
    type: Optional[str] = Query(None),
    capacity: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    # Lấy tất cả phòng đang available, không bị booked trong khoảng ngày này
    # Logic: phòng available và status = available
    # (Booking Service chịu trách nhiệm cập nhật status khi có booking)
    query = db.query(Room).filter(Room.status == "available")

    if type:
        query = query.filter(Room.type == type)
    if capacity:
        query = query.filter(Room.capacity >= capacity)

    return query.all()

@router.get("/{id}", response_model=RoomOut)
def get_room(id: UUID, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("", response_model=RoomOut, status_code=201)
def create_room(
    body: CreateRoomRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    if body.type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of {VALID_TYPES}")

    existing = db.query(Room).filter(Room.room_number == body.room_number).first()
    if existing:
        raise HTTPException(status_code=409, detail="Room number already exists")

    room = Room(**body.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.put("/{id}", response_model=RoomOut)
def update_room(
    id: UUID,
    body: UpdateRoomRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)
    return room

@router.delete("/{id}", status_code=204)
def delete_room(
    id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()

@router.patch("/{id}/status", response_model=RoomOut)
def update_status(
    id: UUID,
    body: UpdateStatusRequest,
    db: Session = Depends(get_db),
):
    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {VALID_STATUSES}")

    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    room.status = body.status
    db.commit()
    db.refresh(room)
    return room
