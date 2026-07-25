import os
import logging
import google.generativeai as genai

logger = logging.getLogger("ashwas.llm")
SYSTEM_INSTRUCTION = "You are a supportive recovery assistant. Keep responses short and non-clinical."

def _get_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION)
    except:
        return None

def generate(prompt: str, fallback: str) -> str:
    model = _get_model()
    if not model: return fallback
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else fallback
    except:
        return fallback

FALLBACK_EMERGENCY_SCRIPT = "Breathe in, breathe out. You are safe."
FALLBACK_CAREGIVER_SCRIPT = "Stay calm, stay present. You're doing your best."
FALLBACK_CHAT_REPLY = "I'm here for you."
