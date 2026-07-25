"""
Ashwas AI 2.0 - Recovery Intelligence Platform
"""
import os
import sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ai_engine import AIEngine
from core.safety import SafetyGuardrails
from utils.constants import CRISIS_KEYWORDS

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ai_engine = AIEngine(api_key=os.getenv("GEMINI_API_KEY"))
safety_guardrails = SafetyGuardrails(crisis_keywords=CRISIS_KEYWORDS)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
@app.post("/api/v1/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    mode = data.get("mode", "recovery_coach")
    
    safety = safety_guardrails.analyze_message(message)
    emergency = safety_guardrails.generate_safe_response(message, safety)
    if emergency: return JSONResponse(emergency)
    
    response = await ai_engine.generate_response(message, mode=mode)
    return JSONResponse(response)

@app.post("/api/emergency-script")
async def emergency_script(request: Request):
    data = await request.json()
    response = await ai_engine.generate_response(data.get("scenario", "panic"), mode="emergency")
    return JSONResponse(response)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
