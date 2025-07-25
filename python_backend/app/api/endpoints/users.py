from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse
from typing import List, Optional
import hashlib

router = APIRouter()

def get_password_hash_simple(password: str) -> str:
    """Simple password hashing for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.order_by(User.name).all()
    
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        })
    
    return result

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        username=user_data.username,
        password=get_password_hash_simple(user_data.password),
        role=user_data.role,
        name=user_data.name,
        email=user_data.email
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_updates: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    for field, value in user_updates.items():
        if field == "password" and value:
            setattr(user, field, get_password_hash_simple(value))
        elif hasattr(user, field) and value is not None:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }