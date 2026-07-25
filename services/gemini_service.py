import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class GeminiService:
    def __init__(self):
        self.model = self._init_model()

    def _init_model(self):
        # Stable model selection
        return genai.GenerativeModel('gemini-1.5-pro')

    def generate_emergency_script(self, situation: str):
        prompt = f"Act as an A-CHESS coach. User distress: '{situation}'. 3-sentence grounding script + 1 recovery tip."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return "Breathe slow. You are not alone."

    def generate_chat_reply(self, message: str):
        prompt = f"Act as an Aashwas-style recovery bot. User says: '{message}'. Provide a helpful response."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return "I'm listening. How can I help?"

gemini_service = GeminiService()
