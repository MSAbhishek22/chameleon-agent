"""
Test script to verify hackathon API format locally
"""
import requests
import json
import subprocess
import time
import sys

# Test payload exactly as provided by hackathon
TEST_PAYLOAD = {
    "sessionId": "1fc994e9-f4c5-47ee-8806-90aeb969928f",
    "message": {
        "sender": "scammer",
        "text": "Your bank account will be blocked today. Verify immediately.",
        "timestamp": 1769776085000
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

EXPECTED_RESPONSE_KEYS = {"status", "reply"}

def test_local():
    """Test against local server"""
    print("=" * 60)
    print("TESTING LOCAL SERVER")
    print("=" * 60)
    
    url = "http://127.0.0.1:8000/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "chameleon-master-key"
    }
    
    try:
        print(f"\nSending POST to: {url}")
        print(f"Payload: {json.dumps(TEST_PAYLOAD, indent=2)}")
        
        response = requests.post(url, json=TEST_PAYLOAD, headers=headers, timeout=30)
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate response format
            if set(data.keys()) == EXPECTED_RESPONSE_KEYS:
                print("\n✅ Response format is CORRECT!")
            else:
                print(f"\n❌ Response format INCORRECT!")
                print(f"   Expected keys: {EXPECTED_RESPONSE_KEYS}")
                print(f"   Got keys: {set(data.keys())}")
            
            if data.get("status") == "success":
                print("✅ Status is 'success'")
            else:
                print(f"❌ Status is not 'success': {data.get('status')}")
            
            if data.get("reply"):
                print(f"✅ Reply present: {data.get('reply')[:100]}...")
            else:
                print("❌ Reply is empty or missing")
                
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error - is the server running?")
        print("   Run: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_live():
    """Test against live Render deployment"""
    print("\n" + "=" * 60)
    print("TESTING LIVE DEPLOYMENT")
    print("=" * 60)
    
    url = "https://chameleon-agent.onrender.com/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "chameleon-master-key"
    }
    
    try:
        print(f"\nSending POST to: {url}")
        response = requests.post(url, json=TEST_PAYLOAD, headers=headers, timeout=60)
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("\n✅ Live deployment is working!")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n❌ Timeout - server may be sleeping or slow")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    if "--live" in sys.argv:
        test_live()
    else:
        test_local()
        print("\n" + "-" * 60)
        print("To test live deployment, run: python test_hackathon_format.py --live")
