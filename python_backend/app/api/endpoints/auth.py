from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
import hashlib

router = APIRouter()

def get_password_hash_simple(password: str) -> str:
    """Simple password hashing for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password_simple(plain_password: str, hashed_password: str) -> bool:
    """Simple password verification for demo purposes"""
    return get_password_hash_simple(plain_password) == hashed_password

@router.post("/login", response_model=dict)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password_simple(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "name": user.name,
            "email": user.email
        },
        "message": "Login successful"
    }

@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    # For demo purposes, return a mock user
    # In a real app, this would verify the JWT token
    return {
        "id": 1,
        "username": "admin",
        "role": "admin",
        "name": "System Administrator",
        "email": "admin@hotel-audit.com"
    }