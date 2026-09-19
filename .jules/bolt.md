## 2024-05-24 - A* Generator Overhead
**Learning:** In this codebase, avoiding the use of UI-focused step generators (e.g., `find_path_stepper`) for core algorithm computations (like `find_path`) avoids massive performance overhead from repetitive state dictionary instantiations and intermediate yields.
**Action:** Implement direct search loops and discrete state variables for the instant solve variants of pathfinding algorithms to bypass visualization costs.
