#!/usr/bin/env python3
"""
Hotel Audit Platform - FastAPI Backend
Main entry point for the Python FastAPI backend server
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings
from app.core.database import create_tables, test_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Hotel Audit Platform API",
    description="AI-Driven Hotel Brand Audit System Backend",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("🗄️ Initializing database...")
    try:
        # Test connection
        if test_connection():
            logger.info("✅ Database connection successful")
        else:
            logger.error("❌ Database connection failed")
            
        # Create tables
        create_tables()
        logger.info("✅ Database tables initialized")
        
        # Seed initial data
        await seed_initial_data()
        logger.info("✅ Initial data seeded")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hotel Audit Platform API", "version": "2.0.0", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}

async def seed_initial_data():
    """Seed database with initial demo data"""
    from app.core.database import SessionLocal
    from app.models.models import User, HotelGroup, Property
    import hashlib
    
    def get_password_hash_simple(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).first():
            logger.info("🔄 Initial data already exists, skipping seed")
            return
            
        # Create demo users
        users = [
            User(username="admin", password=get_password_hash_simple("password"), role="admin", name="Admin User", email="admin@hotel.com"),
            User(username="auditor", password=get_password_hash_simple("password"), role="auditor", name="Auditor User", email="auditor@hotel.com"),
            User(username="reviewer", password=get_password_hash_simple("password"), role="reviewer", name="Reviewer User", email="reviewer@hotel.com"),
            User(username="corporate", password=get_password_hash_simple("password"), role="corporate", name="Corporate User", email="corporate@hotel.com"),
            User(username="hotel_gm", password=get_password_hash_simple("password"), role="hotel_gm", name="Hotel GM User", email="gm@hotel.com"),
        ]
        
        for user in users:
            db.add(user)
        
        # Create demo hotel groups
        hotel_groups = [
            HotelGroup(name="Luxury Hotels Inc.", description="Premium luxury hotel chain"),
            HotelGroup(name="Budget Stay Group", description="Affordable accommodation network"),
        ]
        
        for group in hotel_groups:
            db.add(group)
        
        db.commit()
        
        # Create demo properties
        properties = [
            Property(name="Grand Luxury Hotel", location="New York, NY", hotel_group_id=1, manager_name="John Smith", manager_email="john@grandluxury.com"),
            Property(name="City Center Hotel", location="Los Angeles, CA", hotel_group_id=1, manager_name="Jane Doe", manager_email="jane@citycenter.com"),
            Property(name="Budget Inn Downtown", location="Chicago, IL", hotel_group_id=2, manager_name="Mike Johnson", manager_email="mike@budgetinn.com"),
        ]
        
        for prop in properties:
            db.add(prop)
        
        db.commit()
        logger.info("✅ Demo data seeded successfully")
        
    except Exception as e:
        logger.error(f"❌ Error seeding initial data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("🚀 Starting Hotel Audit Platform FastAPI Server")
    logger.info(f"📍 Server will run on: http://0.0.0.0:8000")
    logger.info(f"📝 API Documentation: http://0.0.0.0:8000/api/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )