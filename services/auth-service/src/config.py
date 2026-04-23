import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:changeme@db-auth:5432/auth_db")
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key")
JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")
