"""
NEXUS AI REASONING WAR - Mission 3: Break Quantum Lock
Algorithm Concept: Constraint Satisfaction Problem (CSP) & Backtracking with Forward Checking
Sector: Quantum Security Lab
Gameplay: Calibrate laser frequencies across 5 emitter nodes without destructive harmonic interference.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator
from .mission_base import MissionBase, MissionStatus
from AI_Algorithms.csp_backtracking import CSPSolver, Variable, Constraint
from GameEngine.objects import Item


class Mission03QuantumLock(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M03",
            title="Quantum Security Vault Laser Calibration",
            sector_name="Sector 3: Quantum Security Lab",
            algorithm_concept="CSP Backtracking with Forward Checking & MRV",
            description="The Quantum Vault is locked by 5 laser modulators (A, B, C, D, E). Tune each emitter to a distinct frequency band (1=Red, 2=Green, 3=Blue, 4=Violet) satisfying non-interference constraints."
        )
        self.variables = {
            "Emitter_A": [1, 2, 3, 4],
            "Emitter_B": [1, 2, 3, 4],
            "Emitter_C": [1, 2, 3, 4],
            "Emitter_D": [1, 2, 3, 4],
            "Emitter_E": [1, 2, 3, 4]
        }
        self.constraints = [
            Constraint(["Emitter_A", "Emitter_B"], lambda a: a["Emitter_A"] != a["Emitter_B"], "A != B (Adjacent laser interference)"),
            Constraint(["Emitter_B", "Emitter_C"], lambda a: a["Emitter_B"] != a["Emitter_C"], "B != C (Adjacent laser interference)"),
            Constraint(["Emitter_C", "Emitter_D"], lambda a: a["Emitter_C"] != a["Emitter_D"], "C != D (Adjacent laser interference)"),
            Constraint(["Emitter_D", "Emitter_E"], lambda a: a["Emitter_D"] != a["Emitter_E"], "D != E (Adjacent laser interference)"),
            Constraint(["Emitter_B", "Emitter_D"], lambda a: a["Emitter_B"] != a["Emitter_D"], "B != D (Cross-refraction interference)"),
            Constraint(["Emitter_A", "Emitter_C"], lambda a: a["Emitter_A"] + a["Emitter_C"] == 5, "A + C == 5 (Harmonic resonance)"),
            Constraint(["Emitter_E", "Emitter_A"], lambda a: a["Emitter_E"] > a["Emitter_A"], "E > A (Gradient step constraint)")
        ]
        self.clues_found = [
            "Laser notes: Emitters A and C must sum to exactly 5 for harmonic resonance.",
            "Optical sensor: Emitter E must operate at a higher frequency band than Emitter A.",
            "Cross-channel check: Emitter B and Emitter D refract into the same cavity and must not share a frequency."
        ]
        self.reward_items = [
            Item("ITEM_CRYO_CRYSTAL", "Superconducting Cryo-Crystal",
                 "Pure zero-resistance crystal required to build superconducting logic probes.",
                 category="TOOL"),
            Item("ITEM_OPTICAL_PRISM", "Quantum Harmonic Prism",
                 "High-refraction optic component used to calibrate advanced neural lasers.",
                 category="PRISM")
        ]

    def solve_interactive_human(self, assignment: Dict[str, int]) -> Tuple[bool, str, Dict[str, Any]]:
        """Human submits a proposed 5-variable frequency assignment."""
        if len(assignment) != len(self.variables):
            return False, f"Incomplete assignment. You must assign all 5 emitters (A, B, C, D, E).", {}

        for var, val in assignment.items():
            if var not in self.variables or val not in self.variables[var]:
                return False, f"Invalid value {val} for {var}. Allowed: {self.variables.get(var)}", {}

        # Validate all constraints
        for c in self.constraints:
            if not c.is_satisfied(assignment):
                return False, f"Constraint Violation: {c.description}. Frequencies create destructive laser feedback!", {}

        self.complete(solved_by_ai=False)
        return True, (
            "QUANTUM LOCK DEFEATED!\n"
            f"Harmonic Frequencies Locked: {assignment}\n"
            "Laser barriers powered down. Superconducting Cryo-Crystal and Optical Prism retrieved!"
        ), {"solution": assignment}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        """NOVA executes CSP backtracking search with MRV and Forward Checking."""
        solver = CSPSolver(self.variables, self.constraints)

        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Formulating Quantum Lock as Constraint Satisfaction Problem (CSP)..."
        }

        for step in solver.solve_stepper():
            yield step

        self.complete(solved_by_ai=True)
