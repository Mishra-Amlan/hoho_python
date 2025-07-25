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
        "created_at": group.created_at
    }

@router.post("/", response_model=HotelGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel_group(group_data: HotelGroupCreate, db: Session = Depends(get_db)):
    # Create new hotel group
    new_group = HotelGroup(
        name=group_data.name,
        description=group_data.description
    )
    
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    
    return {
        "id": new_group.id,
        "name": new_group.name,
        "description": new_group.description,
        "created_at": new_group.created_at
    }