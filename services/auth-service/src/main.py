from fastapi import FastAPI
from src.database import engine, Base
from src.routers import auth, users

# Tạo các bảng trong CSDL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "auth-service"}
