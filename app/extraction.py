import re
from typing import Dict, Optional
from app.models import IntelligenceData

class IntelligenceExtractor:
    """
    Extracts structured intelligence from messages using regex patterns.
    Targets Indian banking entities, contacts, and digital footprints.
    """

    PATTERNS = {
        "upi_id": r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}",
        # Indian Bank Account: Usually 9-18 digits (e.g., SBI is 11, HDFC is 14)
        "bank_account": r"\b\d{9,18}\b",
        # IFSC Code: 4 letters, 0, 6 alphanumeric
        "ifsc": r"[A-Z]{4}0[A-Z0-9]{6}",
        "phone_number": r"(\+91[\-\s]?)?[6-9]\d{9}",
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "url": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*"
    }

    @classmethod
    def extract(cls, message: str, current_data: IntelligenceData) -> IntelligenceData:
        """
        Scans values and updates the IntelligenceData object if new info is found.
        """
        # We only update fields if they are not already set, or if we find new info.
        # For simplicity, we overwrite if found, assuming latest is most relevant, 
        # or we could keep a list. The Hackathon spec asks for "extracted intelligence", 
        # implying single values or a set. The model has single fields.

        extracted = current_data.dict()
        
        for key, pattern in cls.PATTERNS.items():
            match = re.search(pattern, message)
            if match:
                value = match.group(0)
                # Simple heuristic: if we found something and it's not already stored
                if not extracted.get(key):
                     extracted[key] = value

        # Update confidence based on what we found
        # If we have bank details or UPI, confidence is very high
        confidence = extracted.get("confidence_score", 0.0)
        if extracted.get("bank_account") or extracted.get("upi_id"):
            confidence = max(confidence, 0.95)
        elif extracted.get("phone_number") or extracted.get("url"):
             confidence = max(confidence, 0.8)
        
        extracted["confidence_score"] = confidence

        return IntelligenceData(**extracted)
