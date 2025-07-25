from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base
from app.core.config import settings

print(f"Database engine created successfully with SQLite")
print(f"Database file: hotel_audit.db")

# Create engine for SQLite (simulating MS SQL Server structure)
try:
    if settings.database_url.startswith("sqlite"):
        engine = create_engine(
            settings.database_url,
            echo=False,  # Disable SQL logging for cleaner output
            connect_args={"check_same_thread": False},  # SQLite specific
        )
    else:
        engine = create_engine(
            settings.database_url,
            echo=False,  # Disable SQL logging for cleaner output
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,  # Recycle connections every hour
        )
    print("SQLite database engine created successfully!")
except Exception as e:
    print(f"Failed to create SQLite engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        Base.metadata.create_all(bind=engine)
        print("SQLite tables created successfully!")
    except Exception as e:
        print(f"Error creating SQLite tables: {e}")
        raise

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test the SQLite database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"SQLite connection test successful: {result.fetchone()}")
            return True
    except Exception as e:
        print(f"SQLite connection test failed: {e}")
        return False