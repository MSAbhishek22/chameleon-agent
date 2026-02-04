"""
Test Entity Extraction
"""

import pytest
from src.extraction.entity_extractor import EntityExtractor


@pytest.fixture
def extractor():
    return EntityExtractor()


def test_bank_account_extraction(extractor):
    """Test extraction of bank account numbers"""
    messages = [
        "Please transfer money to account number 12345678901",
        "IFSC code is SBIN0001234"
    ]
    result = extractor.extract(messages)
    
    assert "bank_accounts" in result["extracted_data"]
    assert len(result["extracted_data"]["bank_accounts"]) > 0
    assert result["extracted_data"]["bank_accounts"][0]["account_number"] == "12345678901"


def test_upi_extraction(extractor):
    """Test extraction of UPI IDs"""
    messages = ["Send payment to 9876543210@paytm"]
    result = extractor.extract(messages)
    
    assert "upi_ids" in result["extracted_data"]
    assert len(result["extracted_data"]["upi_ids"]) > 0
    assert "9876543210@paytm" in result["extracted_data"]["upi_ids"][0]["upi_id"]


def test_phone_number_extraction(extractor):
    """Test extraction of phone numbers"""
    messages = ["Call me at 9876543210 for more details"]
    result = extractor.extract(messages)
    
    assert "phone_numbers" in result["extracted_data"]
    assert len(result["extracted_data"]["phone_numbers"]) > 0
    assert result["extracted_data"]["phone_numbers"][0]["number"] == "9876543210"


def test_url_extraction(extractor):
    """Test extraction of URLs"""
    messages = ["Click this link: https://fake-bank-login.com/verify"]
    result = extractor.extract(messages)
    
    assert "urls" in result["extracted_data"]
    assert len(result["extracted_data"]["urls"]) > 0
    assert "fake-bank-login.com" in result["extracted_data"]["urls"][0]["url"]


def test_name_extraction(extractor):
    """Test extraction of names"""
    messages = ["Account holder name is Ramesh Kumar"]
    result = extractor.extract(messages)
    
    assert "names" in result["extracted_data"]
    assert len(result["extracted_data"]["names"]) > 0


def test_multiple_entities_extraction(extractor):
    """Test extraction of multiple entity types"""
    messages = [
        "Transfer to account 12345678901, IFSC SBIN0001234",
        "Or use UPI: scammer@paytm",
        "Call 9876543210 if you have issues"
    ]
    result = extractor.extract(messages)
    
    assert result["extraction_count"] >= 3
    assert "bank_accounts" in result["extracted_data"]
    assert "upi_ids" in result["extracted_data"]
    assert "phone_numbers" in result["extracted_data"]


def test_confidence_scoring(extractor):
    """Test that confidence scores are calculated"""
    messages = ["UPI: test@paytm"]
    result = extractor.extract(messages)
    
    assert "upi_ids" in result["extracted_data"]
    assert "confidence" in result["extracted_data"]["upi_ids"][0]
    assert 0.0 <= result["extracted_data"]["upi_ids"][0]["confidence"] <= 1.0


def test_duplicate_removal(extractor):
    """Test that duplicate entities are removed"""
    messages = [
        "My UPI is test@paytm",
        "Again, my UPI is test@paytm"
    ]
    result = extractor.extract(messages)
    
    assert len(result["extracted_data"]["upi_ids"]) == 1


def test_invalid_phone_numbers_rejected(extractor):
    """Test that invalid phone numbers are rejected"""
    messages = ["Call 1234567890"]  # Doesn't start with 6-9
    result = extractor.extract(messages)
    
    # Should not extract invalid phone number
    assert "phone_numbers" not in result["extracted_data"] or \
           len(result["extracted_data"]["phone_numbers"]) == 0
