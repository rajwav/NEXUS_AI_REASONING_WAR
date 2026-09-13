## 2024-05-19 - Pathfinding Algorithm Generator Overhead
**Learning:** In this codebase, pathfinding algorithms (like BFS and A*) relied on UI-focused step generators (`find_path_stepper`) for instant pathfinding. This caused severe performance overhead due to state dictionary instantiations and generator context switching during mass explorations.
**Action:** Always implement direct execution loops for backend logic solvers, and decouple them from visualization-heavy stepper functions. Bypassing the generators provides massive speedups.
