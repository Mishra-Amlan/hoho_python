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
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Property).join(HotelGroup)
    
    if hotel_group_id:
        query = query.filter(Property.hotel_group_id == hotel_group_id)
    if status:
        query = query.filter(Property.status == status)
    
    properties = query.order_by(Property.name).all()
    
    result = []
    for prop in properties:
        result.append({
            "id": prop.id,
            "name": prop.name,
            "location": prop.location,
            "hotel_group_id": prop.hotel_group_id,
            "hotel_group_name": prop.hotel_group.name,
            "manager_name": prop.manager_name,
            "manager_email": prop.manager_email,
            "status": prop.status,
            "overall_score": prop.overall_score,
            "last_audit_date": prop.last_audit_date,
            "created_at": prop.created_at
        })
    
    return result

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: int, db: Session = Depends(get_db)):
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return {
        "id": property_obj.id,
        "name": property_obj.name,
        "location": property_obj.location,
        "hotel_group_id": property_obj.hotel_group_id,
        "hotel_group_name": property_obj.hotel_group.name,
        "manager_name": property_obj.manager_name,
        "manager_email": property_obj.manager_email,
        "status": property_obj.status,
        "overall_score": property_obj.overall_score,
        "last_audit_date": property_obj.last_audit_date,
        "created_at": property_obj.created_at
    }

@router.post("/", response_model=PropertyResponse)
async def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    # Check if hotel group exists
    hotel_group = db.query(HotelGroup).filter(HotelGroup.id == property_data.hotel_group_id).first()
    if not hotel_group:
        raise HTTPException(status_code=404, detail="Hotel group not found")
    
    property_obj = Property(
        name=property_data.name,
        location=property_data.location,
        hotel_group_id=property_data.hotel_group_id,
        manager_name=property_data.manager_name,
        manager_email=property_data.manager_email,
        status=property_data.status or "active"
    )
    
    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    
    return {
        "id": property_obj.id,
        "name": property_obj.name,
        "location": property_obj.location,
        "hotel_group_id": property_obj.hotel_group_id,
        "hotel_group_name": property_obj.hotel_group.name,
        "manager_name": property_obj.manager_name,
        "manager_email": property_obj.manager_email,
        "status": property_obj.status,
        "overall_score": property_obj.overall_score,
        "last_audit_date": property_obj.last_audit_date,
        "created_at": property_obj.created_at
    }

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(property_id: int, property_updates: dict, db: Session = Depends(get_db)):
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Update fields
    for field, value in property_updates.items():
        if hasattr(property_obj, field) and value is not None:
            setattr(property_obj, field, value)
    
    db.commit()
    db.refresh(property_obj)
    
    return {
        "id": property_obj.id,
        "name": property_obj.name,
        "location": property_obj.location,
        "hotel_group_id": property_obj.hotel_group_id,
        "hotel_group_name": property_obj.hotel_group.name,
        "manager_name": property_obj.manager_name,
        "manager_email": property_obj.manager_email,
        "status": property_obj.status,
        "overall_score": property_obj.overall_score,
        "last_audit_date": property_obj.last_audit_date,
        "created_at": property_obj.created_at
    }