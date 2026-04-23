from fastapi import FastAPI
from src.database import Base, engine
from src.routers import auth, users

app = FastAPI(
    title="Auth Service",
    description="Xác thực và phân quyền người dùng",
    version="1.0.0",
)

# Tạo bảng khi khởi động
Base.metadata.create_all(bind=engine)

# Đăng ký routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
def health():
    return {"status": "ok"}
