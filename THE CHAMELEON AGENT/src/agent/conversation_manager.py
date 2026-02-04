"""
Conversation Manager
Manages multi-turn conversations with strategic engagement phases
"""

from typing import List, Dict, Any, Optional
import logging
from src.personas.persona_manager import Persona
from src.agent.llm_client import LLMClient

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation state and generates strategic responses"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        # In-memory conversation state (for hackathon; use Redis for production)
        self.conversations: Dict[str, Dict[str, Any]] = {}
    
    async def generate_response(
        self,
        message: str,
        conversation_id: str,
        history: List[Any],
        persona: Persona,
        scam_type: str,
        turn_count: int
    ) -> str:
        """
        Generate agent response using persona and conversation strategy
        
        Args:
            message: Incoming scammer message
            conversation_id: Unique conversation ID
            history: Conversation history
            persona: Selected persona
            scam_type: Detected scam type
            turn_count: Current turn number
            
        Returns:
            Agent's response as the persona
        """
        
        # Determine conversation phase based on turn count
        phase = self._determine_phase(turn_count)
        
        # Get or create conversation state
        state = self._get_conversation_state(conversation_id, persona, scam_type)
        state["turn_count"] = turn_count
        state["phase"] = phase
        
        # Generate system prompt based on persona and phase
        system_prompt = persona.get_system_prompt(scam_type, phase, turn_count)
        
        # Add conversation history context
        if history:
            history_text = self._format_history(history)
            system_prompt += f"\n\nCONVERSATION SO FAR:\n{history_text}"
        
        # Generate response using LLM
        response = await self.llm_client.generate_response(
            system_prompt=system_prompt,
            user_message=message,
            conversation_history=None  # Already included in system prompt
        )
        
        # Update conversation state
        state["last_response"] = response
        self.conversations[conversation_id] = state
        
        logger.info(f"Generated response for {conversation_id}, phase: {phase}, turn: {turn_count}")
        
        return response
    
    def _determine_phase(self, turn_count: int) -> str:
        """Determine conversation phase based on turn count"""
        if turn_count <= 3:
            return "trust_building"
        elif turn_count <= 7:
            return "extraction"
        else:
            return "deep_extraction"
    
    def _get_conversation_state(
        self,
        conversation_id: str,
        persona: Persona,
        scam_type: str
    ) -> Dict[str, Any]:
        """Get or create conversation state"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                "conversation_id": conversation_id,
                "persona": persona.name,
                "scam_type": scam_type,
                "turn_count": 0,
                "phase": "trust_building",
                "extracted_data": {},
                "last_response": None
            }
        
        return self.conversations[conversation_id]
    
    def _format_history(self, history: List[Any]) -> str:
        """Format conversation history for context"""
        formatted = []
        for msg in history[-6:]:  # Last 6 messages for context
            role = "SCAMMER" if msg.role == "scammer" else "YOU"
            formatted.append(f"{role}: {msg.content}")
        
        return "\n".join(formatted)
    
    def get_conversation_metrics(self, conversation_id: str) -> Dict[str, Any]:
        """Get metrics for a conversation"""
        state = self.conversations.get(conversation_id, {})
        return {
            "turn_count": state.get("turn_count", 0),
            "phase": state.get("phase", "unknown"),
            "persona_used": state.get("persona", "unknown")
        }
