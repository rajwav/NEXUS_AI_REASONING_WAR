# GameEngine Package Init
"""
NEXUS AI REASONING WAR - Game Engine
Core systems for world simulation, entity management, inventory, missions, and interactions.
"""

from .world import World, TileType, Sector
from .player import Player, PlayerStats
from .objects import GameObject, Terminal, InteractiveObject, Item, Door
from .inventory import Inventory
from .missions import MissionManager, MissionStatus
from .events import EventBus, Event, EventType
from .interaction import InteractionHandler

__all__ = [
    "World",
    "TileType",
    "Sector",
    "Player",
    "PlayerStats",
    "GameObject",
    "Terminal",
    "InteractiveObject",
    "Item",
    "Door",
    "Inventory",
    "MissionManager",
    "MissionStatus",
    "EventBus",
    "Event",
    "EventType",
    "InteractionHandler",
]
