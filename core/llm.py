import os
import logging
import google.generativeai as genai

logger = logging.getLogger("ashwas.llm")
SYSTEM_INSTRUCTION = "You are a supportive recovery assistant. Keep responses short and non-clinical. Always respond in the same language as the user (e.g. Malayalam)."

def _get_model():
    # Keep for compatibility, returns gemini-2.0-flash by default
    api_key = (
        os.environ.get("GEMINI_API_KEY") or
        os.environ.get("GEMINI_KEY") or
        os.environ.get("GOOGLE_API_KEY") or
        ""
    )
    if not api_key: return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.0-flash")
    except:
        return None

def generate(prompt: str, fallback: str) -> str:
    api_key = (
        os.environ.get("GEMINI_API_KEY") or
        os.environ.get("GEMINI_KEY") or
        os.environ.get("GOOGLE_API_KEY") or
        ""
    )
    if not api_key: 
        return fallback

    # Self-healing model list
    models_to_try = [
        "gemini-2.0-flash",
        "gemini-flash-latest",
        "gemini-2.5-flash",
        "gemini-pro-latest",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite"
    ]
    
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        logger.error(f"GenAI configuration failed: {e}")
        return fallback

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            full_prompt = f"{SYSTEM_INSTRUCTION}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            if response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Model {model_name} execution failed: {e}. Trying fallback...")
            continue
            
    return fallback

FALLBACK_EMERGENCY_SCRIPT = "Breathe in, breathe out. You are safe. Concentrate on your feet touching the ground."
FALLBACK_CAREGIVER_SCRIPT = "Stay calm, speak in a gentle tone. You're doing your best to support them."
FALLBACK_CHAT_REPLY = "I'm here to support you. Let's take it one moment at a time."
