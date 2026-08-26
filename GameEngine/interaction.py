"""
NEXUS AI REASONING WAR - Contextual Interaction Engine
Handles proximity detection, item utilization, hacking attempts,
and dispatching puzzle requests to the appropriate solver.
"""

from typing import Dict, List, Tuple, Optional, Any, Callable
from .world import World, Sector, TileType
from .player import Player
from .inventory import Inventory
from .objects import GameObject, Terminal, InteractiveObject, ObjectState, Item
from .events import EventBus, EventType


class InteractionHandler:
    """Manages player interactions with world objects, items, and AI solving modes."""
    def __init__(self, world: World, player: Player, inventory: Inventory, event_bus: EventBus):
        self.world = world
        self.player = player
        self.inventory = inventory
        self.event_bus = event_bus
        self.registered_objects: Dict[str, GameObject] = {}
        self.puzzle_dispatch_table: Dict[str, Callable[..., Any]] = {}

    def register_object(self, obj: GameObject):
        self.registered_objects[obj.object_id] = obj

    def register_puzzle_handler(self, puzzle_id: str, handler: Callable[..., Any]):
        self.puzzle_dispatch_table[puzzle_id] = handler

    def get_nearby_interactive_object(self) -> Optional[Tuple[Tuple[int, int], GameObject]]:
        target_info = self.player.check_interaction_target(self.world)
        if not target_info:
            return None
        pos, obj_id = target_info
        if obj_id in self.registered_objects:
            return (pos, self.registered_objects[obj_id])
        return None

    def handle_inspect(self) -> Tuple[bool, str]:
        target = self.get_nearby_interactive_object()
        if not target:
            return False, "Nothing in close proximity to inspect."
        pos, obj = target
        info = obj.inspect()
        self.event_bus.publish(EventType.OBJECT_INSPECTED, {
            "object_id": obj.object_id,
            "position": pos,
            "sector": self.player.current_sector.value
        })
        return True, info

    def handle_interact(self) -> Tuple[bool, str, Optional[str]]:
        """
        Returns (success, message, optional_puzzle_id_to_open)
        """
        target = self.get_nearby_interactive_object()
        if not target:
            return False, "No machine, console, or object in range to interact with.", None

        pos, obj = target

        if isinstance(obj, Terminal) and obj.puzzle_id:
            self.event_bus.publish(EventType.TERMINAL_ACCESSED, {
                "terminal_id": obj.object_id,
                "puzzle_id": obj.puzzle_id
            })
            return True, f"Connecting to terminal [{obj.name}]...", obj.puzzle_id

        success, msg = obj.interact(self.inventory)
        return success, msg, None

    def handle_use_item(self, item_index: int) -> Tuple[bool, str]:
        if item_index < 0 or item_index >= len(self.inventory.items):
            return False, "Invalid inventory slot."

        item = self.inventory.items[item_index]
        target = self.get_nearby_interactive_object()

        if not target:
            return False, f"No target nearby to use [{item.name}] on."

        pos, obj = target

        if item.target_object_id and item.target_object_id != obj.object_id:
            self.player.stats.record_mistake(f"Used {item.name} on incorrect target {obj.name}")
            return False, f"[{item.name}] is incompatible with [{obj.name}]."

        # Use item effect
        self.event_bus.publish(EventType.ITEM_USED, {
            "item_id": item.item_id,
            "target_id": obj.object_id
        })
        return True, f"Applied [{item.name}] to [{obj.name}]."

    def handle_hack(self) -> Tuple[bool, str, Optional[str]]:
        target = self.get_nearby_interactive_object()
        if not target:
            return False, "No hackable terminal or interface within range.", None

        pos, obj = target
        if not isinstance(obj, Terminal):
            return False, f"[{obj.name}] is a physical mechanism, not a digital terminal.", None

        if obj.puzzle_id:
            return True, f"Initiating cyber intrusion into [{obj.name}]...", obj.puzzle_id

        return True, f"Injected diagnostic probe into [{obj.name}]. System logs extracted.", None
