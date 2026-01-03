import asyncio
import torch
import heapq
import time
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
from core.memory_manager import PhysicalMemoryManager

class AdvancedInferenceEngine:
    def __init__(self, model_id, device):
        print(f"🚀 Initializing Engine on {device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if device=="cuda" else torch.float32,
            device_map="auto"
        ).eval()

        self.memory = PhysicalMemoryManager(total_blocks=1024)
        self.waiting_queue = [] 
        self.running_batch = [] 
        self.max_batch_size = 8
        self.stats = {"processed": 0, "shed": 0, "backpressure_events": 0}

    def get_priority_score(self, tier, service_type, prompt_len):
        return (tier * 100) + (service_type * 50) + (min(prompt_len // 20, 20))

    async def continuous_batch_loop(self):
        while True:
            # Step 1: Continuous Batching - 填補空位
            while len(self.running_batch) < self.max_batch_size and self.waiting_queue:
                new_req = heapq.heappop(self.waiting_queue)
                self.running_batch.append({
                    "rid": new_req[2],
                    "ids": new_req[3],
                    "queue": new_req[4],
                    "steps": 0
                })

            if not self.running_batch:
                await asyncio.sleep(0.1); continue

            # Step 2: Iteration Step Simulation
            compute_time = 0.05 + (len(self.running_batch) * 0.005)
            await asyncio.sleep(compute_time)

            finished_indices = []
            for i, req in enumerate(self.running_batch):
                req["steps"] += 1
                await req["queue"].put(f"tok_{req['steps']} ")
                
                if req["steps"] >= random.randint(10, 40):
                    await req["queue"].put("[DONE]")
                    self.memory.deallocate(req["rid"])
                    finished_indices.append(i)
                    self.stats["processed"] += 1

            # Step 3: 動態移除已完成請求
            for index in sorted(finished_indices, reverse=True):
                self.running_batch.pop(index)