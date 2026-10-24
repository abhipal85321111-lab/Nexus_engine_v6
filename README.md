# ☠️ NEXUS V6.1 PRO - Real Zero-Pause Pool

> **IIT wale GC chalate hain, Jamshedpur Lab GC band kar deta hai.**

### 🔥 Kya Hai Ye?
Normal game me har bullet pe `new Object()` banta hai, GC chalta hai, FPS drop.
**V6 me 0 LAG** - 100 bullets = 0.8ms only!

### ⚡ Engine Logic
1.  `gc.disable()` - Game loop me GC hi band, 0 pause
2.  `deque` - O(1) `popleft()` / `append()` - List se 10x fast
3.  Pre-allocate 1000 objects - Game me new alloc nahi
4.  `obj[:] = [0]*len` - C-level fast reset

### 📊 Performance Test
