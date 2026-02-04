"""
Example API request for testing the honeypot endpoint
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000/honeypot"
API_KEY = "chameleon_agent_2026_secure_key"  # Match your .env file

# Example 1: Prize Scam
def test_prize_scam():
    print("Testing Prize Scam Detection...")
    print("-" * 60)
    
    payload = {
        "message": "Congratulations! You have won 5 lakh rupees in KBC lottery! Pay 2000 processing fee to claim your prize.",
        "conversation_id": "test_conv_001",
        "history": []
    }
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success!")
        print(f"Scam Detected: {result['scam_detected']}")
        print(f"Scam Type: {result['scam_type']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Agent Response: {result['agent_response']}")
        print(f"Extracted Intelligence: {json.dumps(result['extracted_intelligence'], indent=2)}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    print()


# Example 2: Multi-turn conversation
def test_multi_turn():
    print("Testing Multi-Turn Conversation...")
    print("-" * 60)
    
    # Turn 1
    payload = {
        "message": "Your bank account has been blocked due to suspicious activity.",
        "conversation_id": "test_conv_002",
        "history": []
    }
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    result1 = response.json()
    print(f"Turn 1 - Agent: {result1['agent_response']}")
    
    # Turn 2
    payload["history"] = [
        {"role": "scammer", "content": payload["message"]},
        {"role": "agent", "content": result1["agent_response"]}
    ]
    payload["message"] = "Update your KYC by paying 500 rupees to 9876543210@paytm"
    
    response = requests.post(API_URL, json=payload, headers=headers)
    result2 = response.json()
    print(f"Turn 2 - Agent: {result2['agent_response']}")
    print(f"Extracted UPI IDs: {result2['extracted_intelligence'].get('upi_ids', [])}")
    
    print()


# Example 3: Health Check
def test_health():
    print("Testing Health Check...")
    print("-" * 60)
    
    response = requests.get("http://localhost:8000/health")
    
    if response.status_code == 200:
        print(f"✅ Server is healthy!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Server error: {response.status_code}")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("CHAMELEON AGENT - API TEST")
    print("=" * 60)
    print()
    
    # Test health check first
    test_health()
    
    # Test scam detection
    test_prize_scam()
    
    # Test multi-turn conversation
    test_multi_turn()
    
    print("=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
