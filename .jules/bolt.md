## 2024-06-25 - Direct Search vs Step Generator Overhead in Core Algorithms
**Learning:** In this codebase, the step generators (like `find_path_stepper`) used for visualization instantiate deep dictionaries containing Node states on every step. Wrapping these generators for the core `find_path` function causes massive overhead (~40x slower) compared to running the algorithm directly.
**Action:** When working with core algorithm execution (not UI visualization), implement the core logic directly in the method instead of wrapping UI-focused steppers to avoid dictionary instantiation overhead.
