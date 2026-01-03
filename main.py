import uvicorn
import asyncio
from fastapi import FastAPI
from core.scheduler import AdvancedInferenceEngine
from telemetry.monitor import HardwareMonitor
from api.routes import create_router

app = FastAPI(title="LLM-Inference-Orchestrator")

# 初始化組件
device = "cuda" # 或 "cpu"
engine = AdvancedInferenceEngine("Qwen/Qwen2.5-1.5B-Instruct", device)
monitor = HardwareMonitor()

# 將 API 邏輯掛載回 Engine (為了簡化調用)
async def add_request_logic(req):
    return await engine.add_request(req.prompt, req.tier, req.service_type)
engine.add_request_logic = add_request_logic

# 註冊路由
app.include_router(create_router(engine, monitor))

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(engine.continuous_batch_loop())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)