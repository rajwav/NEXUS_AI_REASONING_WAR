"""
NEXUS AI REASONING WAR - Player Entity & Telemetry Tracking
Tracks Dr. Aarav Sharma's spatial coordinates, inventory, health,
and rich telemetry for real-time Machine Learning adaptation.
"""

from typing import Dict, List, Tuple, Optional, Any
import time
from .world import Sector, World, TileType


class PlayerStats:
    """Telemetry and cognitive metrics for ML modeling."""
    def __init__(self):
        self.steps_taken: int = 0
        self.puzzles_attempted: int = 0
        self.puzzles_solved: int = 0
        self.mistakes_count: int = 0
        self.hints_used: int = 0
        self.nova_assists: int = 0
        self.time_spent_seconds: float = 0.0
        self.risk_events: int = 0
        self.start_time: float = time.time()
        self.actions_history: List[Dict[str, Any]] = []

    def record_step(self):
        self.steps_taken += 1

    def record_mistake(self, reason: str = ""):
        self.mistakes_count += 1
        self.actions_history.append({
            "timestamp": time.time() - self.start_time,
            "type": "mistake",
            "reason": reason
        })

    def record_hint(self, hint_level: int = 1):
        self.hints_used += hint_level
        self.actions_history.append({
            "timestamp": time.time() - self.start_time,
            "type": "hint",
            "level": hint_level
        })

    def record_puzzle_solved(self, puzzle_id: str, solved_by_ai: bool = False):
        self.puzzles_attempted += 1
        self.puzzles_solved += 1
        if solved_by_ai:
            self.nova_assists += 1
        self.actions_history.append({
            "timestamp": time.time() - self.start_time,
            "type": "puzzle_solved",
            "puzzle_id": puzzle_id,
            "solved_by_ai": solved_by_ai
        })

    def get_telemetry_vector(self) -> List[float]:
        """
        Returns normalized feature vector for ML clustering and predictors:
        [Speed/Steps, Mistake Rate, Hint Dependency, Risk Score, Autonomy Ratio]
        """
        total_time = max(1.0, time.time() - self.start_time)
        velocity = min(1.0, self.steps_taken / max(10.0, total_time))
        error_rate = min(1.0, self.mistakes_count / max(1, self.puzzles_attempted + self.mistakes_count))
        hint_dep = min(1.0, self.hints_used / max(1, self.puzzles_attempted * 2 + 1))
        risk_index = min(1.0, self.risk_events / 10.0)
        autonomy = 1.0 - min(1.0, self.nova_assists / max(1, self.puzzles_solved + 1))

        return [velocity, error_rate, hint_dep, risk_index, autonomy]


class Player:
    """The player character (Dr. Aarav Sharma, Lead AI Engineer)."""
    def __init__(self, name: str = "Dr. Aarav Sharma", start_sector: Sector = Sector.AI_CORE_GARDEN, start_pos: Tuple[int, int] = (3, 7)):
        self.name = name
        self.current_sector = start_sector
        self.x, self.y = start_pos
        self.facing: str = "SOUTH"  # NORTH, SOUTH, EAST, WEST
        self.health: int = 100
        self.max_health: int = 100
        self.energy: int = 100
        self.stats = PlayerStats()
        self.is_nova_companion_active: bool = True
        self.selected_inventory_index: int = 0

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def move(self, dx: int, dy: int, world: World) -> Tuple[bool, str]:
        """Attempts to move player in direction (dx, dy)."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Update facing direction
        if dx > 0:
            self.facing = "EAST"
        elif dx < 0:
            self.facing = "WEST"
        elif dy > 0:
            self.facing = "SOUTH"
        elif dy < 0:
            self.facing = "NORTH"

        curr_map = world.get_current_map()

        # Check walkability
        if not curr_map.is_walkable(new_x, new_y):
            tile = curr_map.get_tile(new_x, new_y)
            if tile == TileType.DOOR_LOCKED:
                portal = world.get_portal_at(self.current_sector, (new_x, new_y))
                key = portal.required_keycard if portal else "Security Keycard"
                return False, f"Door is locked! Requires: {key}"
            elif tile == TileType.LASER_BARRIER:
                self.health = max(0, self.health - 15)
                self.stats.risk_events += 1
                self.stats.record_mistake("Triggered high-voltage laser barrier")
                return False, f"WARNING: Active laser barrier caused 15 damage! [HP: {self.health}]"
            elif tile == TileType.VAULT_GATE:
                return False, "Quantum Vault Gate is locked by 5-variable CSP frequency resonance."
            return False, "Obstacle blocked path."

        # Check hazard tiles
        if curr_map.get_tile(new_x, new_y) == TileType.HAZARD:
            self.health = max(0, self.health - 10)
            self.stats.risk_events += 1
            self.stats.record_mistake("Walked through exposed cooling hazard")

        # Apply movement
        self.x = new_x
        self.y = new_y
        self.stats.record_step()

        # Check portal transition
        portal = world.get_portal_at(self.current_sector, (self.x, self.y))
        if portal and portal.is_unlocked:
            self.current_sector = portal.to_sector
            world.current_sector = portal.to_sector
            self.x, self.y = portal.to_pos
            return True, f"Sector Transition -> {portal.to_sector.value} via {portal.description}"

        return True, "Moved successfully."

    def check_interaction_target(self, world: World) -> Optional[Tuple[Tuple[int, int], str]]:
        """Returns coordinate and object_id of any interactable object in front of or adjacent to player."""
        curr_map = world.get_current_map()

        # Check tile directly in front
        offsets = {
            "NORTH": (0, -1),
            "SOUTH": (0, 1),
            "EAST": (1, 0),
            "WEST": (-1, 0)
        }
        dx, dy = offsets.get(self.facing, (0, 0))
        target_pos = (self.x + dx, self.y + dy)
        if target_pos in curr_map.interactable_positions:
            return (target_pos, curr_map.interactable_positions[target_pos])

        # Check all adjacent 4 tiles if facing tile has no object
        for adx, ady in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:
            pos = (self.x + adx, self.y + ady)
            if pos in curr_map.interactable_positions:
                return (pos, curr_map.interactable_positions[pos])

        return None
