from fastapi import APIRouter
from app.schemas.recovery import TriggerRequest, ChatRequest
from app.services.gemini_service import gemini_service

router = APIRouter()

@router.post("/trigger")
async def trigger(req: TriggerRequest):
    script = gemini_service.generate_emergency_script(req.situation)
    return {"script": script}

@router.post("/chat")
async def chat(req: ChatRequest):
    reply = gemini_service.generate_chat_reply(req.message)
    return {"reply": reply}
