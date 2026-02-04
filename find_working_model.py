import google.generativeai as genai
from app.config import GEMINI_API_KEY
import sys

# Configure
genai.configure(api_key=GEMINI_API_KEY)

print(f"DEBUG: Testing with key: {GEMINI_API_KEY[:5]}...")

working_model = None

try:
    print("DEBUG: Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            # Strip 'models/' prefix if present, SDK handles it but clean is better
            short_name = model_name.replace("models/", "")
            
            print(f"DEBUG: Testing candidate: {model_name} (short: {short_name})")
            
            try:
                # Try with short name first
                model = genai.GenerativeModel(short_name)
                response = model.generate_content("Test")
                print(f"SUCCESS! Model '{short_name}' works. Response: {response.text}")
                working_model = short_name
                break
            except Exception as e:
                print(f"Failed '{short_name}': {e}")
                
                # Try with full name
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content("Test")
                    print(f"SUCCESS! Model '{model_name}' works. Response: {response.text}")
                    working_model = model_name
                    break
                except Exception as ex:
                     print(f"Failed '{model_name}': {ex}")

    if working_model:
        print(f"FOUND WORKING MODEL: {working_model}")
        # Write to file so next tool can read it easily
        with open("working_model_name.txt", "w") as f:
            f.write(working_model)
    else:
        print("NO WORKING MODEL FOUND.")

except Exception as e:
    print(f"Fatal Error: {e}")
