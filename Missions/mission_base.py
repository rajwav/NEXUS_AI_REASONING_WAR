"""
NEXUS AI REASONING WAR - Base Mission Framework
Each mission provides:
- Layer 1: Observation (Clues & environmental inspection)
- Layer 2: Logical Reasoning (Connecting clues & hypotheses)
- Layer 3: AI Algorithm Solution (Human play vs NOVA Autonomous AI solve)
- Layer 4: Decision Consequence (World state changes, unlocks, item rewards)
"""

from typing import Dict, List, Tuple, Optional, Any, Generator
from enum import Enum


class MissionStatus(Enum):
    LOCKED = "LOCKED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class MissionBase:
    """Abstract base class for all 10 story and algorithm missions."""
    def __init__(self, mission_id: str, title: str, sector_name: str,
                 algorithm_concept: str, description: str):
        self.mission_id = mission_id
        self.title = title
        self.sector_name = sector_name
        self.algorithm_concept = algorithm_concept
        self.description = description
        self.status = MissionStatus.LOCKED
        self.clues_found: List[str] = []
        self.required_items_to_start: List[str] = []
        self.reward_items: List[Any] = []
        self.is_solved_by_ai: bool = False
        self.execution_log: List[str] = []

    def can_start(self, player_inventory: Any) -> bool:
        for item_id in self.required_items_to_start:
            if not player_inventory.has_item(item_id):
                return False
        return True

    def activate(self):
        self.status = MissionStatus.ACTIVE
        self.execution_log.append(f"Mission activated: {self.title}")

    def complete(self, solved_by_ai: bool = False):
        self.status = MissionStatus.COMPLETED
        self.is_solved_by_ai = solved_by_ai
        self.execution_log.append(f"Mission completed ({'AI NOVA' if solved_by_ai else 'Human'})")

    def get_clue_summary(self) -> str:
        if not self.clues_found:
            return "No environmental clues gathered yet. Inspect machinery and logs in the sector."
        return "\n".join([f"• {c}" for c in self.clues_found])

    def solve_interactive_human(self, *args, **kwargs) -> Tuple[bool, str, Any]:
        """Human player solving interface."""
        raise NotImplementedError

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        """NOVA AI step-by-step visual autonomous solver generator."""
        raise NotImplementedError
