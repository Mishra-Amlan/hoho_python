from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.models import Audit, AuditItem
from app.schemas.schemas import (
    PhotoAnalysisRequest, PhotoAnalysisResponse,
    ReportGenerationRequest, ReportGenerationResponse,
    ScoreSuggestionRequest, ScoreSuggestionResponse
)
from app.services.gemini_service import gemini_service

router = APIRouter()

@router.post("/analyze-photo", response_model=PhotoAnalysisResponse)
async def analyze_photo(
    request: PhotoAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze a photo using Gemini Vision AI"""
    try:
        analysis = await gemini_service.analyze_audit_photo(
            request.image_data,
            request.context
        )
        
        return PhotoAnalysisResponse(
            analysis=analysis,
            suggested_score=analysis.get("suggested_score", 3),
            confidence=0.85
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze photo: {str(e)}")

@router.post("/suggest-score", response_model=ScoreSuggestionResponse)
async def suggest_score(
    request: ScoreSuggestionRequest,
    db: Session = Depends(get_db)
):
    """Get AI-suggested score for an audit item"""
    try:
        suggestion = await gemini_service.suggest_score(
            request.item_name,
            request.description,
            request.photo_url
        )
        
        return ScoreSuggestionResponse(
            suggested_score=suggestion.get("suggested_score", 3),
            reasoning=suggestion.get("reasoning", "Analysis based on provided information"),
            confidence=suggestion.get("confidence", 0.85)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to suggest score: {str(e)}")

@router.post("/generate-report", response_model=ReportGenerationResponse)
async def generate_report(
    request: ReportGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate comprehensive audit report"""
    # Get audit with all related data
    audit = db.query(Audit).filter(Audit.id == request.audit_id).first()
    
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    try:
        # For demo purposes, return a mock report URL
        report_url = f"/reports/audit_{request.audit_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return ReportGenerationResponse(
            report_url=report_url,
            status="generated"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")