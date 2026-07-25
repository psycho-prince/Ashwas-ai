from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    message: str
    mode: str
    user_id: str
    history: List = []
    context: Dict = {}

class CheckInRequest(BaseModel):
    user_id: str

class SafetyPlanRequest(BaseModel):
    user_id: str

class EmergencyScriptRequest(BaseModel):
    user_id: str
    scenario: str
    audience: str = "self"
    personal_context: Dict = {}

class VoiceInputRequest(BaseModel):
    user_id: str

class CaregiverAlertRequest(BaseModel):
    user_id: str
