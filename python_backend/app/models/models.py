from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, auditor, reviewer, corporate, hotel_gm
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HotelGroup(Base):
    __tablename__ = "hotel_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    properties = relationship("Property", back_populates="hotel_group")

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    hotel_group_id = Column(Integer, ForeignKey("hotel_groups.id"))
    manager_name = Column(String(100))
    manager_email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    hotel_group = relationship("HotelGroup", back_populates="properties")
    audits = relationship("Audit", back_populates="property")

class Audit(Base):
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    auditor_id = Column(Integer, ForeignKey("users.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="pending")  # pending, in_progress, submitted, approved, rejected
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scheduled_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    
    # Relationships
    property = relationship("Property", back_populates="audits")
    auditor = relationship("User", foreign_keys=[auditor_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    audit_items = relationship("AuditItem", back_populates="audit")

class AuditItem(Base):
    __tablename__ = "audit_items"
    
    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("audits.id"))
    category = Column(String(100), nullable=False)
    item_name = Column(String(255), nullable=False)
    description = Column(Text)
    score = Column(Float, nullable=True)  # 0-5 scale
    ai_score = Column(Float, nullable=True)  # AI generated score
    ai_feedback = Column(Text, nullable=True)  # AI analysis feedback
    auditor_comments = Column(Text, nullable=True)
    reviewer_comments = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)
    is_compliant = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    audit = relationship("Audit", back_populates="audit_items")