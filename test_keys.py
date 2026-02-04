import google.generativeai as genai
import sys

keys = [
    "AIzaSyDpd4dYBAuqT9z7vRrWnrs3FIG52GYDtGQ", # Captial I
    "AIzaSyDpd4dYBAuqT9z7vRrWnrs3FlG52GYDtGQ", # Lowercase l
    "AIzaSyDpd4dYBAuqT9z7vRrWnrs3F1G52GYDtGQ", # One
]

with open("key_results.txt", "w") as f:
    for i, key in enumerate(keys):
        f.write(f"Testing key {i}: {key}\n")
        genai.configure(api_key=key)
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content("Hello")
            f.write(f"SUCCESS! The key is: {key}\n")
        except Exception as e:
            f.write(f"Failed: {str(e)[:100]}...\n") # Truncate error
