"""
Test Scam Detection Engine
"""

import pytest
from src.detection.scam_detector import ScamDetector


@pytest.fixture
def detector():
    return ScamDetector()


def test_tech_support_scam_detection(detector):
    """Test detection of tech support scams"""
    message = "Your computer has been infected with virus. Call Microsoft tech support immediately."
    result = detector.analyze(message)
    
    assert result["is_scam"] == True
    assert result["scam_type"] == "tech_support"
    assert result["confidence"] >= 0.5


def test_financial_scam_detection(detector):
    """Test detection of financial scams"""
    message = "Your bank account has been blocked. Update your KYC immediately to avoid penalties."
    result = detector.analyze(message)
    
    assert result["is_scam"] == True
    assert result["scam_type"] == "financial"
    assert result["confidence"] >= 0.5


def test_prize_scam_detection(detector):
    """Test detection of prize/lottery scams"""
    message = "Congratulations! You have won 5 lakh rupees in KBC lottery. Claim your prize now!"
    result = detector.analyze(message)
    
    assert result["is_scam"] == True
    assert result["scam_type"] == "prize"
    assert result["confidence"] >= 0.5


def test_job_scam_detection(detector):
    """Test detection of job/investment scams"""
    message = "Work from home and earn 50,000 per month. Just pay 2,000 registration fee."
    result = detector.analyze(message)
    
    assert result["is_scam"] == True
    assert result["scam_type"] == "job"
    assert result["confidence"] >= 0.5


def test_romance_scam_detection(detector):
    """Test detection of romance scams"""
    message = "Hello dear, I am looking for a serious relationship. Are you single?"
    result = detector.analyze(message)
    
    assert result["is_scam"] == True
    assert result["scam_type"] == "romance"
    assert result["confidence"] >= 0.3


def test_urgency_signal_detection(detector):
    """Test detection of urgency signals"""
    message = "Your account will be closed in 2 hours. Act immediately!"
    result = detector.analyze(message)
    
    assert "urgency" in result["signals_detected"]


def test_authority_signal_detection(detector):
    """Test detection of authority claims"""
    message = "This is official message from Income Tax Department."
    result = detector.analyze(message)
    
    assert "authority_claim" in result["signals_detected"]


def test_action_request_detection(detector):
    """Test detection of action requests"""
    message = "Click this link and share your OTP to verify your account."
    result = detector.analyze(message)
    
    assert "action_request" in result["signals_detected"]


def test_non_scam_message(detector):
    """Test that normal messages are not flagged as scams"""
    message = "Hi, how are you? Let's meet for coffee tomorrow."
    result = detector.analyze(message)
    
    # Should have low confidence or not be detected as scam
    assert result["confidence"] < 0.3 or result["is_scam"] == False


def test_mixed_language_scam(detector):
    """Test detection with Hindi-English code-mixing"""
    message = "Aapka account block ho gaya hai. Please update your KYC immediately."
    result = detector.analyze(message)
    
    assert result["is_scam"] == True
    assert result["scam_type"] == "financial"
