import time
from collections import deque
import gc

class NexusV6_RealPool:
    """V6.1 PRO - Real Zero-Pause Pool - O(1) Alloc/Release"""
    def __init__(self, size=1000):
        gc.disable()  # REAL - GC band hi kar do game loop me
        # Deque = O(1) pop, List = O(n)
        self.free = deque([[0]*100 for _ in range(size)])
        self.busy_count = 0
        print(f"[V6.1 REAL] Pre-allocated {size} objects")
        print(f"[V6.1 REAL] GC Disabled: {not gc.isenabled()} | Free={len(self.free)}")

    def allocate(self):
        # O(1) - No scan, no new object
        if not self.free:
            raise RuntimeError("Pool Exhausted - Size badhao!")
        obj = self.free.popleft()
        self.busy_count += 1
        return obj

    def release(self, obj):
        # O(1) + C-level fast reset - No Python loop
        obj[:] = [0]*len(obj)  # Slice assignment = C me fast
        self.free.append(obj)
        self.busy_count -= 1

# ========== REAL 60 FPS TEST ==========
if __name__ == "__main__":
    v6 = NexusV6_RealPool(1000)
    print("\n--- GAME LOOP 60 FPS (16ms budget) ---")
    for frame in range(5):
        start = time.perf_counter()
        
        # Simulate 100 allocations per frame
        objs = [v6.allocate() for _ in range(100)]
        
        for o in objs:
            o[0] = frame  # use
        
        for o in objs:
            v6.release(o)
        
        elapsed = (time.perf_counter() - start) * 1000
        status = "✅ PASS" if elapsed < 16 else "❌ LAG"
        print(f"Frame {frame}: {elapsed:.4f}ms | Free={len(v6.free)} Busy={v6.busy_count} | {status} - No GC Pause")

    gc.enable()
    print(f"\n[V6.1] GC Re-enabled: {gc.isenabled()}")
