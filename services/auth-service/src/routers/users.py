from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User
from src.schemas import UserResponse
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

# Hàm lấy user_id từ Internal Header (do Gateway truyền xuống)
def get_current_user_id(x_user_id: Optional[str] = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail={"error": "Unauthorized", "message": "Missing X-User-Id header"})
    return x_user_id

@router.get("/me", response_model=UserResponse)
def get_me(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "User not found"})
    return user
