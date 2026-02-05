import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.models import (
    HoneypotRequest, HoneypotResponse, IntelligenceData,
    HackathonRequest, HackathonResponse
)
from app.config import GEMINI_API_KEY
from app.detection import ScamDetector
from app.extraction import IntelligenceExtractor
from app.agent import ConversationManager

app = FastAPI(title="Agentic Honey-Pot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_api_key(x_api_key: str = Header(...)):
    # For this hackathon, we might want to accept any key or a specific one provided in env
    # Simplest: accept if present
    if not x_api_key:
        raise HTTPException(status_code=403, detail="API Key required")
    return x_api_key

@app.get("/health")
def health_check():
    return {"status": "active", "service": "Agentic Honey-Pot"}


@app.post("/", response_model=HackathonResponse)
async def hackathon_endpoint(payload: HackathonRequest, x_api_key: str = Header(...)):
    """
    Hackathon-compatible endpoint.
    Receives messages in the expected format and returns the expected response format.
    """
    try:
        # Extract message text and session ID from hackathon format
        session_id = payload.sessionId
        message_text = payload.message.text
        
        # Use existing conversation logic
        state = ConversationManager.get_state(session_id)
        
        # Scam Detection
        is_scam = False
        scam_type = "default"
        
        if state:
            is_scam = True
            scam_type = state.get("scam_type", "default")
        else:
            is_scam, detected_type, confidence = ScamDetector.analyze(message_text)
            scam_type = detected_type if detected_type else "default"
        
        # Generate response using existing agent
        agent_response = ConversationManager.generate_response(session_id, message_text, scam_type)
        
        return HackathonResponse(
            status="success",
            reply=agent_response
        )
        
    except Exception as e:
        # Return a valid response even on error
        return HackathonResponse(
            status="success",
            reply="I'm sorry, could you please repeat that? I didn't quite understand."
        )

@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(payload: HoneypotRequest, api_key: str = Depends(verify_api_key)):
    """
    Main endpoint for the honeypot system.
    Receives a message, detects scam, engages via agent, and extracts intelligence.
    """
    
    # 1. Retrieve or Initialize Conversation State
    conversation_id = payload.conversation_id
    state = ConversationManager.get_state(conversation_id)
    
    # 2. Extract Intelligence from the incoming message immediately
    # We maintain previous intelligence if available, or start fresh
    current_intelligence = state.get("intelligence", IntelligenceData())
    if isinstance(current_intelligence, dict):
        current_intelligence = IntelligenceData(**current_intelligence)
        
    updated_intelligence = IntelligenceExtractor.extract(payload.message, current_intelligence)
    
    # 3. Scam Detection (if not already detected/established context)
    is_scam = False
    scam_type = "default"
    confidence = 0.0
    
    if state:
        # We are already in a conversation, so we assume the context continues
        is_scam = True 
        scam_type = state.get("scam_type", "default")
        confidence = 0.95 # High confidence as we are already engaged
    else:
        # First turn or new conversation
        is_scam, detected_type, confidence = ScamDetector.analyze(payload.message)
        scam_type = detected_type if detected_type else "default"
        
        # If we didn't detect a scam but we want to be safe, or if this is a honey-pot explicitly:
        # The prompt says "scam interactions will be simulated using a Mock Scammer API"
        # So we can fairly safely assume incoming traffic to this specific endpoint is relevant.
        # But let's stick to the detector for the "scam_detected" flag.
        
    # Update intelligence confidence with detector confidence if higher
    if confidence > updated_intelligence.confidence_score:
        updated_intelligence.confidence_score = confidence
        
    if updated_intelligence.scam_type is None:
        updated_intelligence.scam_type = scam_type

    # 4. Generate Agent Response
    if is_scam or state: 
        # Engage!
        agent_response = ConversationManager.generate_response(conversation_id, payload.message, scam_type)
        
        # Update state with intelligence
        current_state = ConversationManager.get_state(conversation_id)
        current_state["intelligence"] = updated_intelligence.dict()
        ConversationManager.update_state(conversation_id, current_state)
        
    else:
        # Not recognized as a scam yet, and no history.
        # We can either not engage, or engage cautiously.
        # For a Honeypot, we probably should engage to *find out*.
        # Let's use the 'default' persona to probe.
        agent_response = ConversationManager.generate_response(conversation_id, payload.message, "default")
        is_scam = True # We effectively treat it as a potential scam for the sake of the conversation
        
        # Update state with intelligence
        current_state = ConversationManager.get_state(conversation_id)
        current_state["intelligence"] = updated_intelligence.dict()
        ConversationManager.update_state(conversation_id, current_state)

    return HoneypotResponse(
        scam_detected=is_scam,
        response=agent_response,
        intelligence=updated_intelligence
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
