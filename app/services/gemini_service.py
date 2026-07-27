import os
import logging
from typing import Dict, Any, Optional
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

class GeminiService:
    """Service to interact with Google Gemini for recovery coaching."""
    
    def __init__(self) -> None:
        self.model = self._init_model()

    def _init_model(self) -> Any:
        """Initializes and returns the generative model."""
        try:
            # Using pro model for higher reasoning capabilities
            return genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            return None

    def generate_emergency_script(self, situation: str) -> str:
        """Generates a grounding script for emergency situations."""
        if not self.model:
            return "Breathe slow. You are not alone. Please reach out to your support network."
            
        prompt = (
            f"Act as an A-CHESS coach. User distress: '{situation}'. "
            "Provide a 3-sentence, zero-typing, immediate grounding script + 1 actionable recovery tip."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text if response.text else "Breathe slow. You are not alone."
        except Exception as e:
            logger.error(f"Error generating emergency script: {e}")
            return "Breathe slow. You are not alone."

    def generate_chat_reply(self, message: str) -> str:
        """Generates a supportive chat reply."""
        if not self.model:
            return "I'm listening. How can I help?"
            
        prompt = f"Act as an Aashwas-style recovery bot. User says: '{message}'. Provide a helpful response."
        try:
            response = self.model.generate_content(prompt)
            return response.text if response.text else "I'm listening. How can I help?"
        except Exception as e:
            logger.error(f"Error generating chat reply: {e}")
            return "I'm listening. How can I help?"

# Export a single instance
gemini_service = GeminiService()
