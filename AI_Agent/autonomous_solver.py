"""
NEXUS AI REASONING WAR - Autonomous AI Solver
Enables NOVA to take physical control of the avatar, navigate sectors,
interact with machinery, and execute verified algorithms with live step-by-step telemetry.
"""

from typing import Dict, List, Tuple, Optional, Any, Generator
import time
from GameEngine.world import World, Sector
from GameEngine.player import Player
from GameEngine.missions import MissionManager, MissionBase
from AI_Algorithms.astar import AStarSearch


class AutonomousSolver:
    """Controls physical avatar and executes live algorithm solutions."""
    def __init__(self, world: World, player: Player, mission_manager: MissionManager):
        self.world = world
        self.player = player
        self.mission_manager = mission_manager
        self.is_solving = False

    def solve_active_mission(self) -> Generator[Dict[str, Any], None, None]:
        """
        Executes complete autonomous solving cycle for the active mission.
        Yields step-by-step animation states for the UI.
        """
        active_mission = self.mission_manager.get_active_mission()
        if not active_mission:
            yield {"status": "ERROR", "message": "No active mission to solve."}
            return

        self.is_solving = True

        yield {
            "status": "AUTONOMOUS_START",
            "mission_id": active_mission.mission_id,
            "title": active_mission.title,
            "algorithm": active_mission.algorithm_concept,
            "message": f"NOVA taking control: Commencing autonomous solution of {active_mission.title}..."
        }

        # Step 1: Execute algorithm step generator
        for step in active_mission.solve_autonomous_ai():
            yield {
                "type": "ALGORITHM_STEP",
                "mission_id": active_mission.mission_id,
                "step_data": step,
                "message": step.get("message", "Processing algorithm step...")
            }

        # Step 2: Complete mission in manager and collect reward items
        success, msg = self.mission_manager.complete_mission(active_mission.mission_id, solved_by_ai=True)

        yield {
            "status": "AUTONOMOUS_COMPLETE",
            "mission_id": active_mission.mission_id,
            "success": success,
            "message": f"NOVA Solution Finished: {msg}"
        }

        self.is_solving = False
