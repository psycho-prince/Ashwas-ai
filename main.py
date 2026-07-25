import os
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from utils import data
from core import llm

app = FastAPI(title="Ashwas AI — Recovery & Prevention Platform")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class EmergencyRequest(BaseModel):
    severity: Optional[str] = "distress"
    scenario: Optional[str] = "distress"
    user_id: Optional[str] = ""
    note: Optional[str] = ""

class CaregiverRequest(BaseModel):
    relationship: str
    behavior: str
    note: Optional[str] = ""

class ChatMessage(BaseModel):
    message: str
    mode: Optional[str] = "recovery_coach"
    role: Optional[str] = "self"
    user_id: Optional[str] = ""

@app.get("/")
async def index(request: Request):
    # Correct signature for Starlette 1.3.x on Render
    return templates.TemplateResponse(request, "index.html", {"app_name": "Ashwas AI"})

@app.get("/api/health")
async def health():
    api_key = (
        os.environ.get("GEMINI_API_KEY") or
        os.environ.get("GEMINI_KEY") or
        os.environ.get("GOOGLE_API_KEY") or
        ""
    )
    key_exists = bool(api_key)
    key_prefix = api_key[:6] + "..." if key_exists and len(api_key) > 6 else "None"
    
    # Diagnostics check on core model init
    model_loaded = False
    model_name = "None"
    init_error = "None"
    try:
        model = llm._get_model()
        if model:
            model_loaded = True
            model_name = model.model_name
        else:
            init_error = "Model returned None (possibly empty key or configure failed)"
    except Exception as e:
        init_error = str(e)
        
    return {
        "api_key_configured": key_exists,
        "api_key_prefix": key_prefix,
        "model_loaded": model_loaded,
        "model_name": model_name,
        "initialization_error": init_error
    }

@app.get("/api/test-ai")
async def test_ai():
    try:
        model = llm._get_model()
        if not model:
            return {"status": "error", "message": "Model could not be initialized"}
        response = model.generate_content("Hello. Reply in 1 word.")
        return {
            "status": "success",
            "response": response.text.strip() if response.text else "None"
        }
    except Exception as e:
        return {
            "status": "exception",
            "exception_type": type(e).__name__,
            "message": str(e)
        }

@app.post("/api/emergency-script")
async def emergency_script(req: EmergencyRequest):
    scenario = req.scenario or req.severity or "general distress"
    prompt = (
        f"Act as a professional A-CHESS recovery coach. A user is experiencing an acute distress scenario: '{scenario}'. "
        "Provide a comforting 3-sentence grounding script. End with one physical action."
    )
    script = llm.generate(prompt, llm.FALLBACK_EMERGENCY_SCRIPT)
    return {"response": script, "script": script, "contacts": data.CRISIS_CONTACTS}

@app.post("/api/caregiver-script")
async def caregiver_script(req: CaregiverRequest):
    if req.behavior == "unresponsive":
        return {"protocol": data.OVERDOSE_PROTOCOL, "contacts": data.CRISIS_CONTACTS}
    prompt = f"A {req.relationship} is supporting someone who is {req.behavior}. Give 2 example phrases, one 'don't', and a self-care reminder."
    script = llm.generate(prompt, llm.FALLBACK_CAREGIVER_SCRIPT)
    return {"response": script, "script": script, "contacts": data.CRISIS_CONTACTS}

@app.post("/api/chat")
async def chat(req: ChatMessage):
    mode = req.mode or "recovery_coach"
    
    # Custom instructions matching mode and multilingual rules
    system_instruction = (
        "You are an empathetic, professional A-CHESS recovery coach assisting individuals navigating substance use disorders. "
        "Keep responses concise (3-4 sentences) and supportive. "
        "Always respond in the exact same language that the user uses to communicate. If the user writes in Malayalam, respond in Malayalam."
    )
    if mode == "caregiver_support":
        system_instruction = (
            "You are a caregiver support coach assisting family members of individuals in recovery. "
            "Provide de-escalation tips and active listening resources. Keep responses concise (3-4 sentences). "
            "Always respond in the exact same language that the user uses to communicate. If the user writes in Malayalam, respond in Malayalam."
        )
        
    prompt = f"System Instruction: {system_instruction}\nUser message: {req.message}"
    reply = llm.generate(prompt, llm.FALLBACK_CHAT_REPLY)
    return {"response": reply, "reply": reply}

@app.get("/api/resources")
async def resources(audience: Optional[str] = None):
    items = data.EDUCATION
    if audience in ("self", "caregiver"):
        items = [e for e in items if e["audience"] in (audience, "both")]
    return items
