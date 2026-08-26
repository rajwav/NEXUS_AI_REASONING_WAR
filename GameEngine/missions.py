"""
NEXUS AI REASONING WAR - Mission Manager
Orchestrates mission unlocking, progression state, telemetry recording,
and item rewards across all 10 playable missions.
"""

from typing import Dict, List, Optional, Tuple, Any
from Missions.mission_base import MissionBase, MissionStatus
from Missions.m01_restore_ai_core import Mission01RestoreAICore
from Missions.m02_traitor_scientist import Mission02TraitorScientist
from Missions.m03_quantum_lock import Mission03QuantumLock
from Missions.m04_defeat_training_ai import Mission04DefeatTrainingAI
from Missions.m05_stop_malware import Mission05StopMalware
from Missions.m06_recover_memory import Mission06RecoverMemory
from Missions.m07_ai_ethics_dilemma import Mission07AIEthicsDilemma
from Missions.m08_robot_escape import Mission08RobotEscape
from Missions.m09_adaptive_ai_test import Mission09AdaptiveAITest
from Missions.m10_final_nexus_core import Mission10FinalNexusCore
from .player import Player
from .inventory import Inventory
from .events import EventBus, EventType


class MissionManager:
    """Central mission registry and progression controller."""
    def __init__(self, player: Player, inventory: Inventory, event_bus: EventBus):
        self.player = player
        self.inventory = inventory
        self.event_bus = event_bus
        self.missions: Dict[str, MissionBase] = {}
        self.active_mission_id: Optional[str] = None
        self._init_all_missions()

    def _init_all_missions(self):
        """Instantiates all 10 missions and unlocks the starting mission."""
        m_list = [
            Mission01RestoreAICore(),
            Mission02TraitorScientist(),
            Mission03QuantumLock(),
            Mission04DefeatTrainingAI(),
            Mission05StopMalware(),
            Mission06RecoverMemory(),
            Mission07AIEthicsDilemma(),
            Mission08RobotEscape(),
            Mission09AdaptiveAITest(),
            Mission10FinalNexusCore()
        ]
        for m in m_list:
            self.missions[m.mission_id] = m

        # Unlock Mission 1 by default
        self.missions["M01"].status = MissionStatus.ACTIVE
        self.active_mission_id = "M01"

    def get_mission(self, mission_id: str) -> Optional[MissionBase]:
        return self.missions.get(mission_id)

    def get_active_mission(self) -> Optional[MissionBase]:
        if self.active_mission_id:
            return self.missions.get(self.active_mission_id)
        return None

    def start_mission(self, mission_id: str) -> Tuple[bool, str]:
        if mission_id not in self.missions:
            return False, f"Unknown mission ID: {mission_id}"

        m = self.missions[mission_id]
        if m.status == MissionStatus.COMPLETED:
            return True, f"Mission {m.mission_id}: {m.title} has already been completed."

        if not m.can_start(self.inventory):
            reqs = ", ".join(m.required_items_to_start)
            return False, f"Cannot activate {m.title}. Requires items: [{reqs}]."

        m.activate()
        self.active_mission_id = mission_id
        self.event_bus.publish(EventType.MISSION_STARTED, {
            "mission_id": m.mission_id,
            "title": m.title,
            "concept": m.algorithm_concept
        })
        return True, f"Activated Mission {m.mission_id}: {m.title}!"

    def complete_mission(self, mission_id: str, solved_by_ai: bool = False) -> Tuple[bool, str]:
        if mission_id not in self.missions:
            return False, f"Unknown mission ID: {mission_id}"

        m = self.missions[mission_id]
        m.complete(solved_by_ai=solved_by_ai)

        # Distribute reward items
        rewards_awarded = []
        for r_item in m.reward_items:
            success, msg = self.inventory.add_item(r_item)
            if success:
                rewards_awarded.append(r_item.name)

        # Update player stats
        self.player.stats.record_puzzle_solved(mission_id, solved_by_ai=solved_by_ai)

        # Auto-unlock next sequential mission if available
        m_keys = list(self.missions.keys())
        curr_idx = m_keys.index(mission_id)
        next_m_id = m_keys[curr_idx + 1] if curr_idx + 1 < len(m_keys) else None

        if next_m_id and self.missions[next_m_id].status == MissionStatus.LOCKED:
            self.missions[next_m_id].status = MissionStatus.ACTIVE
            self.active_mission_id = next_m_id

        self.event_bus.publish(EventType.MISSION_COMPLETED, {
            "mission_id": mission_id,
            "title": m.title,
            "solved_by_ai": solved_by_ai,
            "rewards": rewards_awarded
        })

        rew_str = ", ".join(rewards_awarded) if rewards_awarded else "None"
        return True, f"Mission {m.mission_id} Complete! Rewards acquired: [{rew_str}]."

    def list_missions_overview(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": m.mission_id,
                "title": m.title,
                "sector": m.sector_name,
                "concept": m.algorithm_concept,
                "status": m.status.value,
                "solved_by_ai": m.is_solved_by_ai
            }
            for m in self.missions.values()
        ]
