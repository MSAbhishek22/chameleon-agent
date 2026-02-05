from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any


# --- Hackathon-specific models (expected format) ---
class MessagePayload(BaseModel):
    sender: str
    text: str
    timestamp: int


class MetadataPayload(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None


class HackathonRequest(BaseModel):
    sessionId: str
    message: MessagePayload
    conversationHistory: List[Dict[str, Any]] = []
    metadata: Optional[MetadataPayload] = None


class HackathonResponse(BaseModel):
    status: str = "success"
    reply: str


# --- Original internal models ---
class HoneypotRequest(BaseModel):
    conversation_id: str
    message: str

class IntelligenceData(BaseModel):
    scam_type: Optional[str] = None
    bank_account: Optional[str] = None
    upi_id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    url: Optional[str] = None
    confidence_score: float = 0.0

class HoneypotResponse(BaseModel):
    scam_detected: bool
    response: str
    intelligence: IntelligenceData
