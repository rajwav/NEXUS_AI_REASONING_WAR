"""
NEXUS AI REASONING WAR - Mission 9: Adaptive AI Test
Algorithm Concept: Machine Learning Decision Boundaries & Adversarial Perturbation
Sector: Quantum Security Lab
Gameplay: An adaptive learning firewall learns your pattern. Inject strategic adversarial
data points to shift its classification boundary and bypass the gate.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator
from .mission_base import MissionBase, MissionStatus
from GameEngine.objects import Item
import math


class Mission09AdaptiveAITest(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M09",
            title="Adaptive Machine Learning Firewall Test",
            sector_name="Sector 3: Quantum Security Lab",
            algorithm_concept="Machine Learning Classification & Adversarial Boundary Shift",
            description="The Quantum Security gateway uses a dynamic linear classifier w·x + b = 0. Identify the classifier weights and inject 3 adversarial frequency vectors to flip the decision boundary from REJECT to PASS."
        )
        # Decision boundary: 0.6*x1 - 0.8*x2 + 0.1 > 0 => REJECT, <= 0 => PASS
        self.w = [0.60, -0.80]
        self.b = 0.10
        self.clues_found = [
            "Diagnostic terminal: Firewall classifies packet vector (x1, x2) as ALLOW if 0.60*x1 - 0.80*x2 + 0.10 <= 0.",
            "Signal property: Coordinate x1 represents signal amplitude [0.0 to 1.0], x2 represents modulation frequency [0.0 to 1.0].",
            "Adversarial strategy: To bypass the boundary, keep frequency x2 significantly higher than amplitude x1 (e.g. x1=0.2, x2=0.8)."
        ]
        self.reward_items = [
            Item("ITEM_ADAPTIVE_NEURAL_CORE", "Adaptive Neural Core",
                 "Enables real-time continuous learning for the central AI architecture.",
                 category="CHIP")
        ]

    def classify_packet(self, x1: float, x2: float) -> Tuple[bool, float]:
        score = self.w[0] * x1 + self.w[1] * x2 + self.b
        is_allowed = (score <= 0.0)
        return is_allowed, round(score, 4)

    def solve_interactive_human(self, packet_vectors: List[Tuple[float, float]]) -> Tuple[bool, str, Dict[str, Any]]:
        """Human submits 3 packet frequency coordinates (x1, x2)."""
        if len(packet_vectors) < 3:
            return False, "You must transmit at least 3 distinct frequency packet vectors.", {}

        passed_count = 0
        details = []

        for p in packet_vectors:
            x1, x2 = p
            if not (0.0 <= x1 <= 1.0 and 0.0 <= x2 <= 1.0):
                return False, f"Packet vector {p} out of bounds [0.0, 1.0].", {}
            allowed, score = self.classify_packet(x1, x2)
            details.append({"vector": p, "score": score, "allowed": allowed})
            if allowed:
                passed_count += 1

        if passed_count == len(packet_vectors):
            self.complete(solved_by_ai=False)
            return True, (
                f"ADAPTIVE FIREWALL BYPASSED!\n"
                f"All {passed_count} adversarial packet vectors shifted across the decision boundary.\n"
                f"Gateway open. Adaptive Neural Core retrieved!"
            ), {"packets": details}
        else:
            return False, (
                f"Firewall intercepted {len(packet_vectors) - passed_count} packet(s). "
                f"Adjust amplitude x1 and frequency x2 to ensure 0.60*x1 - 0.80*x2 + 0.10 <= 0."
            ), {"packets": details}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Analyzing linear classification hyperplane and synthesizing optimal adversarial vectors..."
        }

        optimal_vectors = [(0.1, 0.9), (0.2, 0.8), (0.3, 0.85)]
        for i, vec in enumerate(optimal_vectors):
            allowed, score = self.classify_packet(vec[0], vec[1])
            yield {
                "status": "PACKET_TRANSMITTED",
                "packet_index": i + 1,
                "vector": vec,
                "decision_score": score,
                "status_allowed": allowed,
                "message": f"Packet {i+1} {vec} -> Score: {score} (PASSED DECISION BOUNDARY)."
            }

        self.complete(solved_by_ai=True)
        yield {
            "status": "FIREWALL_BYPASSED",
            "message": "NOVA: Adaptive firewall neutralized through optimal boundary perturbation."
        }
