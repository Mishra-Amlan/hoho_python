from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    name: str
    email: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Hotel Group schemas
class HotelGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None

class HotelGroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Property schemas
class PropertyCreate(BaseModel):
    name: str
    location: str
    hotel_group_id: int
    manager_name: Optional[str] = None
    manager_email: Optional[str] = None
    phone: Optional[str] = None

class PropertyResponse(BaseModel):
    id: int
    name: str
    location: str
    hotel_group_id: int
    manager_name: Optional[str] = None
    manager_email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Audit schemas
class AuditCreate(BaseModel):
    property_id: int
    auditor_id: int
    scheduled_date: Optional[datetime] = None

class AuditUpdate(BaseModel):
    status: Optional[str] = None
    overall_score: Optional[float] = None
    reviewer_id: Optional[int] = None

class AuditResponse(BaseModel):
    id: int
    property_id: int
    auditor_id: int
    reviewer_id: Optional[int] = None
    status: str
    overall_score: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Audit Item schemas
class AuditItemCreate(BaseModel):
    audit_id: int
    category: str
    item_name: str
    description: Optional[str] = None

class AuditItemUpdate(BaseModel):
    score: Optional[float] = None
    ai_score: Optional[float] = None
    ai_feedback: Optional[str] = None
    auditor_comments: Optional[str] = None
    reviewer_comments: Optional[str] = None
    photo_url: Optional[str] = None
    is_compliant: Optional[bool] = None

class AuditItemResponse(BaseModel):
    id: int
    audit_id: int
    category: str
    item_name: str
    description: Optional[str] = None
    score: Optional[float] = None
    ai_score: Optional[float] = None
    ai_feedback: Optional[str] = None
    auditor_comments: Optional[str] = None
    reviewer_comments: Optional[str] = None
    photo_url: Optional[str] = None
    is_compliant: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# AI Analysis schemas
class AIAnalysisRequest(BaseModel):
    item_name: str
    description: str
    photo_url: Optional[str] = None
    category: str

class AIAnalysisResponse(BaseModel):
    score: float
    feedback: str
    is_compliant: bool
    confidence: float

# Photo Analysis schemas
class PhotoAnalysisRequest(BaseModel):
    image_data: str
    context: Optional[str] = None

class PhotoAnalysisResponse(BaseModel):
    analysis: dict
    suggested_score: float
    confidence: float

# Report Generation schemas  
class ReportGenerationRequest(BaseModel):
    audit_id: int
    format: Optional[str] = "pdf"

class ReportGenerationResponse(BaseModel):
    report_url: str
    status: str

# Score Suggestion schemas
class ScoreSuggestionRequest(BaseModel):
    item_name: str
    description: str
    photo_url: Optional[str] = None

class ScoreSuggestionResponse(BaseModel):
    suggested_score: float
    reasoning: str
    confidence: float