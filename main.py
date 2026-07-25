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
    severity: str
    note: Optional[str] = ""

class CaregiverRequest(BaseModel):
    relationship: str
    behavior: str
    note: Optional[str] = ""

class ChatMessage(BaseModel):
    message: str
    role: str = "self"

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/emergency-script")
async def emergency_script(req: EmergencyRequest):
    if req.severity == "overdose":
        return {"protocol": data.OVERDOSE_PROTOCOL, "contacts": data.CRISIS_CONTACTS}
    prompt = f"The person is experiencing {req.severity}. Write a 3-sentence grounding script. End with one physical action."
    script = llm.generate(prompt, llm.FALLBACK_EMERGENCY_SCRIPT)
    return {"script": script, "contacts": data.CRISIS_CONTACTS}

@app.post("/api/caregiver-script")
async def caregiver_script(req: CaregiverRequest):
    if req.behavior == "unresponsive":
        return {"protocol": data.OVERDOSE_PROTOCOL, "contacts": data.CRISIS_CONTACTS}
    prompt = f"A {req.relationship} is supporting someone who is {req.behavior}. Give 2 example phrases, one 'don't', and a self-care reminder."
    script = llm.generate(prompt, llm.FALLBACK_CAREGIVER_SCRIPT)
    return {"script": script, "contacts": data.CRISIS_CONTACTS}

@app.post("/api/chat")
async def chat(req: ChatMessage):
    prompt = f"You are a recovery assistant. User said: {req.message}. Reply supportively in 2-4 sentences."
    reply = llm.generate(prompt, llm.FALLBACK_CHAT_REPLY)
    return {"reply": reply}

@app.get("/api/resources")
async def resources(audience: Optional[str] = None):
    items = data.EDUCATION
    if audience in ("self", "caregiver"):
        items = [e for e in items if e["audience"] in (audience, "both")]
    return {"resources": items}

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
