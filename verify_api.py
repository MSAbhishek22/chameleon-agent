import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/honeypot"
API_KEY = "test_key"

def test_scenario(name, message, conversation_id="test_conv_1"):
    print(f"\n--- Testing Scenario: {name} ---")
    payload = {
        "conversation_id": conversation_id,
        "message": message
    }
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    start_time = time.time()
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        end_time = time.time()
        
        latency = end_time - start_time
        print(f"Latency: {latency:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Status: 200 OK")
            print(f"Scam Detected: {data['scam_detected']}")
            print(f"Agent Response: {data['response']}")
            print(f"Intelligence: {json.dumps(data['intelligence'], indent=2)}")
        else:
            print(f"Failed! Status: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 1. Tech Support Scam
    test_scenario(
        "Tech Support - Initial", 
        "Hello, this is Microsoft Support. Your computer has a virus. Please call us immediately.",
        "conv_tech_1"
    )
    
    # 2. Lottery Scam
    test_scenario(
        "Lottery - Initial", 
        "Congratulations! You calculate won 5 Crore in KBC lottery. Pay 5000 rs registration fee.",
        "conv_lott_1"
    )

    # 3. Extraction Test
    test_scenario(
        "Extraction Test", 
        "Please send money to my bank account 12345678901 at SBI, IFSC: SBIN0001234. Or gpay 9876543210@okaxis",
        "conv_extract_1"
    )
