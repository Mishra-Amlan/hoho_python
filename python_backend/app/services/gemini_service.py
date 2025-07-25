"""
Gemini AI Service for Hotel Audit Analysis
"""

import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini AI service initialized")
        else:
            logger.warning("⚠️ Gemini API key not found - AI features disabled")
            self.model = None
    
    async def analyze_audit_photo(self, image_data: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze audit photo using Gemini Vision"""
        if not self.model:
            return {
                "analysis": "AI analysis unavailable - no API key",
                "suggested_score": 3,
                "confidence": 0.0
            }
        
        try:
            prompt = f"""
            Analyze this hotel audit photo and provide:
            1. Overall assessment
            2. Compliance issues identified
            3. Suggested score (0-5 scale)
            4. Recommendations for improvement
            
            Context: {context or "General hotel audit item"}
            
            Please provide a structured analysis in JSON format.
            """
            
            # For demo purposes, return mock analysis
            return {
                "analysis": "Photo shows good condition with minor issues",
                "suggested_score": 4.2,
                "compliance_issues": ["Minor wear on surfaces"],
                "recommendations": ["Regular maintenance recommended"]
            }
            
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return {
                "analysis": f"Analysis failed: {str(e)}",
                "suggested_score": 3,
                "confidence": 0.0
            }
    
    async def suggest_score(self, item_name: str, description: str, photo_url: Optional[str] = None) -> Dict[str, Any]:
        """Get AI-suggested score for audit item"""
        if not self.model:
            return {
                "suggested_score": 3.0,
                "reasoning": "AI service unavailable",
                "confidence": 0.0
            }
        
        try:
            prompt = f"""
            Analyze this hotel audit item and suggest a score (0-5 scale):
            
            Item: {item_name}
            Description: {description}
            
            Consider standard hotel audit criteria and provide:
            1. Suggested score (0-5)
            2. Reasoning for the score
            3. Key factors considered
            """
            
            # For demo purposes, return mock response
            return {
                "suggested_score": 4.0,
                "reasoning": f"Item '{item_name}' meets most standards with minor improvements needed",
                "confidence": 0.85
            }
            
        except Exception as e:
            logger.error(f"Score suggestion failed: {e}")
            return {
                "suggested_score": 3.0,
                "reasoning": f"Analysis failed: {str(e)}",
                "confidence": 0.0
            }

# Global instance
gemini_service = GeminiService()