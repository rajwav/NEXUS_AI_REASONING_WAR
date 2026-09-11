## 2025-02-14 - Python Generator Yield Bottleneck
**Learning:** Instantiating deep state dictionaries per node during heuristic and brute-force graph search algorithms (via stepper generators) incurs massive, often hidden overhead compared to direct array/set updates. A* was spending ~18s instantiating debugging dicts versus ~0.07s doing the actual calculations.
**Action:** Always bypass visualization-focused step generators for headless or direct `solve()` calls. Implement separate tight loops for logic vs telemetry generation.
