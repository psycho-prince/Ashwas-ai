"""
Ashwas AI 2.0 - Recovery Intelligence Platform
Main FastAPI Application
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

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.ai_engine import AIEngine
from core.safety import SafetyGuardrails

# Import utilities
from utils.constants import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    CRISIS_KEYWORDS
)

# ==================== Configuration ====================
class Config:
    """Application configuration"""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    DEBUG = ENVIRONMENT == "development"
    
    # Model configurations
    MODEL_NAME = "gemini-1.5-flash" if GEMINI_API_KEY else None
    
    # Storage paths
    STATIC_DIR = "static"
    TEMPLATE_DIR = "templates"

# ==================== Initialize Application ====================
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory=Config.STATIC_DIR), name="static")
templates = Jinja2Templates(directory=Config.TEMPLATE_DIR)

# ==================== Initialize Services ====================
ai_engine = AIEngine(api_key=Config.GEMINI_API_KEY)
safety_guardrails = SafetyGuardrails(crisis_keywords=CRISIS_KEYWORDS)

# ==================== Routes ====================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main recovery companion interface"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": APP_NAME
    })

@app.post("/api/v1/chat")
async def chat_endpoint(request: Request):
    """Chat endpoint with safety guardrails"""
    data = await request.json()
    message = data.get("message", "")
    
    # Analyze safety
    safety_analysis = safety_guardrails.analyze_message(message)
    safety_response = safety_guardrails.generate_safe_response(message, safety_analysis)
    
    if safety_response:
        return JSONResponse(safety_response)
        
    # Generate AI response
    response = await ai_engine.generate_response(message)
    return JSONResponse(response)

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)
