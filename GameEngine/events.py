"""
NEXUS AI REASONING WAR - Event System
Pub/Sub event dispatcher for world triggers, alarms, mission completions, and telemetry events.
"""

from enum import Enum
from typing import Dict, List, Callable, Any
import time


class EventType(Enum):
    PLAYER_MOVED = "PLAYER_MOVED"
    OBJECT_INSPECTED = "OBJECT_INSPECTED"
    TERMINAL_ACCESSED = "TERMINAL_ACCESSED"
    ITEM_ACQUIRED = "ITEM_ACQUIRED"
    ITEM_USED = "ITEM_USED"
    PUZZLE_ATTEMPT = "PUZZLE_ATTEMPT"
    PUZZLE_SOLVED = "PUZZLE_SOLVED"
    PUZZLE_FAILED = "PUZZLE_FAILED"
    NOVA_SOLVE_START = "NOVA_SOLVE_START"
    NOVA_STEP = "NOVA_STEP"
    NOVA_SOLVE_COMPLETE = "NOVA_SOLVE_COMPLETE"
    SECTOR_CHANGED = "SECTOR_CHANGED"
    DOOR_UNLOCKED = "DOOR_UNLOCKED"
    MISSION_STARTED = "MISSION_STARTED"
    MISSION_COMPLETED = "MISSION_COMPLETED"
    ML_DIFFICULTY_ADAPTED = "ML_DIFFICULTY_ADAPTED"


class Event:
    def __init__(self, event_type: EventType, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = time.time()


class EventBus:
    """Central event broker for decoupled game communication."""
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable[[Event], None]]] = {
            et: [] for et in EventType
        }
        self.event_log: List[Event] = []

    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def publish(self, event_type: EventType, data: Dict[str, Any]):
        event = Event(event_type, data)
        self.event_log.append(event)
        for callback in self._listeners.get(event_type, []):
            try:
                callback(event)
            except Exception as e:
                print(f"[EventBus Error] Callback for {event_type.value} failed: {e}")
