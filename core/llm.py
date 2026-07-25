import os
import logging
import google.generativeai as genai

logger = logging.getLogger("ashwas.llm")
SYSTEM_INSTRUCTION = "You are a supportive recovery assistant. Keep responses short and non-clinical. Always respond in the same language as the user (e.g. Malayalam)."

def _get_model():
    api_key = (
        os.environ.get("GEMINI_API_KEY") or
        os.environ.get("GEMINI_KEY") or
        os.environ.get("GOOGLE_API_KEY") or
        ""
    )
    if not api_key: 
        logger.warning("No Gemini API key found in environment variables.")
        return None
        
    # Attempt loading preferred models sequentially
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.5-flash-8b"]
    for model_name in models_to_try:
        try:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel(model_name, system_instruction=SYSTEM_INSTRUCTION)
        except Exception as e:
            logger.debug(f"Failed loading model {model_name}: {e}")
            continue
            
    # Final fallback
    try:
        return genai.GenerativeModel("gemini-pro")
    except:
        return None

def generate(prompt: str, fallback: str) -> str:
    model = _get_model()
    if not model: return fallback
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else fallback
    except Exception as e:
        logger.error(f"GenAI generation failed: {e}")
        return fallback

FALLBACK_EMERGENCY_SCRIPT = "Breathe in, breathe out. You are safe. Concentrate on your feet touching the ground."
FALLBACK_CAREGIVER_SCRIPT = "Stay calm, speak in a gentle tone. You're doing your best to support them."
FALLBACK_CHAT_REPLY = "I'm here to support you. Let's take it one moment at a time."
