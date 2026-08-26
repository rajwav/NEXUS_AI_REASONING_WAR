"""
NEXUS AI REASONING WAR - NOVA AI Companion
NOVA provides real-time dialogue, contextual hints, algorithm breakdowns,
and adaptive conversation tailored to Dr. Aarav Sharma's playing style.
"""

from typing import Dict, List, Optional, Tuple, Any
from ML.kmeans_analyzer import PlayerArchetype
from GameEngine.missions import MissionBase, MissionManager
from GameEngine.player import Player


class NovaCompanion:
    """Holographic AI companion that guides, explains, and solves alongside the player."""
    def __init__(self, name: str = "NOVA"):
        self.name = name
        self.personality_style = "Balanced & Supportive"
        self.hints_given_count = 0
        self.dialogue_history: List[Dict[str, str]] = []

    def greet(self, player_name: str) -> str:
        return (
            f"Greetings, {player_name}. Holographic systems synchronized.\n"
            f"I am {self.name}, your neural companion. I am monitoring campus telemetry, "
            f"environmental sensor arrays, and algorithmic state spaces. Press [N] anytime for advisory."
        )

    def provide_hint(self, active_mission: Optional[MissionBase],
                     player: Player, archetype: PlayerArchetype) -> Tuple[str, int]:
        """Provides an investigative, observational hint based on sensory scan rather than revealing solutions."""
        self.hints_given_count += 1
        player.stats.record_hint(hint_level=1)

        if not active_mission:
            return "NOVA Scan: Area is quiet. Move around the sector and inspect offline consoles or power nodes.", 0

        # Contextual investigative hints for Mission 1
        m1_hints = [
            "NOVA Sensory Scan: Thermal sensors show severe cryogenic coolant pooling around the central corridor. Direct routing through sub-zero relays will trip safety breakers unless stabilized.",
            "NOVA Observation: Maintenance logs left at the coolant console mention an engineering directive with three viable routing protocols.",
            "NOVA Circuit Telemetry: The northern bypass exhibits stable 120V nominal voltage with insulated copper conduits.",
            "NOVA Advice: If you have a Logic Probe in your tool deck, we can attempt a superconducting bridge through the high-frequency shunt."
        ]

        if active_mission.mission_id == "M01":
            hint_msg = m1_hints[(self.hints_given_count - 1) % len(m1_hints)]
        else:
            clues = active_mission.clues_found
            hint_msg = clues[(self.hints_given_count - 1) % max(1, len(clues))] if clues else "Scan data suggests cross-referencing nearby terminal logs."

        # Archetype tone modifier
        if archetype == PlayerArchetype.STRATEGIST:
            formatted_hint = f"🤖 [NOVA ANALYTICAL SCAN]\n\"{hint_msg}\"\n[Telemetry: Impedance balancing recommended.]"
        elif archetype == PlayerArchetype.HACKER:
            formatted_hint = f"🤖 [NOVA TACTICAL SCAN]\n\"{hint_msg}\"\n[Telemetry: Logic probe bypass available on flooded relays.]"
        elif archetype == PlayerArchetype.EXPLORER:
            formatted_hint = f"🤖 [NOVA RECONNAISSANCE]\n\"{hint_msg}\"\n[Telemetry: Check the corner terminal for unread maintenance memos.]"
        else:
            formatted_hint = f"🤖 [NOVA ASSISTANT]\n\"{hint_msg}\"\n[Tip: Walk up to terminals and press [E] to read diagnostics.]"

        self.dialogue_history.append({"speaker": "NOVA", "message": formatted_hint})
        return formatted_hint, self.hints_given_count

    def explain_algorithm(self, algorithm_name: str) -> str:
        """Educational breakdown of core AIML algorithms."""
        algo = algorithm_name.strip().upper()
        if "A*" in algo or "ASTAR" in algo:
            return (
                "=== ALGORITHM EXPLANATION: A* SEARCH ===\n"
                "• Type: Informed / Heuristic Graph Search.\n"
                "• Evaluation Function: f(n) = g(n) + h(n)\n"
                "  - g(n): Exact cost from start to current node.\n"
                "  - h(n): Estimated cost from current node to goal (Heuristic).\n"
                "• Optimality: Guaranteed optimal if heuristic h(n) is admissible (never overestimates real distance).\n"
                "• Efficiency: Expands far fewer nodes than BFS by prioritizing states with lowest f(n)."
            )
        elif "CSP" in algo or "BACKTRACKING" in algo:
            return (
                "=== ALGORITHM EXPLANATION: CONSTRAINT SATISFACTION (CSP) ===\n"
                "• Type: Constraint Satisfaction Problem with Backtracking Search.\n"
                "• Minimum Remaining Values (MRV): Chooses variable with smallest legal domain (Fail-First).\n"
                "• Degree Heuristic: Breaks ties by picking variable with most constraints on unassigned variables.\n"
                "• Forward Checking: Tracks domains of unassigned variables and prunes values violating constraints.\n"
                "• Backtracking: Rolls back state when any domain is emptied."
            )
        elif "MINIMAX" in algo or "ALPHA" in algo:
            return (
                "=== ALGORITHM EXPLANATION: MINIMAX WITH ALPHA-BETA PRUNING ===\n"
                "• Type: Adversarial Search for 2-player Zero-Sum Games.\n"
                "• Minimax Theorem: MAX selects move maximizing utility; MIN selects move minimizing MAX's utility.\n"
                "• Alpha: Best (highest) value MAX can guarantee so far.\n"
                "• Beta: Best (lowest) value MIN can guarantee so far.\n"
                "• Alpha-Beta Pruning: Prunes branches whenever alpha >= beta without affecting the optimal decision."
            )
        elif "FORWARD" in algo or "CHAINING" in algo:
            return (
                "=== ALGORITHM EXPLANATION: FORWARD CHAINING ===\n"
                "• Type: Data-Driven Logical Inference Engine using Horn Clauses.\n"
                "• Process: Starts with known atomic facts, matches premises of production rules (IF P THEN Q), and fires rules to deduce new facts until goal is proven or no new rules trigger."
            )
        elif "DECISION" in algo or "MEU" in algo or "UTILITY" in algo:
            return (
                "=== ALGORITHM EXPLANATION: MAXIMUM EXPECTED UTILITY (MEU) ===\n"
                "• Type: Decision Theory under Uncertainty.\n"
                "• Formula: U(a) = Sum_s' [ P(s' | a) * Utility(s') ]\n"
                "• Rational Decision Maker: Chooses action argmax_a U(a) balancing risks and multi-attribute rewards."
            )
        elif "STRIPS" in algo or "PLANNING" in algo:
            return (
                "=== ALGORITHM EXPLANATION: STRIPS AUTOMATED PLANNING ===\n"
                "• Type: Classical Goal-Oriented Action Planning (GOAP).\n"
                "• Components: States (set of propositional predicates), Actions (Preconditions, Add-List, Delete-List).\n"
                "• Goal: Finds a valid permutation of actions taking Initial State -> Goal State."
            )
        elif "MIN-CUT" in algo or "GRAPH" in algo:
            return (
                "=== ALGORITHM EXPLANATION: MINIMUM CUT & EDMONDS-KARP ===\n"
                "• Type: Network Flow & Graph Partitioning.\n"
                "• Max-Flow Min-Cut Theorem: The maximum amount of flow passing from source to sink equals the minimum capacity of edges that, if removed, completely disconnect source from sink."
            )
        else:
            return f"NOVA database has complete mathematical models for A*, BFS, CSP, Forward Chaining, Minimax, STRIPS, Decision Theory, and Min-Cut."
