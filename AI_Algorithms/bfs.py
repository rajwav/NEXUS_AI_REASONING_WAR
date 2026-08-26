"""
NEXUS AI REASONING WAR - Breadth-First Search (BFS)
Uninformed search benchmark used to demonstrate exploration inefficiency compared to A*.
"""

from typing import List, Tuple, Dict, Set, Optional, Generator, Any
from collections import deque


class BreadthFirstSearch:
    """Breadth-First Search (BFS) pathfinder with step-by-step generator."""
    def find_path(self, grid: List[List[Any]], start: Tuple[int, int], goal: Tuple[int, int],
                  walkable_fn: Optional[Any] = None) -> Tuple[Optional[List[Tuple[int, int]]], Dict[str, Any]]:
        stats = {"expanded_nodes": 0, "path_cost": 0.0, "visited_states": []}
        steps = list(self.find_path_stepper(grid, start, goal, walkable_fn))
        if not steps:
            return None, stats
        final_step = steps[-1]
        stats["expanded_nodes"] = final_step["expanded_count"]
        stats["visited_states"] = [s["current_pos"] for s in steps if "current_pos" in s]
        if final_step["status"] == "GOAL_REACHED":
            stats["path_cost"] = len(final_step["path"]) - 1
            return final_step["path"], stats
        return None, stats

    def find_path_stepper(self, grid: List[List[Any]], start: Tuple[int, int], goal: Tuple[int, int],
                          walkable_fn: Optional[Any] = None) -> Generator[Dict[str, Any], None, None]:
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        def is_walkable(pos: Tuple[int, int]) -> bool:
            x, y = pos
            if not (0 <= x < width and 0 <= y < height):
                return False
            if walkable_fn:
                return walkable_fn(pos)
            return True

        queue = deque([start])
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        visited: Set[Tuple[int, int]] = {start}
        expanded_count = 0

        yield {
            "status": "START",
            "current_pos": start,
            "queue_size": len(queue),
            "visited_count": len(visited),
            "expanded_count": 0,
            "message": f"Initialized BFS frontier at {start}."
        }

        while queue:
            current = queue.popleft()
            expanded_count += 1

            if current == goal:
                path = []
                curr: Optional[Tuple[int, int]] = current
                while curr:
                    path.append(curr)
                    curr = came_from.get(curr)
                path.reverse()

                yield {
                    "status": "GOAL_REACHED",
                    "current_pos": current,
                    "queue_size": len(queue),
                    "visited_count": len(visited),
                    "expanded_count": expanded_count,
                    "path": path,
                    "message": f"BFS discovered path of {len(path)} steps by expanding {expanded_count} nodes (uninformed brute force)."
                }
                return

            for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                nxt = (current[0] + dx, current[1] + dy)
                if is_walkable(nxt) and nxt not in visited:
                    visited.add(nxt)
                    came_from[nxt] = current
                    queue.append(nxt)

            yield {
                "status": "EXPANDING",
                "current_pos": current,
                "queue_size": len(queue),
                "visited_count": len(visited),
                "expanded_count": expanded_count,
                "message": f"BFS exploring breadth frontier: {current}. Visited states: {len(visited)}."
            }

        yield {
            "status": "NO_PATH",
            "queue_size": 0,
            "visited_count": len(visited),
            "expanded_count": expanded_count,
            "message": "BFS failed to locate a valid path."
        }
