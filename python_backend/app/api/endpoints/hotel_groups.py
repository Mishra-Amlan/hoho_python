from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import HotelGroup
from app.schemas.schemas import HotelGroupCreate, HotelGroupResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[HotelGroupResponse])
async def get_hotel_groups(db: Session = Depends(get_db)):
    hotel_groups = db.query(HotelGroup).order_by(HotelGroup.name).all()
    
    result = []
    for group in hotel_groups:
        result.append({
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "default_sop_files": group.default_sop_files,
            "created_at": group.created_at
        })
    
    return result

@router.get("/{group_id}", response_model=HotelGroupResponse)
async def get_hotel_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(HotelGroup).filter(HotelGroup.id == group_id).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Hotel group not found")
    
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "default_sop_files": group.default_sop_files,
        "created_at": group.created_at
    }

@router.post("/", response_model=HotelGroupResponse)
async def create_hotel_group(group_data: HotelGroupCreate, db: Session = Depends(get_db)):
    # Check if name already exists
    existing_group = db.query(HotelGroup).filter(HotelGroup.name == group_data.name).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Hotel group name already exists")
    
    group = HotelGroup(
        name=group_data.name,
        description=group_data.description,
        default_sop_files=group_data.default_sop_files
    )
    
    db.add(group)
    db.commit()
    db.refresh(group)
    
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "default_sop_files": group.default_sop_files,
        "created_at": group.created_at
    }

@router.put("/{group_id}", response_model=HotelGroupResponse)
async def update_hotel_group(group_id: int, group_updates: dict, db: Session = Depends(get_db)):
    group = db.query(HotelGroup).filter(HotelGroup.id == group_id).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Hotel group not found")
    
    # Update fields
    for field, value in group_updates.items():
        if hasattr(group, field) and value is not None:
            setattr(group, field, value)
    
    db.commit()
    db.refresh(group)
    
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "default_sop_files": group.default_sop_files,
        "created_at": group.created_at
    }