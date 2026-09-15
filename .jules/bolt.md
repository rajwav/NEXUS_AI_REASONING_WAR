
## 2024-05-18 - Generator Overhead in Pathfinding Algorithms
**Learning:** In this codebase, pathfinding algorithms (like BFS and A*) heavily relied on UI-focused step generators (e.g., `find_path_stepper`) for instant pathfinding. This caused severe performance overhead due to state dictionary instantiation and yielding for every node expansion.
**Action:** Bypass these generators and implement direct search logic for the instant execution functions (e.g. `find_path`). This simple decoupling avoids massive overhead and provides significant execution speedups (e.g. from 13.7s to 0.05s on a 100x100 grid).
