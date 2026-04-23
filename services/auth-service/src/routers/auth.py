from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User
from src.schemas import RegisterRequest, LoginRequest, AuthResponse, VerifyRequest, VerifyResponse
from src.security import hash_password, verify_password, create_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        phone=body.phone,
        role="guest",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(str(user.id), user.role)
    return {"user": user, "token": token}

@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(str(user.id), user.role)
    return {"user": user, "token": token}

@router.post("/verify", response_model=VerifyResponse)
def verify(body: VerifyRequest, db: Session = Depends(get_db)):
    result = decode_token(body.token)
    if not result["valid"]:
        return {"valid": False}

    user = db.query(User).filter(User.id == result["user_id"]).first()
    if not user:
        return {"valid": False}

    return {"valid": True, "user": user}
