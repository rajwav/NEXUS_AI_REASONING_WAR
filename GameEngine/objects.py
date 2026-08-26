"""
NEXUS AI REASONING WAR - Interactive Objects & Machinery
Provides interactive world objects: Terminals, Circuit Boards, Lasers,
Servers, Quantum Locks, and Power Nodes.
"""

from typing import Dict, List, Tuple, Optional, Any, Callable
from enum import Enum


class ObjectState(Enum):
    LOCKED = "LOCKED"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    RESOLVED = "RESOLVED"
    ERROR = "ERROR"


class Item:
    """An inventory item with description, usage effect, and combination recipe."""
    def __init__(self, item_id: str, name: str, description: str, category: str = "TOOL",
                 usable: bool = True, target_object_id: Optional[str] = None):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.category = category  # TOOL, KEYCARD, EVIDENCE, CHIP, PRISM
        self.usable = usable
        self.target_object_id = target_object_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "usable": self.usable,
            "target_object_id": self.target_object_id
        }


class GameObject:
    """Base class for all interactive physical objects in the world."""
    def __init__(self, object_id: str, name: str, description: str,
                 position: Tuple[int, int], sector_name: str,
                 state: ObjectState = ObjectState.ACTIVE):
        self.object_id = object_id
        self.name = name
        self.description = description
        self.position = position
        self.sector_name = sector_name
        self.state = state
        self.required_item_id: Optional[str] = None
        self.inspection_count: int = 0
        self.associated_mission_id: Optional[str] = None

    def inspect(self) -> str:
        self.inspection_count += 1
        return f"[{self.name}] ({self.state.value})\n{self.description}"

    def interact(self, player_inventory: Any) -> Tuple[bool, str]:
        """Default interaction handler."""
        return True, f"Interacted with {self.name}."


class Terminal(GameObject):
    """An interactive computer console running specific AI diagnostics or puzzle interfaces."""
    def __init__(self, object_id: str, name: str, description: str,
                 position: Tuple[int, int], sector_name: str,
                 terminal_os: str = "NEXUS_OS_v4.88",
                 puzzle_id: Optional[str] = None):
        super().__init__(object_id, name, description, position, sector_name)
        self.terminal_os = terminal_os
        self.puzzle_id = puzzle_id
        self.logs: List[str] = []
        self.is_hacked: bool = False

    def add_log(self, text: str):
        self.logs.append(text)

    def interact(self, player_inventory: Any) -> Tuple[bool, str]:
        self.inspection_count += 1
        if self.state == ObjectState.RESOLVED:
            return True, f"{self.name} has already been calibrated and online."
        return True, f"Accessed {self.name}. Running {self.terminal_os}."


class Door(GameObject):
    """A physical security door / airlock."""
    def __init__(self, object_id: str, name: str, position: Tuple[int, int],
                 sector_name: str, required_keycard: Optional[str] = None):
        state = ObjectState.ACTIVE if required_keycard is None else ObjectState.LOCKED
        super().__init__(object_id, name, "Security airlock door.", position, sector_name, state)
        self.required_keycard = required_keycard

    def unlock(self):
        self.state = ObjectState.ACTIVE


class InteractiveObject(GameObject):
    """Custom interactive machinery (AI Core, Laser Grid, Forensic Deck, Quantum Lock)."""
    def __init__(self, object_id: str, name: str, description: str,
                 position: Tuple[int, int], sector_name: str,
                 on_interact: Optional[Callable[..., Tuple[bool, str]]] = None):
        super().__init__(object_id, name, description, position, sector_name)
        self.custom_interact = on_interact

    def interact(self, player_inventory: Any) -> Tuple[bool, str]:
        if self.custom_interact:
            return self.custom_interact(self, player_inventory)
        return super().interact(player_inventory)
