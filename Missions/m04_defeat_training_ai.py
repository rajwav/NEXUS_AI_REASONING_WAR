"""
NEXUS AI REASONING WAR - Mission 4: Defeat Training AI (ARES-7)
Algorithm Concept: Minimax Algorithm with Alpha-Beta Pruning
Sector: Robot Training Arena
Gameplay: Tactical turn-based combat against ARES-7 Combat Drone.
Show live decision tree evaluation and anticipated moves.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator
from .mission_base import MissionBase, MissionStatus
from AI_Algorithms.minimax import MinimaxEngine, GameState, CombatAction
from GameEngine.objects import Item


class Mission04DefeatTrainingAI(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M04",
            title="Combat Simulation: Defeat Sentry Bot ARES-7",
            sector_name="Sector 2: Robot Training Arena",
            algorithm_concept="Game Theory & Minimax with Alpha-Beta Pruning",
            description="ARES-7 has entered rogue combat simulation mode. Engage in tactical turn-based battle, anticipating its Minimax decision tree calculations."
        )
        self.clues_found = [
            "Tactics Intel: ARES-7 evaluates moves 3 turns ahead using Alpha-Beta pruning.",
            "Energy analysis: ARES-7 requires 40 energy for Overclock Burst and 20 for Cyber Hack.",
            "Counter-strategy: Activating EMP Shield immediately reflects damage and drains enemy kinetic momentum."
        ]
        self.reward_items = [
            Item("ITEM_COMBAT_CORE", "Overclocked Combat Core",
                 "High-throughput processor salvaged from ARES-7.",
                 category="CHIP"),
            Item("KEY_NEXUS_PRIME", "Gold Master Keycard (NEXUS Prime)",
                 "Highest security clearance granting access to the Final Nexus Chamber.",
                 category="KEYCARD")
        ]

    def create_initial_combat_state(self) -> GameState:
        return GameState(ai_hp=100, ai_energy=100, player_hp=100, player_energy=100, is_ai_turn=False)

    def execute_turn(self, state: GameState, player_action: str) -> Tuple[GameState, str, Dict[str, Any]]:
        """Executes player move followed by ARES-7 Minimax move."""
        # 1. Apply Player move
        after_player = state.apply_action(player_action, is_ai=False)
        if after_player.is_terminal():
            if after_player.ai_hp <= 0:
                self.complete(solved_by_ai=False)
                return after_player, "VICTORY! ARES-7 Combat Systems neutralized. Master Keycard retrieved!", {}
            else:
                return after_player, "DEFEAT! Your chassis took critical damage.", {}

        # 2. AI calculates counter-move using Minimax
        engine = MinimaxEngine(max_depth=3)
        ai_action, ai_val, stats = engine.select_best_action(after_player, is_ai=True)
        after_ai = after_player.apply_action(ai_action, is_ai=True)

        if after_ai.is_terminal():
            if after_ai.ai_hp <= 0:
                self.complete(solved_by_ai=False)
                return after_ai, "VICTORY! ARES-7 neutralized!", stats
            else:
                return after_ai, "DEFEAT! Player health reached 0.", stats

        msg = f"You used [{player_action}]. ARES-7 countered with [{ai_action}] (Utility Score: {ai_val})."
        return after_ai, msg, stats

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        """NOVA takes over combat actions, playing optimal minimax responses."""
        engine = MinimaxEngine(max_depth=3)
        state = self.create_initial_combat_state()

        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Linking directly to tactical combat processor. Initiating optimal counter-moves..."
        }

        turn = 1
        while not state.is_terminal() and turn <= 10:
            # NOVA (as player) chooses optimal minimax move
            p_action, p_val, _ = engine.select_best_action(state, is_ai=False)
            state = state.apply_action(p_action, is_ai=False)

            yield {
                "status": "NOVA_PLAYER_MOVE",
                "turn": turn,
                "action": p_action,
                "state": {
                    "player_hp": state.player_hp, "player_energy": state.player_energy,
                    "ai_hp": state.ai_hp, "ai_energy": state.ai_energy
                },
                "message": f"Turn {turn}: NOVA executed [{p_action}]."
            }

            if state.is_terminal():
                break

            # Opponent AI moves
            ai_action, ai_val, _ = engine.select_best_action(state, is_ai=True)
            state = state.apply_action(ai_action, is_ai=True)

            yield {
                "status": "OPPONENT_AI_MOVE",
                "turn": turn,
                "action": ai_action,
                "state": {
                    "player_hp": state.player_hp, "player_energy": state.player_energy,
                    "ai_hp": state.ai_hp, "ai_energy": state.ai_energy
                },
                "message": f"Turn {turn}: ARES-7 responded with [{ai_action}]."
            }
            turn += 1

        if state.ai_hp <= 0:
            self.complete(solved_by_ai=True)
            yield {
                "status": "NOVA_COMBAT_VICTORY",
                "message": "NOVA successfully defeated ARES-7 via Minimax optimal equilibrium!"
            }
