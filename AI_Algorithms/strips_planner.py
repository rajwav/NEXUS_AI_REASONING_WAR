"""
NEXUS AI REASONING WAR - STRIPS Automated Planning Engine
Provides Goal-Oriented Action Planning (GOAP) with Preconditions,
Add-Effects, and Delete-Effects to solve the Robot Escape Challenge.
"""

from typing import Set, List, Dict, Tuple, Optional, Any, Generator
from collections import deque
import copy


class State:
    def __init__(self, predicates: Set[str]):
        self.predicates = set(predicates)

    def satisfies(self, conditions: Set[str]) -> bool:
        return conditions.issubset(self.predicates)

    def apply(self, action: 'Action') -> 'State':
        new_preds = (self.predicates - action.delete_effects) | action.add_effects
        return State(new_preds)

    def __eq__(self, other):
        if isinstance(other, State):
            return self.predicates == other.predicates
        return False

    def __hash__(self):
        return hash(frozenset(self.predicates))

    def __repr__(self):
        return f"State({sorted(list(self.predicates))})"


class Action:
    def __init__(self, name: str, preconditions: Set[str],
                 add_effects: Set[str], delete_effects: Set[str],
                 cost: float = 1.0, description: str = ""):
        self.name = name
        self.preconditions = set(preconditions)
        self.add_effects = set(add_effects)
        self.delete_effects = set(delete_effects)
        self.cost = cost
        self.description = description or name

    def is_applicable(self, state: State) -> bool:
        return state.satisfies(self.preconditions)

    def __repr__(self):
        return f"Action({self.name})"


class STRIPSPlanner:
    """State-space forward progression search for linear and branched action plans."""
    def __init__(self, initial_state: State, goal_conditions: Set[str], actions: List[Action]):
        self.initial_state = initial_state
        self.goal_conditions = set(goal_conditions)
        self.actions = actions

    def plan(self) -> Tuple[Optional[List[Action]], Dict[str, Any]]:
        steps = list(self.plan_stepper())
        final = steps[-1] if steps else {}
        stats = {
            "expanded_states": final.get("expanded_count", 0),
            "plan_length": len(final.get("plan", [])) if final.get("plan") else 0
        }
        return final.get("plan"), stats

    def plan_stepper(self) -> Generator[Dict[str, Any], None, None]:
        queue = deque([(self.initial_state, [])])
        visited: Set[State] = {self.initial_state}
        expanded_count = 0

        yield {
            "status": "INIT",
            "current_state": sorted(list(self.initial_state.predicates)),
            "goal": sorted(list(self.goal_conditions)),
            "expanded_count": 0,
            "message": f"STRIPS Planner initialized with goal: {sorted(list(self.goal_conditions))}."
        }

        while queue:
            current_state, plan_so_far = queue.popleft()
            expanded_count += 1

            if current_state.satisfies(self.goal_conditions):
                yield {
                    "status": "GOAL_REACHED",
                    "plan": plan_so_far,
                    "plan_names": [a.name for a in plan_so_far],
                    "plan_descriptions": [a.description for a in plan_so_far],
                    "final_state": sorted(list(current_state.predicates)),
                    "expanded_count": expanded_count,
                    "message": f"STRIPS Plan constructed! Total actions: {len(plan_so_far)} steps."
                }
                return

            for act in self.actions:
                if act.is_applicable(current_state):
                    next_state = current_state.apply(act)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, plan_so_far + [act]))

            yield {
                "status": "EXPANDING",
                "current_state": sorted(list(current_state.predicates)),
                "plan_so_far": [a.name for a in plan_so_far],
                "expanded_count": expanded_count,
                "message": f"Exploring planning state with {len(visited)} states visited."
            }

        yield {
            "status": "NO_PLAN",
            "expanded_count": expanded_count,
            "message": "STRIPS planning failed: Goal conditions cannot be reached from initial state."
        }
