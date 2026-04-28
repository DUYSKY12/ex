from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User
from src.schemas import UserCreate, AuthResponse, LoginRequest, VerifyRequest, VerifyResponse, UserResponse
from src.security import get_password_hash, verify_password, create_access_token, verify_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail={"error": "Conflict", "message": "Email already exists"})
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(data={"sub": str(new_user.id), "role": new_user.role})
    return {"user": new_user, "token": token}

@router.post("/login", response_model=AuthResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail={"error": "Unauthorized", "message": "Incorrect email or password"})
    
    token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})
    return {"user": db_user, "token": token}

@router.post("/verify", response_model=VerifyResponse)
def verify_jwt(req: VerifyRequest, db: Session = Depends(get_db)):
    payload = verify_token(req.token)
    if not payload:
        return {"valid": False, "user": None}
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"valid": False, "user": None}
    
    return {"valid": True, "user": user}
