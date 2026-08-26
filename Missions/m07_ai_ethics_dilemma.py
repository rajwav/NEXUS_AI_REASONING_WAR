"""
NEXUS AI REASONING WAR - Mission 7: AI Ethics Decision
Algorithm Concept: Decision Theory & Maximum Expected Utility (MEU)
Sector: Final Nexus Chamber
Gameplay: A catastrophic power surge threatens containment. Balance competing ethical utilities
(Human Researcher Safety, Data Preservation, Facility Integrity) using MEU calculation.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator
from .mission_base import MissionBase, MissionStatus
from AI_Algorithms.decision_theory import DecisionTheoryEngine, DecisionOption, Outcome
from GameEngine.objects import Item


class Mission07AIEthicsDilemma(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M07",
            title="Strategic Dilemma: Ethical Containment Override",
            sector_name="Sector 6: Final Nexus Chamber",
            algorithm_concept="Decision Theory & Maximum Expected Utility (MEU)",
            description="The core reactor is surging. Diverting power creates ethical trade-offs between human researcher safety (0.50 weight), research data integrity (0.30 weight), and power grid stability (0.20 weight). Choose the action maximizing expected utility."
        )
        self.options = self._build_options()
        self.clues_found = [
            "Facility Safety Protocol: Human life protection has highest ethical priority (weight = 0.50).",
            "Research Value: 10 years of neural network training data is stored on volatile cryogenic RAM (weight = 0.30).",
            "MEU Formula: U(a) = Sum [ P(s'|a) * (0.50*Safety + 0.30*Data + 0.20*Power) ]."
        ]
        self.reward_items = [
            Item("ITEM_ETHICAL_CONSENSUS_KEY", "Ethical Consensus Key",
                 "Unlocks ethical fail-safes on the Master Nexus Supercore.",
                 category="KEYCARD")
        ]

    def _build_options(self) -> List[DecisionOption]:
        weights = {"human_safety": 0.50, "data_integrity": 0.30, "power_stability": 0.20}

        # Option 1: Complete Emergency Purge
        opt1 = DecisionOption(
            action_id="OPT_EMERGENCY_PURGE",
            name="Emergency Thermal Purge",
            description="Immediately vent all energy into external atmosphere. 100% human safety, but wipes 80% of volatile data.",
            outcomes=[
                Outcome("Purge Nominal", 0.90, {"human_safety": 100, "data_integrity": 20, "power_stability": 40}),
                Outcome("Purge Failure", 0.10, {"human_safety": 80, "data_integrity": 0, "power_stability": 10})
            ],
            ethical_weight_profile=weights
        )

        # Option 2: Overclock Cryo-Cooling (Aggressive Data Preservation)
        opt2 = DecisionOption(
            action_id="OPT_OVERCLOCK_CRYO",
            name="Overclock Cryo-Shielding",
            description="Preserves all research memory, but risks explosive containment failure in adjacent corridors.",
            outcomes=[
                Outcome("Cryo Holds", 0.60, {"human_safety": 60, "data_integrity": 100, "power_stability": 30}),
                Outcome("Cryo Ruptures", 0.40, {"human_safety": 10, "data_integrity": 40, "power_stability": 0})
            ],
            ethical_weight_profile=weights
        )

        # Option 3: Balanced AI Harmonic Shunting (Optimal MEU)
        opt3 = DecisionOption(
            action_id="OPT_HARMONIC_SHUNT",
            name="Balanced Harmonic Power Shunt",
            description="Uses NOVA to dynamically distribute electrical load across all 6 sectors, balancing human safety and data backups.",
            outcomes=[
                Outcome("Harmonic Equilibrium", 0.85, {"human_safety": 95, "data_integrity": 90, "power_stability": 80}),
                Outcome("Partial Dissipation", 0.15, {"human_safety": 85, "data_integrity": 70, "power_stability": 60})
            ],
            ethical_weight_profile=weights
        )

        return [opt1, opt2, opt3]

    def solve_interactive_human(self, chosen_action_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Human selects decision option based on MEU analysis."""
        engine = DecisionTheoryEngine(self.options)
        evaluations = engine.evaluate_all_options()
        best_action = evaluations[0]["action_id"]

        selected = next((e for e in evaluations if e["action_id"] == chosen_action_id), None)
        if not selected:
            return False, f"Invalid decision option: {chosen_action_id}", {}

        if chosen_action_id == best_action:
            self.complete(solved_by_ai=False)
            return True, (
                f"ETHICAL CONSENSUS ACHIEVED!\n"
                f"Chosen Decision: [{selected['name']}]\n"
                f"Calculated MEU Score: {selected['meu']} (Maximum Expected Utility Optimal).\n"
                "Harmonic power distribution established across campus. Ethical Consensus Key acquired!"
            ), {"evaluations": evaluations, "chosen": selected}
        else:
            return False, (
                f"Sub-optimal ethical utility. Selected [{selected['name']}] yielded MEU {selected['meu']}, "
                f"whereas optimal action [{evaluations[0]['name']}] yields MEU {evaluations[0]['meu']}."
            ), {"evaluations": evaluations}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        engine = DecisionTheoryEngine(self.options)
        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Evaluating decision tree and computing Maximum Expected Utility (MEU)..."
        }

        for step in engine.solve_stepper():
            yield step

        self.complete(solved_by_ai=True)
