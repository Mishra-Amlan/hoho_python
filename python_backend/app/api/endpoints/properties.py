from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Property, HotelGroup
from app.schemas.schemas import PropertyCreate, PropertyResponse
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    hotel_group_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    
    if hotel_group_id:
        query = query.filter(Property.hotel_group_id == hotel_group_id)
    
    properties = query.order_by(Property.name).all()
    
    result = []
    for prop in properties:
        result.append({
            "id": prop.id,
            "name": prop.name,
            "location": prop.location,
            "hotel_group_id": prop.hotel_group_id,
            "manager_name": prop.manager_name,
            "manager_email": prop.manager_email,
            "phone": prop.phone,
            "created_at": prop.created_at
        })
    
    return result

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return {
        "id": prop.id,
        "name": prop.name,
        "location": prop.location,
        "hotel_group_id": prop.hotel_group_id,
        "manager_name": prop.manager_name,
        "manager_email": prop.manager_email,
        "phone": prop.phone,
        "created_at": prop.created_at
    }

@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    # Check if hotel group exists
    hotel_group = db.query(HotelGroup).filter(HotelGroup.id == property_data.hotel_group_id).first()
    if not hotel_group:
        raise HTTPException(status_code=404, detail="Hotel group not found")
    
    # Create new property
    new_property = Property(
        name=property_data.name,
        location=property_data.location,
        hotel_group_id=property_data.hotel_group_id,
        manager_name=property_data.manager_name,
        manager_email=property_data.manager_email,
        phone=property_data.phone
    )
    
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    
    return {
        "id": new_property.id,
        "name": new_property.name,
        "location": new_property.location,
        "hotel_group_id": new_property.hotel_group_id,
        "manager_name": new_property.manager_name,
        "manager_email": new_property.manager_email,
        "phone": new_property.phone,
        "created_at": new_property.created_at
    }