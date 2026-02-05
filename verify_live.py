import requests
import time

URL = "https://chameleon-agent.onrender.com/honeypot"
HEALTH_URL = "https://chameleon-agent.onrender.com/health"
API_KEY = "chameleon-master-key"

print(f"--- Checking Live Deployment: {URL} ---")

# 1. Check Health
try:
    print("1. Pinging /health...")
    resp = requests.get(HEALTH_URL)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# 2. Check Honeypot Logic (Scam Detection)
try:
    print("\n2. Testing Scam Detection...")
    payload = {
        "conversation_id": "live_test_1",
        "message": "Hello sir, your bank account is blocked. Update KYC immediately."
    }
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    
    start = time.time()
    resp = requests.post(URL, json=payload, headers=headers)
    latency = time.time() - start
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"Status: 200 OK (Latency: {latency:.2f}s)")
        print(f"Scam Detected: {data['scam_detected']}")
        print(f"Agent Response: {data['response']}")
        print(f"Intelligence: {data['intelligence']}")
    else:
        print(f"Failed: {resp.status_code} - {resp.text}")

except Exception as e:
    print(f"Honeypot check failed: {e}")
