"""
NEXUS AI REASONING WAR - Mission 8: Robot Escape Challenge
Algorithm Concept: STRIPS Automated Planning & Goal-Oriented Action Planning (GOAP)
Sector: Robot Training Arena
Gameplay: Formulate an automated action plan with Preconditions and Add/Delete lists
to evacuate locked repair drones through the security airlock.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator, Set
from .mission_base import MissionBase, MissionStatus
from AI_Algorithms.strips_planner import STRIPSPlanner, Action, State
from GameEngine.objects import Item


class Mission08RobotEscape(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M08",
            title="Automated Drone Evacuation Planning",
            sector_name="Sector 2: Robot Training Arena",
            algorithm_concept="STRIPS Action Planning & State Progression",
            description="Maintenance drones are trapped inside containment bay Alpha. Synthesize an ordered sequence of actions satisfying state preconditions to unlock the airlock and evacuate the drones."
        )
        self.initial_state_preds = {
            "drone_at_bay", "door_locked", "power_offline", "keycard_in_safe", "safe_locked", "player_has_logic_probe"
        }
        self.goal_preds = {"drone_evacuated", "door_open"}
        self.actions = self._build_strips_actions()
        self.clues_found = [
            "Airlock requirement: Drone cannot move through airlock unless door is unlocked and power is online.",
            "Safe mechanism: Safe can be bypassed using the Logic Probe, revealing Keycard-3.",
            "Generator condition: Power requires Keycard-3 authorization to engage the main breaker."
        ]
        self.reward_items = [
            Item("ITEM_QUANTUM_STABILIZER", "Sub-atomic Quantum Stabilizer",
                 "Stabilizes energy fluctuation during hyper-dimensional computation.",
                 category="TOOL")
        ]

    def _build_strips_actions(self) -> List[Action]:
        return [
            Action(
                "hack_safe_with_probe",
                preconditions={"player_has_logic_probe", "safe_locked"},
                add_effects={"safe_unlocked", "has_keycard3"},
                delete_effects={"safe_locked"},
                description="Use Logic Probe to bypass electronic safe lock and grab Keycard-3."
            ),
            Action(
                "activate_generator",
                preconditions={"has_keycard3", "power_offline"},
                add_effects={"power_online"},
                delete_effects={"power_offline"},
                description="Authorize auxiliary breaker with Keycard-3 and bring power online."
            ),
            Action(
                "unlock_airlock_door",
                preconditions={"has_keycard3", "power_online", "door_locked"},
                add_effects={"door_open"},
                delete_effects={"door_locked"},
                description="Unlock and slide open the reinforced containment airlock door."
            ),
            Action(
                "evacuate_drone",
                preconditions={"door_open", "power_online", "drone_at_bay"},
                add_effects={"drone_evacuated"},
                delete_effects={"drone_at_bay"},
                description="Signal drone autonomous navigation system to transit to safety."
            )
        ]

    def solve_interactive_human(self, action_sequence: List[str]) -> Tuple[bool, str, Dict[str, Any]]:
        """Human submits an ordered action sequence."""
        curr_state = State(self.initial_state_preds)
        action_map = {a.name: a for a in self.actions}

        for act_name in action_sequence:
            if act_name not in action_map:
                return False, f"Unknown action: {act_name}", {}

            action_obj = action_map[act_name]
            if not action_obj.is_applicable(curr_state):
                missing = action_obj.preconditions - curr_state.predicates
                return False, (
                    f"PRECONDITION FAILURE on action [{act_name}]!\n"
                    f"Missing required state predicates: {list(missing)}."
                ), {"failed_action": act_name, "state": list(curr_state.predicates)}

            curr_state = curr_state.apply(action_obj)

        if curr_state.satisfies(self.goal_preds):
            self.complete(solved_by_ai=False)
            return True, (
                f"AUTOMATED EVACUATION PLAN VALIDATED!\n"
                f"Executed {len(action_sequence)} STRIPS actions successfully.\n"
                "All maintenance drones evacuated safely to Sector 1. Quantum Stabilizer acquired!"
            ), {"plan": action_sequence, "final_state": list(curr_state.predicates)}
        else:
            missing_goals = self.goal_preds - curr_state.predicates
            return False, f"Plan ended but goal predicates {list(missing_goals)} not achieved.", {}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        planner = STRIPSPlanner(State(self.initial_state_preds), self.goal_preds, self.actions)
        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Synthesizing forward state-space progression plan using STRIPS..."
        }

        for step in planner.plan_stepper():
            yield step

        self.complete(solved_by_ai=True)
