
## 2024-05-18 - A* Search Generator Overhead
**Learning:** Using UI-focused step generators (`find_path_stepper`) for core algorithm computations (`find_path`) causes severe performance overhead (~100x slower) due to constant state dictionary instantiation.
**Action:** Implement direct search logic (using `heapq` and direct evaluation) for raw computation paths while preserving generators solely for visualization/telemetry use cases.
