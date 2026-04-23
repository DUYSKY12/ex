from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Room
from src.schemas import RoomCreate, RoomUpdate, RoomResponse, RoomListResponse, RoomStatusUpdate
from typing import Optional, List
from datetime import date

router = APIRouter(prefix="/rooms", tags=["rooms"])

def require_admin(x_user_role: Optional[str] = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail={"error": "Forbidden", "message": "Admin access required"})
    return x_user_role

@router.get("", response_model=RoomListResponse)
def get_rooms(
    status: Optional[str] = None,
    type: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Room)
    if status:
        query = query.filter(Room.status == status)
    if type:
        query = query.filter(Room.type == type)
    
    total = query.count()
    rooms = query.offset((page - 1) * limit).limit(limit).all()
    
    return {"data": rooms, "total": total, "page": page, "limit": limit}

@router.post("", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate, db: Session = Depends(get_db), role: str = Depends(require_admin)):
    db_room = db.query(Room).filter(Room.room_number == room.room_number).first()
    if db_room:
        raise HTTPException(status_code=400, detail={"error": "BadRequest", "message": "Room number already exists"})
    
    new_room = Room(**room.model_dump())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/available", response_model=dict)
def get_available_rooms(
    check_in: date,
    check_out: date,
    type: Optional[str] = None,
    capacity: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if check_in >= check_out:
        raise HTTPException(status_code=400, detail={"error": "BadRequest", "message": "Check-out date must be after check-in date"})

    # Logic tìm phòng trống thực tế sẽ phức tạp hơn (cần join với bảng Booking).
    # Hiện tại mock logic đơn giản là lấy các phòng status = 'available'.
    query = db.query(Room).filter(Room.status == "available")
    if type:
        query = query.filter(Room.type == type)
    if capacity:
        query = query.filter(Room.capacity >= capacity)
    
    rooms = query.all()
    return {"data": rooms, "total": len(rooms)}

@router.get("/{id}", response_model=RoomResponse)
def get_room(id: str, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Room not found"})
    return room

@router.put("/{id}", response_model=RoomResponse)
def update_room(id: str, room_update: RoomUpdate, db: Session = Depends(get_db), role: str = Depends(require_admin)):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Room not found"})
    
    update_data = room_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)
        
    db.commit()
    db.refresh(room)
    return room

@router.patch("/{id}/status", response_model=RoomResponse)
def update_room_status(id: str, status_update: RoomStatusUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Room not found"})
    
    room.status = status_update.status
    db.commit()
    db.refresh(room)
    return room

@router.delete("/{id}", status_code=204)
def delete_room(id: str, db: Session = Depends(get_db), role: str = Depends(require_admin)):
    room = db.query(Room).filter(Room.id == id).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Room not found"})
    
    db.delete(room)
    db.commit()
    return None
