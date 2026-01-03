from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    tier: int = 1         # 0: VIP, 1: Standard
    service_type: int = 0 # 0: Real-time, 1: Batch