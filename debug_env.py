from app.config import GEMINI_API_KEY
import os

print(f"CWD: {os.getcwd()}")
if GEMINI_API_KEY:
    print(f"Key loaded: {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}")
    print(f"Length: {len(GEMINI_API_KEY)}")
else:
    print("Key NOT loaded")
