## 2024-05-24 - A* and BFS Stepper Overhead
**Learning:** Pathfinding algorithms in this codebase (A*, BFS) previously used UI-focused step generators (`find_path_stepper`) for instant pathfinding. This caused severe performance overhead due to state dictionary instantiation at every step.
**Action:** Always bypass these generators to implement direct search logic for "instant solve" methods to achieve massive speedups.
