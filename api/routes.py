import asyncio
import json
import time
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from api.models import ChatRequest

def create_router(engine, monitor):
    router = APIRouter()

    @router.post("/v1/chat/completions")
    async def chat(req: ChatRequest):
        # [Load Shedding & Backpressure Logic]
        if len(engine.waiting_queue) > 50:
            engine.stats["shed"] += 1
            raise HTTPException(status_code=503, detail="Server Overloaded")

        if engine.memory.get_usage_ratio() > 0.9:
            engine.stats["backpressure_events"] += 1
            await asyncio.sleep(0.5)

        rid, q = await engine.add_request_logic(req) # 呼叫 engine 內部的分配邏輯
        
        async def event_generator():
            while True:
                token = await q.get()
                if token == "[DONE]": break
                yield {"event": "token", "data": json.dumps({"rid": rid, "text": token})}
        
        return EventSourceResponse(event_generator())

    @router.get("/health")
    async def health():
        return {
            "hardware": monitor.get_stats(),
            "engine_load": len(engine.waiting_queue),
            "usage_ratio": engine.memory.get_usage_ratio()
        }
    
    return router