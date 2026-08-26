"""
NEXUS AI REASONING WAR - Minimax with Alpha-Beta Pruning
Provides adversarial decision evaluation for turn-based combat in the Robot Training Arena,
displaying evaluated move branches, alpha-beta cutoffs, and utility scores.
"""

from typing import Dict, List, Tuple, Optional, Any, Generator
import copy
import math


class CombatAction:
    ATTACK = "KINETIC_STRIKE"   # Deals direct damage (15-25)
    DEFEND = "EMP_SHIELD"       # Blocks 70% incoming damage and reflects 5
    HACK = "CYBER_DISRUPTION"   # Drains 20 energy and damages 10
    CHARGE = "CHARGE_BATTERY"   # Restores 30 energy
    OVERCLOCK = "OVERCLOCK_BURST" # Consumes 40 energy for 45 damage


class GameState:
    """Represents state in the Robot Arena combat challenge."""
    def __init__(self, ai_hp: int = 100, ai_energy: int = 100,
                 player_hp: int = 100, player_energy: int = 100,
                 ai_shield: bool = False, player_shield: bool = False,
                 is_ai_turn: bool = True):
        self.ai_hp = max(0, min(100, ai_hp))
        self.ai_energy = max(0, min(100, ai_energy))
        self.player_hp = max(0, min(100, player_hp))
        self.player_energy = max(0, min(100, player_energy))
        self.ai_shield = ai_shield
        self.player_shield = player_shield
        self.is_ai_turn = is_ai_turn

    def is_terminal(self) -> bool:
        return self.ai_hp <= 0 or self.player_hp <= 0

    def evaluate_utility(self) -> float:
        """Utility function from AI (ARES-7) perspective."""
        if self.ai_hp <= 0:
            return -1000.0  # Loss
        if self.player_hp <= 0:
            return 1000.0   # Win
        
        # Heuristic utility balance
        hp_diff = (self.ai_hp - self.player_hp) * 3.0
        energy_diff = (self.ai_energy - self.player_energy) * 0.8
        shield_bonus = (15.0 if self.ai_shield else 0.0) - (15.0 if self.player_shield else 0.0)
        return hp_diff + energy_diff + shield_bonus

    def get_legal_actions(self, is_ai: bool) -> List[str]:
        energy = self.ai_energy if is_ai else self.player_energy
        actions = [CombatAction.ATTACK, CombatAction.DEFEND, CombatAction.CHARGE]
        if energy >= 20:
            actions.append(CombatAction.HACK)
        if energy >= 40:
            actions.append(CombatAction.OVERCLOCK)
        return actions

    def apply_action(self, action: str, is_ai: bool) -> 'GameState':
        """Returns new state after executing action."""
        next_state = copy.deepcopy(self)
        next_state.is_ai_turn = not is_ai

        if is_ai:
            next_state.ai_shield = False
            if action == CombatAction.ATTACK:
                dmg = 20
                if next_state.player_shield:
                    dmg = int(dmg * 0.3)
                    next_state.ai_hp = max(0, next_state.ai_hp - 5)
                next_state.player_hp = max(0, next_state.player_hp - dmg)
            elif action == CombatAction.DEFEND:
                next_state.ai_shield = True
            elif action == CombatAction.HACK:
                next_state.ai_energy = max(0, next_state.ai_energy - 20)
                next_state.player_energy = max(0, next_state.player_energy - 20)
                next_state.player_hp = max(0, next_state.player_hp - 10)
            elif action == CombatAction.CHARGE:
                next_state.ai_energy = min(100, next_state.ai_energy + 30)
            elif action == CombatAction.OVERCLOCK:
                next_state.ai_energy = max(0, next_state.ai_energy - 40)
                dmg = 45
                if next_state.player_shield:
                    dmg = int(dmg * 0.3)
                next_state.player_hp = max(0, next_state.player_hp - dmg)
        else:
            next_state.player_shield = False
            if action == CombatAction.ATTACK:
                dmg = 20
                if next_state.ai_shield:
                    dmg = int(dmg * 0.3)
                    next_state.player_hp = max(0, next_state.player_hp - 5)
                next_state.ai_hp = max(0, next_state.ai_hp - dmg)
            elif action == CombatAction.DEFEND:
                next_state.player_shield = True
            elif action == CombatAction.HACK:
                next_state.player_energy = max(0, next_state.player_energy - 20)
                next_state.ai_energy = max(0, next_state.ai_energy - 20)
                next_state.ai_hp = max(0, next_state.ai_hp - 10)
            elif action == CombatAction.CHARGE:
                next_state.player_energy = min(100, next_state.player_energy + 30)
            elif action == CombatAction.OVERCLOCK:
                next_state.player_energy = max(0, next_state.player_energy - 40)
                dmg = 45
                if next_state.ai_shield:
                    dmg = int(dmg * 0.3)
                next_state.ai_hp = max(0, next_state.ai_hp - dmg)

        return next_state


class MinimaxEngine:
    """Minimax Evaluator with Alpha-Beta Pruning and live visual thought traces."""
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.pruning_cutoffs = 0

    def select_best_action(self, state: GameState, is_ai: bool = True) -> Tuple[str, float, Dict[str, Any]]:
        """Instant best move selection."""
        steps = list(self.evaluate_stepper(state, is_ai))
        final_step = steps[-1] if steps else {}
        stats = {
            "nodes_evaluated": self.nodes_evaluated,
            "pruning_cutoffs": self.pruning_cutoffs,
            "all_move_evaluations": final_step.get("move_evaluations", {})
        }
        return final_step.get("best_action", CombatAction.ATTACK), final_step.get("best_value", 0.0), stats

    def evaluate_stepper(self, state: GameState, is_ai: bool = True) -> Generator[Dict[str, Any], None, None]:
        """
        Step-by-step generator yielding tree evaluation branch by branch.
        """
        self.nodes_evaluated = 0
        self.pruning_cutoffs = 0
        legal_actions = state.get_legal_actions(is_ai)

        yield {
            "status": "START",
            "depth": 0,
            "legal_actions": legal_actions,
            "message": f"Minimax initializing game tree expansion (depth={self.max_depth}) across {len(legal_actions)} actions."
        }

        best_action = legal_actions[0]
        best_value = -math.inf if is_ai else math.inf
        alpha = -math.inf
        beta = math.inf
        move_evaluations: Dict[str, float] = {}

        for action in legal_actions:
            next_state = state.apply_action(action, is_ai)
            val = self._minimax_value(next_state, self.max_depth - 1, alpha, beta, not is_ai)
            move_evaluations[action] = round(val, 2)

            if is_ai:
                if val > best_value:
                    best_value = val
                    best_action = action
                alpha = max(alpha, val)
            else:
                if val < best_value:
                    best_value = val
                    best_action = action
                beta = min(beta, val)

            yield {
                "status": "ACTION_EVALUATED",
                "action": action,
                "score": round(val, 2),
                "current_best": best_action,
                "current_best_score": round(best_value, 2),
                "alpha": round(alpha, 2),
                "beta": round(beta, 2),
                "message": f"Evaluated action [{action}] -> Projected Utility: {round(val, 2)}."
            }

        yield {
            "status": "DECISION_FINALIZED",
            "best_action": best_action,
            "best_value": round(best_value, 2),
            "move_evaluations": move_evaluations,
            "nodes_evaluated": self.nodes_evaluated,
            "pruning_cutoffs": self.pruning_cutoffs,
            "message": f"Minimax finalized decision: [{best_action}] with utility {round(best_value, 2)} ({self.pruning_cutoffs} branches pruned)."
        }

    def _minimax_value(self, state: GameState, depth: int, alpha: float, beta: float, is_max: bool) -> float:
        self.nodes_evaluated += 1
        if depth == 0 or state.is_terminal():
            return state.evaluate_utility()

        actions = state.get_legal_actions(is_max)

        if is_max:
            max_eval = -math.inf
            for act in actions:
                nxt = state.apply_action(act, True)
                eval_val = self._minimax_value(nxt, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    self.pruning_cutoffs += 1
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = math.inf
            for act in actions:
                nxt = state.apply_action(act, False)
                eval_val = self._minimax_value(nxt, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha:
                    self.pruning_cutoffs += 1
                    break  # Alpha cut-off
            return min_eval
