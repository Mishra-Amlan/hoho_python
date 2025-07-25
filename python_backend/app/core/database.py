from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.models import Base

# Create PostgreSQL engine with SQLAlchemy
try:
    engine = create_engine(
        settings.database_url,
        echo=False,  # Disable SQL logging for cleaner output
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,  # Recycle connections every hour
    )
    print(f"Database engine created successfully with URL: {settings.database_url}")
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

def test_connection():
    """Test the database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Database connection test successful: {result.fetchone()}")
            return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
