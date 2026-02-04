import google.generativeai as genai
import os

key = "AIzaSyDpd4dYBAuqT9z7vRrWnrs3FiG52GYDtGQ"
genai.configure(api_key=key)

print("Listing models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"AVAILABLE: {m.name}")
except Exception as e:
    print(f"List failed: {e}")

print("Done listing.")
