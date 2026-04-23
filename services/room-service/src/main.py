from fastapi import FastAPI
from src.database import Base, engine
from src.routers import rooms

app = FastAPI(
    title="Room Service",
    description="Quản lý thông tin phòng khách sạn",
    version="1.0.0",
)

# Tạo bảng khi khởi động
Base.metadata.create_all(bind=engine)

# Đăng ký routers
app.include_router(rooms.router)

@app.get("/health")
def health():
    return {"status": "ok"}
