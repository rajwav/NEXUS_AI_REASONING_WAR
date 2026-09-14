## 2024-05-20 - Bypass UI-focused step generators in core algorithmic solvers
**Learning:** In this codebase, pathfinding algorithms (like BFS and A*) may rely on UI-focused step generators (e.g., `find_path_stepper`) for instant pathfinding, which causes severe performance overhead due to state dictionary instantiation.
**Action:** Bypass these generators to implement direct search logic for massive speedups when raw computation is needed over state telemetry.
