from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hotel Audit Management"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # SQLite Database Configuration (pure Python setup)
    DATABASE_URL: str = "sqlite:///./hotel_audit.db"
    
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-hotel-audit-2024")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    class Config:
        case_sensitive = True

settings = Settings()
