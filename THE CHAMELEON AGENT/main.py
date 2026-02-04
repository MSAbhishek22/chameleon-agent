"""
Chameleon Agent - Main FastAPI Application
Agentic Honey-Pot for Scam Detection & Intelligence Extraction
"""

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our modules (will create these next)
from src.detection.scam_detector import ScamDetector
from src.personas.persona_manager import PersonaManager
from src.agent.conversation_manager import ConversationManager
from src.extraction.entity_extractor import EntityExtractor
from src.api.response_models import HoneypotResponse

# Initialize FastAPI app
app = FastAPI(
    title="Chameleon Agent - Agentic Honey-Pot",
    description="AI-powered honeypot for scam detection and intelligence extraction",
    version="1.0.0"
)

# Initialize components
scam_detector = ScamDetector()
persona_manager = PersonaManager()
conversation_manager = ConversationManager()
entity_extractor = EntityExtractor()

# API Key from environment
HONEYPOT_API_KEY = os.getenv("HONEYPOT_API_KEY", "default_key_change_me")


# Request Models
class ConversationMessage(BaseModel):
    role: str = Field(..., description="Role: 'scammer' or 'agent'")
    content: str = Field(..., description="Message content")


class HoneypotRequest(BaseModel):
    message: str = Field(..., description="Incoming scammer message")
    conversation_id: str = Field(..., description="Unique conversation identifier")
    history: Optional[List[ConversationMessage]] = Field(default=[], description="Conversation history")


# Middleware for API Key Authentication
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    """Verify API key for all requests except health check"""
    if request.url.path == "/health":
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        return JSONResponse(
            status_code=401,
            content={"error": "Missing API key. Include X-API-Key header."}
        )
    
    if api_key != HONEYPOT_API_KEY:
        return JSONResponse(
            status_code=403,
            content={"error": "Invalid API key"}
        )
    
    return await call_next(request)


# Health Check Endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "chameleon-agent",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# Main Honeypot Endpoint
@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(request: HoneypotRequest):
    """
    Main honeypot endpoint that processes scam messages and returns agent responses
    with extracted intelligence.
    """
    try:
        logger.info(f"Processing conversation: {request.conversation_id}")
        
        # Step 1: Detect scam intent and type
        scam_analysis = scam_detector.analyze(request.message, request.history)
        
        logger.info(f"Scam detected: {scam_analysis['is_scam']}, Type: {scam_analysis.get('scam_type')}, Confidence: {scam_analysis.get('confidence')}")
        
        # Step 2: Select appropriate persona based on scam type
        persona = persona_manager.select_persona(scam_analysis['scam_type'])
        
        # Step 3: Generate agent response using conversation manager
        agent_response = await conversation_manager.generate_response(
            message=request.message,
            conversation_id=request.conversation_id,
            history=request.history,
            persona=persona,
            scam_type=scam_analysis['scam_type'],
            turn_count=len(request.history) + 1
        )
        
        # Step 4: Extract intelligence from conversation history + new message
        all_messages = [msg.content for msg in request.history] + [request.message, agent_response]
        extracted_intelligence = entity_extractor.extract(all_messages)
        
        # Step 5: Calculate engagement metrics
        engagement_metrics = {
            "turn_count": len(request.history) + 1,
            "engagement_duration_seconds": (len(request.history) + 1) * 15,  # Estimate
            "persona_used": persona.name,
            "extraction_success_rate": extracted_intelligence.get("extraction_count", 0) / max(len(request.history), 1)
        }
        
        # Step 6: Build response
        response = HoneypotResponse(
            scam_detected=scam_analysis['is_scam'],
            scam_type=scam_analysis.get('scam_type', 'unknown'),
            confidence=scam_analysis.get('confidence', 0.0),
            agent_response=agent_response,
            extracted_intelligence=extracted_intelligence.get('extracted_data', {}),
            engagement_metrics=engagement_metrics,
            metadata={
                "conversation_id": request.conversation_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model_version": "chameleon-v1.0"
            }
        )
        
        logger.info(f"Response generated successfully for {request.conversation_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Chameleon Agent - Agentic Honey-Pot",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "honeypot": "POST /honeypot",
            "docs": "/docs"
        },
        "description": "AI-powered honeypot for scam detection and intelligence extraction"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )
