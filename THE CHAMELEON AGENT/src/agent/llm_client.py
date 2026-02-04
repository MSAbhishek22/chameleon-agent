"""
LLM Client
Handles communication with LLM providers (Gemini, Groq)
"""

import os
from typing import Optional
import logging
import google.generativeai as genai
from groq import Groq

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with LLM providers"""
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "gemini")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "150"))
        self.timeout = int(os.getenv("LLM_TIMEOUT", "5"))
        
        # Initialize providers
        if self.provider == "gemini":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model_name = os.getenv("LLM_MODEL", "gemini-2.0-flash-exp")
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Initialized Gemini model: {self.model_name}")
        
        elif self.provider == "groq":
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model_name = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")
            logger.info(f"Initialized Groq model: {self.model_name}")
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: Optional[list] = None
    ) -> str:
        """
        Generate response from LLM
        
        Args:
            system_prompt: System instructions for the LLM
            user_message: The user's message
            conversation_history: Optional conversation history
            
        Returns:
            Generated response text
        """
        try:
            if self.provider == "gemini":
                return await self._generate_gemini(system_prompt, user_message, conversation_history)
            elif self.provider == "groq":
                return await self._generate_groq(system_prompt, user_message, conversation_history)
        
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}", exc_info=True)
            # Fallback response
            return self._get_fallback_response(user_message)
    
    async def _generate_gemini(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: Optional[list] = None
    ) -> str:
        """Generate response using Google Gemini"""
        
        # Combine system prompt and user message
        full_prompt = f"{system_prompt}\n\nSCAMMER'S MESSAGE:\n{user_message}\n\nYour response:"
        
        # Generate response
        response = self.model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
        )
        
        return response.text.strip()
    
    async def _generate_groq(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: Optional[list] = None
    ) -> str:
        """Generate response using Groq"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Add conversation history if available
        if conversation_history:
            # Insert history before the latest message
            for msg in conversation_history[-4:]:  # Last 4 messages for context
                messages.insert(-1, msg)
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        
        return response.choices[0].message.content.strip()
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Generate fallback response if LLM fails"""
        message_lower = user_message.lower()
        
        # Simple rule-based fallback responses
        if any(word in message_lower for word in ["bank", "account", "kyc", "blocked"]):
            return "Oh no! My account is blocked? I'm very worried. What should I do? Can you help me?"
        
        elif any(word in message_lower for word in ["won", "prize", "lottery", "congratulations"]):
            return "Really?! I won something? That's amazing! How do I claim it? What do I need to do?"
        
        elif any(word in message_lower for word in ["job", "work", "earn", "income"]):
            return "This sounds interesting! Can you tell me more about this opportunity? How much can I earn?"
        
        elif any(word in message_lower for word in ["computer", "virus", "tech", "microsoft"]):
            return "Oh dear, is something wrong with my computer? I'm not very good with technology. What should I do?"
        
        else:
            return "I see. Can you explain more? I want to make sure I understand correctly."
