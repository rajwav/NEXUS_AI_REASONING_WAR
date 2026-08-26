"""
AI Solver for Cyber Sokoban
Algorithm: A* Search / BFS with Deadlock Detection and Manhattan Distance Heuristic.
"""

from typing import List, Tuple, Set, Dict, Optional, Any
import collections
import heapq
from AI_Agent.explanation_recorder import ExplanationRecorder


class SokobanAISolver:
    def __init__(self, walls: Set[Tuple[int, int]], targets: Set[Tuple[int, int]],
                 boxes: Set[Tuple[int, int]], player: Tuple[int, int]):
        self.walls = set(walls)
        self.targets = set(targets)
        self.initial_boxes = set(boxes)
        self.initial_player = player
        self.states_evaluated = 0
        self.recorder = ExplanationRecorder()

    def is_deadlock(self, bx: int, by: int, current_boxes: Set[Tuple[int, int]]) -> bool:
        if (bx, by) in self.targets:
            return False
        # Corner Deadlock
        has_vert = (bx, by - 1) in self.walls or (bx, by + 1) in self.walls
        has_horiz = (bx - 1, by) in self.walls or (bx + 1, by) in self.walls
        if has_vert and has_horiz:
            return True
        return False

    def heuristic(self, boxes: Set[Tuple[int, int]]) -> int:
        """Sum of minimum Manhattan distances from each box to its nearest unassigned target."""
        total = 0
        unmatched_targets = list(self.targets)
        for bx, by in boxes:
            if (bx, by) in self.targets:
                continue
            min_dist = min((abs(bx - tx) + abs(by - ty) for tx, ty in unmatched_targets), default=0)
            total += min_dist
        return total

    def solve(self, max_expansions: int = 6000) -> Dict[str, Any]:
        """A* Search to find optimal push/move sequence."""
        self.states_evaluated = 0
        start_boxes = tuple(sorted(self.initial_boxes))
        start_state = (self.initial_player, start_boxes)

        h0 = self.heuristic(self.initial_boxes)
        pq = [(h0, 0, start_state, [])]
        visited = {start_state: 0}

        self.recorder.start_session(
            game_id="sokoban",
            algorithm="A* Search + Deadlock Detection Pruning",
            complexity_class="O(b^d) state space with heuristic branch pruning",
            theory_overview="A* Search expands search nodes in order of minimum f(n) = g(n) + h(n), where g(n) is step cost and h(n) is admissible Manhattan distance to targets.",
            root_label="Initial Sokoban State",
            root_state_summary=f"Robot at {self.initial_player}, {len(self.initial_boxes)} energy cores"
        )

        dir_names = {
            (0, -1): ("UP", "▲"),
            (0, 1): ("DOWN", "▼"),
            (-1, 0): ("LEFT", "◄"),
            (1, 0): ("RIGHT", "►")
        }

        deadlocks_pruned = 0

        while pq and self.states_evaluated < max_expansions:
            self.states_evaluated += 1
            f, g, (player, boxes_tuple), path = heapq.heappop(pq)
            boxes_set = set(boxes_tuple)

            # Goal test
            if boxes_set == self.targets:
                # Build explanation timeline & search tree from optimal path
                parent_tree_id = "root"
                for s_idx, action in enumerate(path):
                    node_id = f"soko_step_{s_idx + 1}"
                    is_push = action["is_push"]
                    dname = action["dir_name"]
                    p_pos = action["player"]
                    
                    self.recorder.add_tree_node(
                        node_id=node_id,
                        parent_id=parent_tree_id,
                        label=f"{dname} {'⚡ Push' if is_push else 'Move'}",
                        action=f"Move {dname} to {p_pos}",
                        status="ACCEPTED",
                        state_summary=f"g={action['g']}, h={action['h']}, f={action['f']}",
                        cost_g=action["g"],
                        cost_h=action["h"],
                        cost_f=action["f"],
                        reason=action["reason"]
                    )
                    parent_tree_id = node_id

                    self.recorder.add_decision(
                        step_index=s_idx + 1,
                        type="PUSH" if is_push else "MOVE",
                        selected_target=f"Robot -> {p_pos}",
                        candidates_domain=["UP", "DOWN", "LEFT", "RIGHT"],
                        chosen_value=f"{dname} ({'Push Box' if is_push else 'Step'})",
                        rejected_alternatives=[d for d in ["UP", "DOWN", "LEFT", "RIGHT"] if d != dname],
                        constraint_checks={"Wall Collision": "✓ Clear", "Deadlock Check": "✓ Clear", "Frontier Priority": f"f={action['f']}"},
                        decision_outcome="OPTIMAL",
                        rationale=f"A* expanded direction {dname} with lowest evaluation function f(n) = {action['g']} + {action['h']} = {action['f']}.",
                        theory_principle="A* optimality guarantees shortest path when using admissible Manhattan distance heuristics h(n) <= h*(n).",
                        state_snapshot={"player": p_pos, "is_push": is_push, "g": action["g"], "h": action["h"], "f": action["f"]},
                        tree_node_ref=node_id
                    )

                self.recorder.add_tree_node(
                    node_id="soko_goal",
                    parent_id=parent_tree_id,
                    label="ALL CORES ENERGIZED 🎯",
                    action="GOAL REACHED",
                    status="GOAL",
                    state_summary=f"{len(self.targets)}/{len(self.targets)} cores on target pads",
                    reason="All energy cores pushed onto designated target coordinates."
                )

                self.recorder.add_metric("states_evaluated", self.states_evaluated)
                self.recorder.add_metric("total_moves", len(path))
                self.recorder.add_metric("total_pushes", sum(1 for a in path if a["is_push"]))
                self.recorder.add_metric("deadlocks_pruned", deadlocks_pruned)
                self.recorder.add_metric("open_queue_size", len(pq))

                return {
                    "solved": True,
                    "algorithm": "A* Search + Deadlock Detection",
                    "states_evaluated": self.states_evaluated,
                    "total_moves": len(path),
                    "total_pushes": sum(1 for a in path if a["is_push"]),
                    "steps": path,
                    "explanation_data": self.recorder.finish_session()
                }

            px, py = player
            for (dx, dy), (dname, dicon) in dir_names.items():
                nx, ny = px + dx, py + dy
                if (nx, ny) in self.walls:
                    continue

                if (nx, ny) in boxes_set:
                    # Push box
                    bx, by = nx + dx, ny + dy
                    if (bx, by) in self.walls or (bx, by) in boxes_set:
                        continue
                    if self.is_deadlock(bx, by, boxes_set):
                        deadlocks_pruned += 1
                        continue

                    new_boxes = set(boxes_set)
                    new_boxes.remove((nx, ny))
                    new_boxes.add((bx, by))
                    nxt_state = ((nx, ny), tuple(sorted(new_boxes)))

                    new_g = g + 1
                    if nxt_state not in visited or new_g < visited[nxt_state]:
                        visited[nxt_state] = new_g
                        h = self.heuristic(new_boxes)
                        f_score = new_g + h
                        action = {
                            "dx": dx, "dy": dy,
                            "player": (nx, ny),
                            "box_from": (nx, ny),
                            "box_to": (bx, by),
                            "is_push": True,
                            "dir_name": dname,
                            "g": new_g,
                            "h": h,
                            "f": f_score,
                            "open_list": len(pq) + 1,
                            "closed_list": len(visited),
                            "state_id": self.states_evaluated,
                            "deadlock_prob": "0% (Pruned)",
                            "reason": f"A* Push {dname} {dicon}: box ({nx},{ny}) -> ({bx},{by}) | g={new_g}, h={h}, f={f_score}."
                        }
                        heapq.heappush(pq, (f_score, new_g, nxt_state, path + [action]))
                else:
                    # Regular move
                    nxt_state = ((nx, ny), boxes_tuple)
                    new_g = g + 1
                    if nxt_state not in visited or new_g < visited[nxt_state]:
                        visited[nxt_state] = new_g
                        h = self.heuristic(boxes_set)
                        f_score = new_g + h
                        action = {
                            "dx": dx, "dy": dy,
                            "player": (nx, ny),
                            "is_push": False,
                            "dir_name": dname,
                            "g": new_g,
                            "h": h,
                            "f": f_score,
                            "open_list": len(pq) + 1,
                            "closed_list": len(visited),
                            "state_id": self.states_evaluated,
                            "deadlock_prob": "0% (Safe)",
                            "reason": f"A* Maneuver {dname} {dicon}: robot to ({nx},{ny}) | g={new_g}, h={h}, f={f_score}."
                        }
                        heapq.heappush(pq, (f_score, new_g, nxt_state, path + [action]))

        return {
            "solved": False,
            "algorithm": "A* Search (Manhattan Distance + Deadlock Pruning)",
            "states_evaluated": self.states_evaluated,
            "total_moves": 0,
            "total_pushes": 0,
            "steps": [],
            "explanation_data": self.recorder.finish_session()
        }
