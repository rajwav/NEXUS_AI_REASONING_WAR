## 2024-05-17 - Generator Overhead in Pathfinding
**Learning:** In this codebase, pathfinding algorithms (like A* and BFS) relied on UI-focused step generators (`find_path_stepper`) even for instant, non-visual solves. This caused immense overhead because the generators instantiated full state dictionaries (including a massive serialization of the open set) on every node expansion.
**Action:** Always bypass visual/telemetry step generators for instant logical calculations. Implement direct logic paths that only construct state dicts when explicitly requested by UI or telemetry systems.
