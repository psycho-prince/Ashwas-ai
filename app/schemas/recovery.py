from pydantic import BaseModel, Field

class TriggerRequest(BaseModel):
    situation: str = Field(..., min_length=1, max_length=500)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
