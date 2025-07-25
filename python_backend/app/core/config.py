from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
import pyodbc 

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hotel Audit Management"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MS SQL Server Database Configuration
    MSSQL_SERVER: str = os.getenv("MSSQL_SERVER", "LAPTOP-OQB79HTV\\SQLEXPRESS")
    MSSQL_DATABASE: str = os.getenv("MSSQL_DATABASE", "hotel_audit_db")
    MSSQL_USERNAME: str = os.getenv("MSSQL_USERNAME", "Amlan")
    MSSQL_PASSWORD: str = os.getenv("MSSQL_PASSWORD", "Amlan@123")
    MSSQL_DRIVER: str = os.getenv("MSSQL_DRIVER", "{ODBC Driver 17 for SQL Server}")
    
    # Build SQL Server connection string
    @property
    def database_url(self) -> str:
        return f"mssql+pyodbc://{self.MSSQL_USERNAME}:{self.MSSQL_PASSWORD}@{self.MSSQL_SERVER}/{self.MSSQL_DATABASE}?driver={self.MSSQL_DRIVER.replace(' ', '+').replace('{', '').replace('}', '')}&TrustServerCertificate=yes"
    
    # Direct pyodbc connection function
    def get_pyodbc_connection(self):
        try:
            connection = pyodbc.connect(
                f'DRIVER={self.MSSQL_DRIVER};SERVER={self.MSSQL_SERVER};DATABASE={self.MSSQL_DATABASE};UID={self.MSSQL_USERNAME};PWD={self.MSSQL_PASSWORD};TrustServerCertificate=yes'
            )
            print("MS SQL Server connection successful!")
            return connection
        except pyodbc.Error as e:
            print(f"Error connecting to MS SQL Server: {e}")
            raise
    
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
