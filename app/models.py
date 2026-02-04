from pydantic import BaseModel
from typing import Optional, Dict, List, Any

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
