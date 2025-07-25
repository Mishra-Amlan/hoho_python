from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.core.database import get_db
from app.models.models import Audit, AuditItem, Property, User, HotelGroup
from app.schemas.schemas import AuditCreate, AuditResponse, AuditItemCreate, AuditItemResponse
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[AuditResponse])
async def get_audits(
    status: Optional[str] = None,
    auditor_id: Optional[int] = None,
    reviewer_id: Optional[int] = None,
    property_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Audit).join(Property).join(HotelGroup)
    
    if status:
        query = query.filter(Audit.status == status)
    if auditor_id:
        query = query.filter(Audit.auditor_id == auditor_id)
    if reviewer_id:
        query = query.filter(Audit.reviewer_id == reviewer_id)
    if property_id:
        query = query.filter(Audit.property_id == property_id)
    
    audits = query.order_by(Audit.created_at.desc()).all()
    
    result = []
    for audit in audits:
        result.append({
            "id": audit.id,
            "property_id": audit.property_id,
            "auditor_id": audit.auditor_id,
            "reviewer_id": audit.reviewer_id,
            "status": audit.status,
            "overall_score": audit.overall_score,
            "created_at": audit.created_at,
            "updated_at": audit.updated_at,
            "scheduled_date": audit.scheduled_date,
            "completed_date": audit.completed_date
        })
    
    return result

@router.get("/{audit_id}", response_model=AuditResponse)
async def get_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    return {
        "id": audit.id,
        "property_id": audit.property_id,
        "property_name": audit.property.name,
        "property_location": audit.property.location,
        "hotel_group_name": audit.hotel_group.name,
        "auditor_id": audit.auditor_id,
        "auditor_name": audit.auditor.name if audit.auditor else None,
        "reviewer_id": audit.reviewer_id,
        "reviewer_name": audit.reviewer.name if audit.reviewer else None,
        "status": audit.status,
        "overall_score": audit.overall_score,
        "cleanliness_score": audit.cleanliness_score,
        "branding_score": audit.branding_score,
        "operational_score": audit.operational_score,
        "compliance_zone": audit.compliance_zone,
        "findings": audit.findings,
        "action_plan": audit.action_plan,
        "submitted_at": audit.submitted_at,
        "reviewed_at": audit.reviewed_at,
        "created_at": audit.created_at
    }

@router.post("/", response_model=AuditResponse)
async def create_audit(audit_data: AuditCreate, db: Session = Depends(get_db)):
    # Check if property exists
    property_obj = db.query(Property).filter(Property.id == audit_data.property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    audit = Audit(
        property_id=audit_data.property_id,
        auditor_id=audit_data.auditor_id,
        reviewer_id=audit_data.reviewer_id,
        hotel_group_id=property_obj.hotel_group_id,
        sop=audit_data.sop,
        sop_files=audit_data.sop_files,
        status="scheduled"
    )
    
    db.add(audit)
    db.commit()
    db.refresh(audit)
    
    return {
        "id": audit.id,
        "property_id": audit.property_id,
        "property_name": audit.property.name,
        "property_location": audit.property.location,
        "hotel_group_name": audit.hotel_group.name,
        "auditor_id": audit.auditor_id,
        "auditor_name": audit.auditor.name if audit.auditor else None,
        "reviewer_id": audit.reviewer_id,
        "reviewer_name": audit.reviewer.name if audit.reviewer else None,
        "status": audit.status,
        "overall_score": audit.overall_score,
        "cleanliness_score": audit.cleanliness_score,
        "branding_score": audit.branding_score,
        "operational_score": audit.operational_score,
        "compliance_zone": audit.compliance_zone,
        "findings": audit.findings,
        "action_plan": audit.action_plan,
        "submitted_at": audit.submitted_at,
        "reviewed_at": audit.reviewed_at,
        "created_at": audit.created_at
    }

@router.put("/{audit_id}", response_model=AuditResponse)
async def update_audit(audit_id: int, audit_updates: dict, db: Session = Depends(get_db)):
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    # Update fields
    for field, value in audit_updates.items():
        if hasattr(audit, field) and value is not None:
            setattr(audit, field, value)
    
    if audit_updates.get('status') == 'submitted':
        audit.submitted_at = datetime.utcnow()
    elif audit_updates.get('status') == 'reviewed':
        audit.reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(audit)
    
    return {
        "id": audit.id,
        "property_id": audit.property_id,
        "property_name": audit.property.name,
        "property_location": audit.property.location,
        "hotel_group_name": audit.hotel_group.name,
        "auditor_id": audit.auditor_id,
        "auditor_name": audit.auditor.name if audit.auditor else None,
        "reviewer_id": audit.reviewer_id,
        "reviewer_name": audit.reviewer.name if audit.reviewer else None,
        "status": audit.status,
        "overall_score": audit.overall_score,
        "cleanliness_score": audit.cleanliness_score,
        "branding_score": audit.branding_score,
        "operational_score": audit.operational_score,
        "compliance_zone": audit.compliance_zone,
        "findings": audit.findings,
        "action_plan": audit.action_plan,
        "submitted_at": audit.submitted_at,
        "reviewed_at": audit.reviewed_at,
        "created_at": audit.created_at
    }

@router.get("/{audit_id}/items", response_model=List[AuditItemResponse])
async def get_audit_items(audit_id: int, db: Session = Depends(get_db)):
    items = db.query(AuditItem).filter(AuditItem.audit_id == audit_id).all()
    
    result = []
    for item in items:
        result.append({
            "id": item.id,
            "audit_id": item.audit_id,
            "category": item.category,
            "item": item.item,
            "score": item.score,
            "comments": item.comments,
            "ai_analysis": item.ai_analysis,
            "photos": item.photos,
            "status": item.status
        })
    
    return result

@router.post("/{audit_id}/items", response_model=AuditItemResponse)
async def create_audit_item(audit_id: int, item_data: AuditItemCreate, db: Session = Depends(get_db)):
    # Check if audit exists
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    item = AuditItem(
        audit_id=audit_id,
        category=item_data.category,
        item=item_data.item,
        score=item_data.score,
        comments=item_data.comments,
        photos=item_data.photos
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return {
        "id": item.id,
        "audit_id": item.audit_id,
        "category": item.category,
        "item": item.item,
        "score": item.score,
        "comments": item.comments,
        "ai_analysis": item.ai_analysis,
        "photos": item.photos,
        "status": item.status
    }

@router.put("/items/{item_id}", response_model=AuditItemResponse)
async def update_audit_item(item_id: int, item_updates: dict, db: Session = Depends(get_db)):
    item = db.query(AuditItem).filter(AuditItem.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Audit item not found")
    
    # Update fields
    for field, value in item_updates.items():
        if hasattr(item, field) and value is not None:
            setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return {
        "id": item.id,
        "audit_id": item.audit_id,
        "category": item.category,
        "item": item.item,
        "score": item.score,
        "comments": item.comments,
        "ai_analysis": item.ai_analysis,
        "photos": item.photos,
        "status": item.status
    }