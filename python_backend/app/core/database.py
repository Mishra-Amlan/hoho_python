from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.models import Base
import pyodbc

# Create MS SQL Server engine with SQLAlchemy
try:
    engine = create_engine(
        settings.database_url,
        echo=True,  # Enable SQL logging for debugging
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,  # Recycle connections every hour
    )
except Exception as e:
    print(f"Failed to create SQLAlchemy engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_pyodbc_connection():
    """Get direct pyodbc connection for raw SQL operations"""
    return settings.get_pyodbc_connection()

def test_connection():
    """Test the database connection"""
    try:
        connection = get_pyodbc_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"Database connection test successful: {result}")
        connection.close()
        return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
