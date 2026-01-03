# LLM-Inference-Orchestrator

A high-performance LLM inference engine designed for resilient infrastructure, featuring iteration-level scheduling and dynamic memory management.

## 🌟 Key Technical Features

### 1. Continuous Batching (Iteration-level Scheduling)
Implemented an iteration-level scheduler that allows new requests to join the running batch at each token generation step. This eliminates "computation bubbles" caused by traditional static batching and significantly maximizes GPU throughput.

### 2. Paged Memory Management (PagedAttention Simulation)
To mitigate VRAM fragmentation, the system features a logical-to-physical block mapping mechanism. This simulates PagedAttention logic, ensuring that KV-cache memory is allocated efficiently even with varying sequence lengths, preventing OOM crashes.

### 3. Resilience & SRE (Load Shedding & Backpressure)
Designed for high-availability cloud environments:
* **Adaptive Backpressure**: Actively throttles request inflow based on real-time VRAM utilization.
* **Load Shedding**: Automatically rejects excess requests (HTTP 503) during peak loads to maintain system stability and SLOs.

## 🏗️ Project Structure
* **core/**: Inference engine logic, Iteration-level scheduler, and Memory manager.
* **api/**: FastAPI implementation with Server-Sent Events (SSE) for streaming responses.
* **telemetry/**: Real-time hardware monitoring using NVML (NVIDIA Management Library).