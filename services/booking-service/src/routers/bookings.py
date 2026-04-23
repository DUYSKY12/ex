from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Booking
from src.schemas import BookingCreate, BookingResponse, BookingListResponse, ConfirmBookingRequest
from src.external_services import get_room, update_room_status
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/bookings", tags=["bookings"])

def get_current_user_id(x_user_id: Optional[str] = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail={"error": "Unauthorized", "message": "Missing X-User-Id header"})
    return x_user_id

@router.post("", response_model=BookingResponse, status_code=201)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    if booking.check_in >= booking.check_out:
        raise HTTPException(status_code=400, detail={"error": "BadRequest", "message": "Check-out must be after check-in"})
    
    # 1. Gọi Room Service để lấy thông tin phòng
    room = get_room(str(booking.room_id))
    if not room:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Room not found"})
    
    if room.get("status") != "available":
        raise HTTPException(status_code=409, detail={"error": "Conflict", "message": "Room is not available"})
    
    # 2. Tính tổng tiền
    days = (booking.check_out - booking.check_in).days
    total_price = days * room.get("price_per_night", 0)
    
    # 3. Tạo Booking với trạng thái pending
    new_booking = Booking(
        user_id=user_id,
        room_id=booking.room_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_price=total_price,
        status="pending"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    # 4. (Saga Phase 1) Gọi Room Service để khóa phòng (booked)
    success = update_room_status(str(booking.room_id), "booked")
    if not success:
        db.delete(new_booking)
        db.commit()
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": "Failed to lock room"})
        
    return new_booking

@router.get("", response_model=BookingListResponse)
def get_my_bookings(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    query = db.query(Booking).filter(Booking.user_id == user_id)
    if status:
        query = query.filter(Booking.status == status)
    
    total = query.count()
    bookings = query.offset((page - 1) * limit).limit(limit).all()
    
    return {"data": bookings, "total": total, "page": page, "limit": limit}

@router.patch("/{id}/confirm", response_model=BookingResponse)
def confirm_booking(id: str, req: ConfirmBookingRequest, db: Session = Depends(get_db)):
    # Endpoint này dành cho Payment Service gọi sang sau khi thanh toán thành công
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Booking not found"})
    
    if booking.status != "pending":
        raise HTTPException(status_code=400, detail={"error": "BadRequest", "message": "Only pending bookings can be confirmed"})
        
    booking.status = "confirmed"
    booking.payment_id = req.payment_id
    db.commit()
    db.refresh(booking)
    return booking

@router.patch("/{id}/cancel", response_model=BookingResponse)
def cancel_booking(id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    booking = db.query(Booking).filter(Booking.id == id, Booking.user_id == user_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Booking not found"})
        
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail={"error": "BadRequest", "message": "Booking is already cancelled"})
        
    # Saga Compensating Transaction: Cập nhật lại trạng thái phòng thành available
    update_room_status(str(booking.room_id), "available")
    
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking
