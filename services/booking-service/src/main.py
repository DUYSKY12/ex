from fastapi import FastAPI
from src.database import engine, Base
from src.routers import bookings

# Tạo các bảng trong CSDL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking Service", version="1.0.0")

app.include_router(bookings.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "booking-service"}
