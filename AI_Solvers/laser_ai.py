"""
AI Solver for Laser Mirror Routing
Algorithm: Beam Raytracing Simulation and Combinatorial Search.
"""

from typing import List, Tuple, Set, Dict, Any, Optional
import itertools
from AI_Agent.explanation_recorder import ExplanationRecorder


class LaserAISolver:
    def __init__(self, width: int, height: int, emitters: List[Dict], detectors: List[Tuple[int, int]],
                 obstacles: Set[Tuple[int, int]], initial_mirrors: Dict[Tuple[int, int], str]):
        self.width = width
        self.height = height
        self.emitters = emitters
        self.detectors = {tuple(d) if isinstance(d, (list, tuple)) else d for d in detectors}
        self.obstacles = {tuple(o) if isinstance(o, (list, tuple)) else o for o in obstacles}
        self.initial_mirrors = {tuple(k) if isinstance(k, (list, tuple)) else k: v for k, v in dict(initial_mirrors).items()}
        self.mirror_keys = list(self.initial_mirrors.keys())
        self.states_evaluated = 0
        self.recorder = ExplanationRecorder()

    def trace_beams(self, current_mirrors: Dict[Tuple[int, int], str]) -> Tuple[List[List[Tuple[int, int]]], Set[Tuple[int, int]]]:
        paths = []
        activated_detectors = set()

        for em in self.emitters:
            path = [(em["pos"][0], em["pos"][1])]
            cx, cy = em["pos"][0], em["pos"][1]
            dx, dy = em["dir"][0], em["dir"][1]

            for _ in range(64):
                cx += dx
                cy += dy
                if cx < 0 or cx >= self.width or cy < 0 or cy >= self.height:
                    break
                path.append((cx, cy))
                if (cx, cy) in self.obstacles:
                    break
                if (cx, cy) in self.detectors:
                    activated_detectors.add((cx, cy))
                if (cx, cy) in current_mirrors:
                    m = current_mirrors[(cx, cy)]
                    if m == "/":
                        dx, dy = -dy, -dx
                    elif m == "\\":
                        dx, dy = dy, dx
            paths.append(path)

        return paths, activated_detectors

    def solve(self) -> Dict[str, Any]:
        """Finds mirror rotation assignment that activates all detectors."""
        self.states_evaluated = 0
        n_mirrors = len(self.mirror_keys)

        self.recorder.start_session(
            game_id="laser",
            algorithm="Optical Raytracing + Combinatorial Vector Search",
            complexity_class=f"O(2^{n_mirrors}) discrete mirror orientation space",
            theory_overview="AI simulates optical photons reflecting at 45°/135° across continuous grid vectors, pruning configurations that fail to energize all detector targets.",
            root_label="Initial Optical Matrix",
            root_state_summary=f"{n_mirrors} reconfigurable mirrors, {len(self.detectors)} target detector cores"
        )

        # Evaluate initial state first
        _, initial_act = self.trace_beams(self.initial_mirrors)
        if len(initial_act) == len(self.detectors):
            self.recorder.add_metric("states_evaluated", 1)
            self.recorder.add_metric("mirrors_rotated", 0)
            self.recorder.add_metric("activated_detectors", f"{len(initial_act)}/{len(self.detectors)}")
            
            return {
                "solved": True,
                "algorithm": "Optical Raytrace + Combinatorial Search",
                "states_evaluated": 1,
                "steps": [],
                "final_mirrors": self.initial_mirrors,
                "explanation_data": self.recorder.finish_session()
            }

        total_combos = 2 ** n_mirrors
        parent_tree_id = "root"

        # Search mirror orientation combinations
        for combo in itertools.product(["/", "\\"], repeat=n_mirrors):
            self.states_evaluated += 1
            test_mirrors = {k: combo[i] for i, k in enumerate(self.mirror_keys)}
            paths, activated = self.trace_beams(test_mirrors)

            if len(activated) == len(self.detectors):
                # Formulate step-by-step diff from initial
                steps = []
                for idx, k in enumerate(self.mirror_keys):
                    orig = self.initial_mirrors[k]
                    new_val = test_mirrors[k]
                    if orig != new_val:
                        step_idx = len(steps) + 1
                        node_id = f"laser_rot_{step_idx}"
                        
                        step_item = {
                            "x": k[0],
                            "y": k[1],
                            "from_type": orig,
                            "to_type": new_val,
                            "reflection_angle": "45° / 135° Optics",
                            "testing_rotation": f"Config {self.states_evaluated}/{total_combos}",
                            "active_detectors": f"{len(activated)}/{len(self.detectors)}",
                            "simulation_trace": "Emitter ⚡ ➔ Mirror ➔ Reflection ➔ Detector 🔮",
                            "reason": f"Optical Solver: Rotated mirror at ({k[0]},{k[1]}) from '{orig}' to '{new_val}' to redirect beam into target detector."
                        }
                        steps.append(step_item)

                        # Record Search Tree Node
                        self.recorder.add_tree_node(
                            node_id=node_id,
                            parent_id=parent_tree_id,
                            label=f"Mirror ({k[0]},{k[1]}): {orig} -> {new_val}",
                            action=f"Rotate to '{new_val}'",
                            status="ACCEPTED",
                            state_summary=f"Active detectors: {len(activated)}/{len(self.detectors)}",
                            reason=step_item["reason"]
                        )
                        parent_tree_id = node_id

                        # Record Timeline Step
                        self.recorder.add_decision(
                            step_index=step_idx,
                            type="ROTATE",
                            selected_target=f"Mirror at ({k[0]}, {k[1]})",
                            candidates_domain=["/", "\\"],
                            chosen_value=new_val,
                            rejected_alternatives=[orig],
                            constraint_checks={"Optical Path": "✓ Continuous", "Target Alignment": f"{len(activated)}/{len(self.detectors)} Cores"},
                            decision_outcome="ACCEPTED",
                            rationale=f"Orienting mirror at ({k[0]},{k[1]}) to '{new_val}' reflects optical ray onto target trajectory.",
                            theory_principle="Laser reflection transforms incident vector (dx, dy) to (-dy, -dx) for '/' and (dy, dx) for '\\\\'.",
                            state_snapshot={"x": k[0], "y": k[1], "orientation": new_val},
                            tree_node_ref=node_id
                        )

                self.recorder.add_tree_node(
                    node_id="laser_goal",
                    parent_id=parent_tree_id,
                    label="ALL DETECTORS ENERGIZED 🔮",
                    action="OPTICAL HARMONY",
                    status="GOAL",
                    state_summary=f"{len(self.detectors)}/{len(self.detectors)} detectors active",
                    reason="Laser beam forms an uninterrupted optical path powering all detector cores."
                )

                self.recorder.add_metric("states_evaluated", self.states_evaluated)
                self.recorder.add_metric("total_rotations", len(steps))
                self.recorder.add_metric("total_combinations", total_combos)
                self.recorder.add_metric("activated_detectors", f"{len(activated)}/{len(self.detectors)}")

                return {
                    "solved": True,
                    "algorithm": "Ray Tracing + Combinatorial Search",
                    "states_evaluated": self.states_evaluated,
                    "total_rotations": len(steps),
                    "steps": steps,
                    "final_mirrors": test_mirrors,
                    "explanation_data": self.recorder.finish_session()
                }

        return {
            "solved": False,
            "algorithm": "Ray Tracing + Combinatorial Search",
            "states_evaluated": self.states_evaluated,
            "total_rotations": 0,
            "steps": [],
            "final_mirrors": self.initial_mirrors,
            "explanation_data": self.recorder.finish_session()
        }
