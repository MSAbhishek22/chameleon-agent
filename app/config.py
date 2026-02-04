import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # Warning instead of error to allow app to start for testing other parts
    print("WARNING: GEMINI_API_KEY is not set in environment variables.")
