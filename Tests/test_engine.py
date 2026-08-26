"""
Unit Tests - NEXUS Game Engine
Tests World grid generation, Player movement, Portals, Inventory, and Events.
"""

import unittest
from GameEngine.world import World, Sector, TileType
from GameEngine.player import Player
from GameEngine.inventory import Inventory
from GameEngine.objects import Item, Terminal, ObjectState
from GameEngine.events import EventBus, EventType


class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.player = Player(start_sector=Sector.AI_CORE_GARDEN, start_pos=(2, 2))
        self.inventory = Inventory(capacity=5)
        self.event_bus = EventBus()

    def test_world_sectors_initialized(self):
        self.assertEqual(len(self.world.sectors), 6)
        s_map = self.world.get_current_map()
        self.assertEqual(s_map.sector, Sector.AI_CORE_GARDEN)
        # Check boundary wall
        self.assertEqual(s_map.get_tile(0, 0), TileType.WALL)

    def test_player_movement_and_bounds(self):
        # Move East
        success, msg = self.player.move(1, 0, self.world)
        self.assertTrue(success)
        self.assertEqual(self.player.x, 3)
        self.assertEqual(self.player.y, 2)
        self.assertEqual(self.player.stats.steps_taken, 1)

        # Move into wall at x=0
        self.player.x = 1
        self.player.y = 1
        success, msg = self.player.move(-1, 0, self.world)
        self.assertFalse(success)
        self.assertEqual(self.player.x, 1)  # blocked

    def test_inventory_management_and_crafting(self):
        p1 = Item("ITEM_LOGIC_PROBE", "Standard Logic Probe", "Test tool", category="TOOL")
        c1 = Item("ITEM_CRYO_CRYSTAL", "Cryo-Crystal", "Raw crystal", category="TOOL")

        self.inventory.add_item(p1)
        self.inventory.add_item(c1)
        self.assertEqual(len(self.inventory.items), 2)

        # Test Crafting/Combination
        success, msg, result = self.inventory.combine_items("ITEM_LOGIC_PROBE", "ITEM_CRYO_CRYSTAL")
        self.assertTrue(success)
        self.assertIsNotNone(result)
        self.assertEqual(result.item_id, "ITEM_SUPERCONDUCTING_PROBE")
        self.assertEqual(len(self.inventory.items), 1)

    def test_event_bus(self):
        received = []
        def handler(event):
            received.append(event.data)

        self.event_bus.subscribe(EventType.PLAYER_MOVED, handler)
        self.event_bus.publish(EventType.PLAYER_MOVED, {"pos": (3, 3)})
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["pos"], (3, 3))


if __name__ == "__main__":
    unittest.main()
