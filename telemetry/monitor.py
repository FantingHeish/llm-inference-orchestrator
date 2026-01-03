import pynvml

class HardwareMonitor:
    def __init__(self):
        try:
            pynvml.nvmlInit()
            self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.gpu_ready = True
        except:
            self.gpu_ready = False

    def get_stats(self):
        if not self.gpu_ready: return {"mode": "CPU"}
        info = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
        return {
            "vram_used_gb": round(info.used / 1024**3, 2),
            "vram_util_pct": round((info.used/info.total)*100, 1),
            "temp_c": pynvml.nvmlDeviceGetTemperature(self.gpu_handle, 0)
        }