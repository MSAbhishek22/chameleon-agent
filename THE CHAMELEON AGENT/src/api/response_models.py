"""
API Response Models
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class BankAccountData(BaseModel):
    """Bank account information"""
    account_number: str
    ifsc_code: Optional[str] = None
    account_holder: Optional[str] = None
    confidence: float


class UPIData(BaseModel):
    """UPI ID information"""
    upi_id: str
    confidence: float


class PhoneNumberData(BaseModel):
    """Phone number information"""
    number: str
    confidence: float


class URLData(BaseModel):
    """URL/Link information"""
    url: str
    domain: Optional[str] = None
    confidence: float


class NameData(BaseModel):
    """Name information"""
    name: str
    confidence: float


class ExtractedIntelligence(BaseModel):
    """Extracted intelligence from conversation"""
    bank_accounts: Optional[List[BankAccountData]] = []
    upi_ids: Optional[List[UPIData]] = []
    phone_numbers: Optional[List[PhoneNumberData]] = []
    urls: Optional[List[URLData]] = []
    names: Optional[List[NameData]] = []


class EngagementMetrics(BaseModel):
    """Engagement metrics for the conversation"""
    turn_count: int
    engagement_duration_seconds: int
    persona_used: str
    extraction_success_rate: float


class HoneypotResponse(BaseModel):
    """Main API response model"""
    scam_detected: bool = Field(..., description="Whether scam was detected")
    scam_type: str = Field(..., description="Type of scam detected")
    confidence: float = Field(..., description="Confidence score (0.0-1.0)")
    agent_response: str = Field(..., description="Agent's response message")
    extracted_intelligence: Dict[str, Any] = Field(default={}, description="Extracted intelligence")
    engagement_metrics: EngagementMetrics = Field(..., description="Engagement metrics")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
