from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.routers import rooms

# Tạo các bảng trong CSDL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Room Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "room-service"}
