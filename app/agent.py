import google.generativeai as genai
from typing import List, Dict, Any
import asyncio
import concurrent.futures
from app.config import GEMINI_API_KEY
from app.personas import PersonaManager

# Configure Gemini once at module load
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class ConversationManager:
    """
    Manages the conversation state and interaction with the LLM.
    """
    
    # In-memory storage for MVP. For production/scaling, use Redis.
    _states = {}
    _executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    @classmethod
    def get_state(cls, conversation_id: str) -> Dict[str, Any]:
        return cls._states.get(conversation_id, {})

    @classmethod
    def update_state(cls, conversation_id: str, state: Dict[str, Any]):
        cls._states[conversation_id] = state

    @classmethod
    def _call_gemini(cls, full_prompt: str) -> str:
        """Synchronous Gemini API call - runs in thread pool"""
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(full_prompt)
        return response.text.strip()

    @classmethod
    def generate_response(cls, conversation_id: str, user_message: str, scam_type: str) -> str:
        state = cls.get_state(conversation_id)
        
        # Validate state integrity
        if not state or "history" not in state or "persona" not in state:
            persona = PersonaManager.get_persona(scam_type)
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

        try:
            if not GEMINI_API_KEY:
                return "System Error: Gemini API Key not configured."

            full_prompt = f"{system_instruction}\n\nCONVERSATION SO FAR:\n"
            for msg in recent_history:
                role = "Scammer" if msg["role"] == "user" else "You"
                text = msg["parts"][0]
                full_prompt += f"{role}: {text}\n"
            full_prompt += "You: "

            # Use thread pool with timeout to avoid hanging
            future = cls._executor.submit(cls._call_gemini, full_prompt)
            try:
                reply_text = future.result(timeout=15)  # 15 second timeout
            except concurrent.futures.TimeoutError:
                print("Gemini API call timed out after 15 seconds")
                return "Sorry, I'm having connection issues. Can you repeat that?"
            
            state["history"].append({"role": "model", "parts": [reply_text]})
            cls.update_state(conversation_id, state)
            
            return reply_text
            
        except Exception as e:
            print(f"Gemini API Error: {type(e).__name__}: {str(e)}")
            return "I am having some network trouble, please wait."
