import requests
import time
import json

URL = "http://127.0.0.1:8000/honeypot"
API_KEY = "test_key"
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}
CONVERSATION_ID = f"strat_test_{int(time.time())}"

scammer_lines = [
    "Hello sir, I am calling from Microsoft Support.",
    "Your computer has a virus, please download AnyDesk.",
    "Sir, you must pay 500 rupees for antivirus.",
    "Pay to this UPI: scam@upi",
    "Why are you delaying? Pay now.",
    "Okay send to bank account 123456789 (HDFC0001234)"
]

print(f"--- Testing Conversation Strategy (ID: {CONVERSATION_ID}) ---")

for i, line in enumerate(scammer_lines):
    turn = i + 1
    print(f"\n[Turn {turn}] Scammer: {line}")
    
    try:
        payload = {"conversation_id": CONVERSATION_ID, "message": line}
        resp = requests.post(URL, json=payload, headers=HEADERS)
        data = resp.json()
        
        agent_reply = data["response"]
        scam_type = data["intelligence"].get("scam_type", "unknown")
        
        print(f"Agent ({scam_type}): {agent_reply}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(1) # simulate slight delay
