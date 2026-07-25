"""
AI Engine for Ashwas - Integrates with Google Gemini
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
import google.generativeai as genai
from utils.constants import SYSTEM_PROMPTS, SAFETY_CONFIG
from utils.helpers import sanitize_input, format_response

class AIEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.model = None
        self.available = False
        if api_key:
            self._initialize_model()
    
    def _initialize_model(self):
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash", safety_settings=SAFETY_CONFIG)
            self.available = True
        except Exception as e:
            print(f"AI init failed: {e}")
    
    def is_available(self):
        return self.available
    
    async def generate_response(self, prompt: str, mode: str = "recovery_coach"):
        if not self.available:
            return {"response": "I'm currently in offline mode. Take a breath, you're not alone."}
        try:
            full_prompt = f"{SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS['recovery_coach'])}\n\nUser: {sanitize_input(prompt)}\n\nAssistant:"
            response = self.model.generate_content(full_prompt)
            return {"response": format_response(response.text)}
        except Exception:
            return {"response": "I'm here with you."}
