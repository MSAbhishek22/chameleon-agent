import re
from typing import Tuple, Optional

class ScamDetector:
    """
    Analyzes messages to detect scam intent and classify the type of scam.
    Uses a combination of keyword matching and pattern recognition.
    """
    
    # Keywords for different scam types
    SCAM_KEYWORDS = {
        "tech_support": [
            r"microsoft", r"windows", r"virus", r"defender", r"computer blocked",
            r"technical support", r"customer care", r"remote access", r"anydesk", r"teamviewer"
        ],
        "financial": [
            r"kyc", r"pan card", r"aadhar", r"bank account", r"blocked", r"expire",
            r"update", r"verify", r"credit card", r"debit card", r"otp", r"cvv"
        ],
        "lottery": [
            r"won", r"prize", r"lottery", r"lucky draw", r"winner", r"claim",
            r"crore", r"lakh", r"kbc", r"congratulations"
        ],
        "job": [
            r"part time", r"job", r"hiring", r"work from home", r"salary",
            r"income", r"daily payment", r"investment", r"crypto", r"telegram"
        ],
        "romance": [
            r"love", r"beautiful", r"friendship", r"dear", r"gift", r"customs",
            r"airport", r"parcel"
        ]
    }

    @classmethod
    def analyze(cls, message: str) -> Tuple[bool, Optional[str], float]:
        """
        Analyzes a message to determine if it's a scam and what type.
        Returns: (is_scam, scam_type, confidence_score)
        """
        message_lower = message.lower()
        
        detected_types = {}
        
        for scam_type, patterns in cls.SCAM_KEYWORDS.items():
            count = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    count += 1
            if count > 0:
                detected_types[scam_type] = count

        if not detected_types:
            # Fallback: check for general urgency/suspicious patterns if no specific type found
            # For hackathon, we might assume most inputs to the honeypot are scams
            # But let's return False for now if nothing matches to be safe, or default to a generic one
            # Given the context is a "Honey-Pot", we can be aggressive.
            return False, None, 0.0

        # Get the scam type with the most keyword matches
        best_match = max(detected_types, key=detected_types.get)
        confidence = min(0.5 + (detected_types[best_match] * 0.1), 0.95) # Cap at 0.95

        return True, best_match, confidence
