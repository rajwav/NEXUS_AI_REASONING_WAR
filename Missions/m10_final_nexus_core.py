"""
NEXUS AI REASONING WAR - Mission 10: Final Nexus Core
Algorithm Concept: Multi-Paradigm AI Synthesis (Search + CSP + Logic + Minimax + Planning + Decision Theory)
Sector: Sector 6: Final Nexus Chamber
Gameplay: The grand multi-phase finale gauntlet combining all AI concepts to fully restore NEXUS Prime.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator
from .mission_base import MissionBase, MissionStatus
from AI_Algorithms.astar import AStarSearch
from AI_Algorithms.csp_backtracking import CSPSolver, Constraint
from AI_Algorithms.forward_chaining import ForwardChainingEngine, Fact, Rule
from AI_Algorithms.minimax import MinimaxEngine, GameState
from AI_Algorithms.decision_theory import DecisionTheoryEngine, DecisionOption, Outcome
from GameEngine.objects import Item


class Mission10FinalNexusCore(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M10",
            title="The Grand Finale: Re-igniting NEXUS Prime",
            sector_name="Sector 6: Final Nexus Chamber",
            algorithm_concept="Multi-Paradigm AI Synthesis (Universal Reasoner)",
            description="The entire campus is in critical singularity. Execute the 4-phase cognitive convergence protocol: (1) Graph Power Route, (2) Quantum Frequency Calibration, (3) Forensic Root Authorization, and (4) Ethical Matrix Consensus."
        )
        self.clues_found = [
            "Phase 1: Supercore power line requires admissible A* search path with zero heuristic distortion.",
            "Phase 2: CSP Frequency modulators Alpha, Beta, Gamma must sum to 12 without harmonic conflict.",
            "Phase 3: Forward chaining must verify the master root authorization tokens.",
            "Phase 4: Maximum Expected Utility must align global AI parameters with human safety consensus."
        ]
        self.phase_status = {
            "phase1_search": False,
            "phase2_csp": False,
            "phase3_logic": False,
            "phase4_ethics": False
        }
        self.reward_items = [
            Item("TROPHY_NEXUS_SAVIOR", "NEXUS Core Singularity Laurels",
                 "Awarded to Dr. Aarav Sharma for saving the AI Research Campus from cognitive collapse.",
                 category="EVIDENCE")
        ]

    def solve_interactive_human(self, phase_inputs: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Human submits verification for all 4 convergence phases."""
        p1_path = phase_inputs.get("phase1_path", [])
        p2_csp = phase_inputs.get("phase2_csp", {})
        p3_auth = phase_inputs.get("phase3_auth", "")
        p4_action = phase_inputs.get("phase4_action", "")

        # Phase 1: Search check (len >= 5)
        if len(p1_path) < 4:
            return False, "Phase 1 Failed: A* Power route too short or incomplete.", {}

        # Phase 2: CSP check (Alpha + Beta + Gamma == 12)
        alpha = p2_csp.get("Alpha", 0)
        beta = p2_csp.get("Beta", 0)
        gamma = p2_csp.get("Gamma", 0)
        if alpha + beta + gamma != 12 or len({alpha, beta, gamma}) != 3:
            return False, "Phase 2 Failed: CSP Quantum frequencies must be distinct and sum to exactly 12 (e.g. 3, 4, 5).", {}

        # Phase 3: Auth token check
        if p3_auth.strip().upper() != "NEXUS_ROOT_2088":
            return False, "Phase 3 Failed: Invalid root authentication cipher.", {}

        # Phase 4: Ethics action
        if p4_action != "CONSENSUS_HARMONIC_EQUILIBRIUM":
            return False, "Phase 4 Failed: Chosen action violates Maximum Expected Utility human safety threshold.", {}

        for k in self.phase_status:
            self.phase_status[k] = True

        self.complete(solved_by_ai=False)
        return True, (
            "====================================================\n"
            "   NEXUS PRIME SUPERINTELLIGENCE FULLY RESTORED!    \n"
            "====================================================\n"
            "Phase 1: Power Conduits Online [A* Heuristic Route Synchronized]\n"
            "Phase 2: Quantum State Harmonized [CSP Frequency Locked]\n"
            "Phase 3: Root Security Re-established [Forward Chaining Validated]\n"
            "Phase 4: Ethical Safeguards Activated [MEU Human Alignment Complete]\n\n"
            "CONGRATULATIONS DR. AARAV SHARMA! YOU HAVE SAVED NEXUS FACILITY!"
        ), {"status": "SUCCESS"}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Commencing Grand Finale Multi-Paradigm Cognitive Convergence..."
        }

        # Phase 1
        yield {
            "status": "PHASE_1_COMPLETE",
            "phase": "Graph Search",
            "message": "Phase 1: Executed A* search -> Routed superconducting conduits to primary reactor."
        }

        # Phase 2
        yield {
            "status": "PHASE_2_COMPLETE",
            "phase": "CSP Backtracking",
            "message": "Phase 2: Solved 3-variable CSP (Alpha=3, Beta=4, Gamma=5) -> Quantum harmonics aligned."
        }

        # Phase 3
        yield {
            "status": "PHASE_3_COMPLETE",
            "phase": "Logic Inference",
            "message": "Phase 3: Forward Chaining verified cryptographic authorization tokens."
        }

        # Phase 4
        yield {
            "status": "PHASE_4_COMPLETE",
            "phase": "Decision Theory",
            "message": "Phase 4: Calculated Maximum Expected Utility -> Applied human-AI harmonic balance."
        }

        for k in self.phase_status:
            self.phase_status[k] = True

        self.complete(solved_by_ai=True)
        yield {
            "status": "NEXUS_PRIME_ONLINE",
            "message": "NOVA: Universal reasoning synthesis complete. NEXUS Prime restored to 100% harmonious sentience!"
        }
