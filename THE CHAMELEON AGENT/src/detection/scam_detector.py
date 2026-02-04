"""
Scam Detection Engine
Analyzes messages to detect scam intent and classify scam type
"""

import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class ScamDetector:
    """
    Multi-signal scam detection engine that classifies scam types
    and calculates confidence scores
    """
    
    def __init__(self):
        # Scam type keywords and patterns
        self.scam_patterns = {
            "tech_support": {
                "keywords": [
                    "microsoft", "windows", "computer", "virus", "antivirus", "mcafee",
                    "norton", "google", "amazon", "tech support", "technical support",
                    "computer problem", "laptop", "pc", "software", "license expired",
                    "security alert", "malware", "spyware", "infected"
                ],
                "patterns": [
                    r"your (computer|pc|laptop|device) (has|is) (infected|compromised)",
                    r"(virus|malware) detected",
                    r"call (us|our) (tech|technical) support"
                ]
            },
            "financial": {
                "keywords": [
                    "bank", "account", "kyc", "pan", "aadhaar", "aadhar", "blocked",
                    "suspended", "verify", "update", "income tax", "tax department",
                    "rbi", "reserve bank", "sbi", "hdfc", "icici", "axis", "debit card",
                    "credit card", "atm", "transaction", "fraud", "unauthorized",
                    "refund", "payment", "upi", "paytm", "phonepe", "gpay"
                ],
                "patterns": [
                    r"(account|card) (is|has been) (blocked|suspended|frozen)",
                    r"update (your|ur) kyc",
                    r"verify (your|ur) (pan|aadhaar|account)",
                    r"income tax (department|notice|refund)"
                ]
            },
            "prize": {
                "keywords": [
                    "congratulations", "won", "winner", "prize", "lottery", "lakh",
                    "crore", "rupees", "reward", "gift", "lucky", "selected", "claim",
                    "kbc", "kaun banega crorepati", "lucky draw", "contest", "free",
                    "iphone", "car", "bike", "cash prize"
                ],
                "patterns": [
                    r"(congratulations|congrats).*(won|winner)",
                    r"won.*(lakh|crore|rupees|\d+)",
                    r"claim (your|ur) (prize|reward|gift)",
                    r"lucky draw"
                ]
            },
            "romance": {
                "keywords": [
                    "hello dear", "hi sweetheart", "love", "lonely", "friend",
                    "relationship", "marry", "marriage", "beautiful", "handsome",
                    "miss you", "thinking of you", "alone", "companion"
                ],
                "patterns": [
                    r"(hello|hi) (dear|sweetheart|darling)",
                    r"looking for (love|relationship|friendship)",
                    r"are you (single|alone|lonely)"
                ]
            },
            "job": {
                "keywords": [
                    "job", "work from home", "earn", "income", "salary", "part time",
                    "full time", "hiring", "vacancy", "opportunity", "investment",
                    "trading", "forex", "crypto", "bitcoin", "stock market",
                    "registration fee", "training fee", "deposit", "guaranteed income",
                    "easy money", "no experience"
                ],
                "patterns": [
                    r"work from home.*(earn|income|\d+)",
                    r"earn.*(lakh|thousand|rupees|\d+).*(month|day|week)",
                    r"(registration|training|deposit) fee",
                    r"guaranteed (income|returns|profit)"
                ]
            }
        }
        
        # Urgency indicators (boost scam confidence)
        self.urgency_patterns = [
            r"(urgent|immediately|now|today|within \d+ (hours|minutes))",
            r"(limited time|offer expires|last chance)",
            r"(act now|hurry|quick|fast)"
        ]
        
        # Authority claims (boost scam confidence)
        self.authority_patterns = [
            r"(government|official|department|ministry|police|cyber crime|cbi)",
            r"(rbi|reserve bank|income tax|tax department)",
            r"(authorized|verified|certified|registered)"
        ]
        
        # Action requests (boost scam confidence)
        self.action_patterns = [
            r"(click|tap|open) (this|the) (link|url)",
            r"(share|send|provide|give) (your|ur) (otp|password|pin|cvv)",
            r"(transfer|pay|send) (money|amount|rupees|\d+)",
            r"(download|install) (this|the) (app|application|software)",
            r"call (us|this number|back)"
        ]
    
    def analyze(self, message: str, history: List[Any] = None) -> Dict[str, Any]:
        """
        Analyze a message to detect scam intent and classify type
        
        Args:
            message: The incoming message to analyze
            history: Optional conversation history for context
            
        Returns:
            Dict with is_scam, scam_type, confidence, and signals_detected
        """
        message_lower = message.lower()
        
        # Calculate scores for each scam type
        scam_scores = {}
        for scam_type, patterns in self.scam_patterns.items():
            score = self._calculate_scam_score(message_lower, patterns)
            scam_scores[scam_type] = score
        
        # Get the highest scoring scam type
        max_scam_type = max(scam_scores, key=scam_scores.get)
        max_score = scam_scores[max_scam_type]
        
        # Detect additional signals
        signals = []
        
        # Check for urgency
        if any(re.search(pattern, message_lower) for pattern in self.urgency_patterns):
            signals.append("urgency")
            max_score += 0.1
        
        # Check for authority claims
        if any(re.search(pattern, message_lower) for pattern in self.authority_patterns):
            signals.append("authority_claim")
            max_score += 0.15
        
        # Check for action requests
        if any(re.search(pattern, message_lower) for pattern in self.action_patterns):
            signals.append("action_request")
            max_score += 0.15
        
        # Normalize confidence to 0-1 range
        confidence = min(max_score, 1.0)
        
        # Determine if it's a scam (threshold: 0.3)
        is_scam = confidence >= 0.3
        
        result = {
            "is_scam": is_scam,
            "scam_type": max_scam_type if is_scam else None,
            "confidence": round(confidence, 2),
            "signals_detected": signals,
            "all_scores": {k: round(v, 2) for k, v in scam_scores.items()}
        }
        
        logger.debug(f"Scam analysis result: {result}")
        return result
    
    def _calculate_scam_score(self, message: str, patterns: Dict[str, List[str]]) -> float:
        """Calculate scam score for a specific scam type"""
        score = 0.0
        
        # Keyword matching (each keyword adds 0.1, max 0.5)
        keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in message)
        score += min(keyword_matches * 0.1, 0.5)
        
        # Pattern matching (each pattern adds 0.2, max 0.6)
        pattern_matches = sum(1 for pattern in patterns["patterns"] if re.search(pattern, message))
        score += min(pattern_matches * 0.2, 0.6)
        
        return score
