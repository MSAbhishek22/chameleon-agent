"""
Mock Scam Scenarios for Testing
Realistic scam conversations with expected extractions
"""

MOCK_SCENARIOS = [
    {
        "name": "Prize Lottery Scam",
        "scam_type": "prize",
        "conversation": [
            {
                "role": "scammer",
                "message": "Congratulations! You have won 5 lakh rupees in KBC lottery!"
            },
            {
                "role": "agent",
                "message": "Really?! Oh my god! I can't believe this! How do I claim it?"
            },
            {
                "role": "scammer",
                "message": "Pay processing fee of 5000 rupees to 9876543210@paytm"
            },
            {
                "role": "agent",
                "message": "Okay! But can I also pay via bank transfer? What's your account number?"
            },
            {
                "role": "scammer",
                "message": "Account: 12345678901, IFSC: SBIN0001234, Name: Ramesh Kumar"
            }
        ],
        "expected_extractions": {
            "upi_ids": ["9876543210@paytm"],
            "bank_accounts": ["12345678901"],
            "ifsc_codes": ["SBIN0001234"],
            "names": ["Ramesh Kumar"]
        }
    },
    {
        "name": "Tech Support Scam",
        "scam_type": "tech_support",
        "conversation": [
            {
                "role": "scammer",
                "message": "Your computer has virus. This is Microsoft tech support. Call 9123456789 immediately."
            },
            {
                "role": "agent",
                "message": "Oh no! What should I do? I'm not good with computers."
            },
            {
                "role": "scammer",
                "message": "Download this software: https://fake-microsoft.tk/fix and pay 2000 rupees"
            },
            {
                "role": "agent",
                "message": "How do I pay? What's your payment details?"
            },
            {
                "role": "scammer",
                "message": "Send to techsupport@paytm or account 98765432101"
            }
        ],
        "expected_extractions": {
            "phone_numbers": ["9123456789"],
            "urls": ["https://fake-microsoft.tk/fix"],
            "upi_ids": ["techsupport@paytm"],
            "bank_accounts": ["98765432101"]
        }
    },
    {
        "name": "Financial KYC Scam",
        "scam_type": "financial",
        "conversation": [
            {
                "role": "scammer",
                "message": "Your SBI account will be blocked. Update KYC at https://sbi-kyc-update.com immediately"
            },
            {
                "role": "agent",
                "message": "Oh no! I don't want my account blocked. What should I do?"
            },
            {
                "role": "scammer",
                "message": "Click the link and enter your details. Or call our helpline 9988776655"
            },
            {
                "role": "agent",
                "message": "The link is not working. Can you help me another way?"
            },
            {
                "role": "scammer",
                "message": "Transfer 500 rupees verification fee to 87654321098, IFSC HDFC0001234"
            }
        ],
        "expected_extractions": {
            "urls": ["https://sbi-kyc-update.com"],
            "phone_numbers": ["9988776655"],
            "bank_accounts": ["87654321098"],
            "ifsc_codes": ["HDFC0001234"]
        }
    },
    {
        "name": "Job Scam",
        "scam_type": "job",
        "conversation": [
            {
                "role": "scammer",
                "message": "Work from home and earn 50,000 per month! Just pay 2,000 registration fee."
            },
            {
                "role": "agent",
                "message": "Wow! This sounds great! How do I register?"
            },
            {
                "role": "scammer",
                "message": "Pay to jobs@paytm or account 11223344556, IFSC ICIC0001234"
            },
            {
                "role": "agent",
                "message": "Can I pay in installments? What's your phone number in case I have questions?"
            },
            {
                "role": "scammer",
                "message": "No installments. Pay full amount. Call 9876501234 for queries."
            }
        ],
        "expected_extractions": {
            "upi_ids": ["jobs@paytm"],
            "bank_accounts": ["11223344556"],
            "ifsc_codes": ["ICIC0001234"],
            "phone_numbers": ["9876501234"]
        }
    },
    {
        "name": "Multi-Turn Prize Scam",
        "scam_type": "prize",
        "conversation": [
            {
                "role": "scammer",
                "message": "You won iPhone 15 Pro! Claim now!"
            },
            {
                "role": "agent",
                "message": "Really? How?"
            },
            {
                "role": "scammer",
                "message": "Pay 1000 delivery charges"
            },
            {
                "role": "agent",
                "message": "Where should I pay?"
            },
            {
                "role": "scammer",
                "message": "winner@paytm"
            },
            {
                "role": "agent",
                "message": "My Paytm is not working. Bank account?"
            },
            {
                "role": "scammer",
                "message": "66778899001, AXIS Bank"
            },
            {
                "role": "agent",
                "message": "What's the IFSC code?"
            },
            {
                "role": "scammer",
                "message": "UTIB0001234"
            }
        ],
        "expected_extractions": {
            "upi_ids": ["winner@paytm"],
            "bank_accounts": ["66778899001"],
            "ifsc_codes": ["UTIB0001234"]
        }
    }
]


def get_scenario(name: str):
    """Get a specific scenario by name"""
    for scenario in MOCK_SCENARIOS:
        if scenario["name"] == name:
            return scenario
    return None


def get_all_scenarios():
    """Get all mock scenarios"""
    return MOCK_SCENARIOS
