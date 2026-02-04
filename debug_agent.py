from app.agent import ConversationManager
import sys

print("DEBUG: Starting agent test...")
try:
    response = ConversationManager.generate_response("debug_session", "Hello help me", "tech_support")
    print(f"DEBUG: Response: {response}")
except Exception as e:
    print(f"DEBUG: Exception caught in main wrapper: {e}")
