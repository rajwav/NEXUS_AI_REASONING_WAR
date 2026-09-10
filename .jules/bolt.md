## 2026-09-10 - A* Pathfinding Generator Overhead Optimization
**Learning:** In standard library Python, generating pathfinding states via yielding and complex dictionary instantiation for step-by-step UI updates (`find_path_stepper`) adds massive overhead to bulk pathfinding. Converting the generator outputs to a list (`list(self.find_path_stepper(...))`) for instant path solutions causes severe degradation (~450ms vs ~10ms execution).

**Action:** Separate visual inspection/telemetry generators from native direct-solve algorithms. Extract core logic natively when instant results are required, bypassing state dictionary creation entirely.
