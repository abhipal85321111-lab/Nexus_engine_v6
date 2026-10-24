from fastapi import FastAPI
import time
from collections import deque
import gc

app = FastAPI(title="NEXUS V6 - Jamshedpur Lab")

class NexusV6_RealPool:
    def __init__(self, size=1000):
        gc.disable()
        self.free = deque([[0]*100 for _ in range(size)])
        self.busy_count = 0
    def allocate(self):
        if not self.free:
            raise RuntimeError("Pool Exhausted")
        obj = self.free.popleft()
        self.busy_count += 1
        return obj
    def release(self, obj):
        obj[:] = [0]*len(obj)
        self.free.append(obj)
        self.busy_count -= 1

v6_pool = NexusV6_RealPool(1000)

@app.get("/")
def home():
    return {"engine": "NEXUS V6", "status": "LIVE ✅", "free": len(v6_pool.free)}

@app.get("/v6/test")
def test():
    start = time.perf_counter()
    objs = [v6_pool.allocate() for _ in range(100)]
    for o in objs: v6_pool.release(o)
    elapsed = (time.perf_counter() - start)*1000
    return {"time_ms": elapsed, "result": "PASS ✅" if elapsed < 16 else "LAG ❌"}
