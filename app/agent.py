import google.generativeai as genai
from typing import List, Dict, Any
from app.config import GEMINI_API_KEY
from app.personas import PersonaManager

class ConversationManager:
    """
    Manages the conversation state and interaction with the LLM.
    """
    
    # In-memory storage for MVP. For production/scaling, use Redis.
    _states = {}

    @classmethod
    def get_state(cls, conversation_id: str) -> Dict[str, Any]:
        return cls._states.get(conversation_id, {})

    @classmethod
    def update_state(cls, conversation_id: str, state: Dict[str, Any]):
        cls._states[conversation_id] = state

    @classmethod
    def generate_response(cls, conversation_id: str, user_message: str, scam_type: str) -> str:
        state = cls.get_state(conversation_id)
        
        # Validate state integrity
        if not state or "history" not in state or "persona" not in state:
            persona = PersonaManager.get_persona(scam_type)
            # If state exists but is partial (e.g. only intelligence), preserve it
            if not state:
                state = {}
            
            if "scam_type" not in state:
                state["scam_type"] = scam_type
            if "persona" not in state:
                state["persona"] = persona
            if "history" not in state:
                state["history"] = []
        
        state["history"].append({"role": "user", "parts": [user_message]})
        recent_history = state["history"][-10:]
        
        # --- STRATEGY ENGINE ---
        # Calculate turn count (each user message = 1 turn)
        turn_count = len([m for m in state["history"] if m["role"] == "user"])
        
        current_phase = "TRUST_BUILDING"
        phase_instruction = ""
        
        if turn_count <= 2:
            current_phase = "TRUST_BUILDING"
            phase_instruction = "PHASE 1 (TRUST): Act confused, eager, or worried depending on your persona. Ask clarifying questions. Do NOT give money yet."
        elif turn_count <= 5:
            current_phase = "STALLING_&_EXTRACTING"
            phase_instruction = "PHASE 2 (STALL/EXTRACT): Agree to pay but create a hurdle. (e.g., 'UPI not working', 'Battery low'). Ask for BANK ACCOUNT DETAILS or alternate payment method."
        else:
            current_phase = "DEEP_EXTRACTION"
            phase_instruction = "PHASE 3 (DEEP EXTRACT): Claim the previous method failed. Ask for a different Phone Number or URL. wasting their time."

        persona_prompt = state["persona"]["prompt"]
        system_instruction = f"""
        {persona_prompt}
        
        CURRENT STRATEGY PHASE: {current_phase} (Turn {turn_count})
        TACTIC: {phase_instruction}
        
        TASK:
        Reply to the user staying completely in character. 
        Keep the response short (1-2 sentences).
        """
        
        # print(f"DEBUG: Active Phase: {current_phase}")

        try:
            if not GEMINI_API_KEY:
                return "System Error: Gemini API Key not configured."

            # Configure here to ensure thread safety / latest key usage
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            full_prompt = f"{system_instruction}\n\nCONVERSATION SO FAR:\n"
            for msg in recent_history:
                role = "Scammer" if msg["role"] == "user" else "You"
                text = msg["parts"][0]
                full_prompt += f"{role}: {text}\n"
            full_prompt += "You: "

            response = model.generate_content(full_prompt)
            reply_text = response.text.strip()
            
            state["history"].append({"role": "model", "parts": [reply_text]})
            cls.update_state(conversation_id, state)
            
            return reply_text
            
        except Exception as e:
            # Log the error for debugging
            print(f"Gemini API Error: {type(e).__name__}: {str(e)}")
            # Graceful fallback for the hackathon so the system doesn't crash
            return "I am having some network trouble, please wait."

