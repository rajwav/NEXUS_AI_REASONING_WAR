"""
NEXUS AI REASONING WAR - World & Sector Simulation
Provides 2D spatial representation of the NEXUS Advanced AI Research Facility,
supporting tile grids, dynamic doors, hazards, and interconnected sectors.
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
import random


class TileType(Enum):
    EMPTY = " "
    FLOOR = "."
    WALL = "#"
    DOOR_LOCKED = "D"
    DOOR_UNLOCKED = "O"
    HAZARD = "^"
    TERMINAL = "T"
    POWER_NODE = "P"
    AI_CORE = "C"
    SERVER_RACK = "S"
    LASER_BARRIER = "L"
    VAULT_GATE = "V"
    TELEPORTER = "@"
    MAINTENANCE_TUNNEL = "~"
    CONDUIT = "="


class Sector(Enum):
    AI_CORE_GARDEN = "Sector 1: AI Core Garden"
    ROBOT_TRAINING_ARENA = "Sector 2: Robot Training Arena"
    QUANTUM_SECURITY_LAB = "Sector 3: Quantum Security Lab"
    DIGITAL_FORENSIC_LAB = "Sector 4: Digital Forensic Lab"
    NETWORK_CONTROL_CENTER = "Sector 5: Network Control Center"
    FINAL_NEXUS_CHAMBER = "Sector 6: Final Nexus Chamber"


class Portal:
    """Represents a connection/doorway between two sectors."""
    def __init__(self, from_sector: Sector, from_pos: Tuple[int, int],
                 to_sector: Sector, to_pos: Tuple[int, int],
                 required_keycard: Optional[str] = None,
                 description: str = ""):
        self.from_sector = from_sector
        self.from_pos = from_pos
        self.to_sector = to_sector
        self.to_pos = to_pos
        self.required_keycard = required_keycard
        self.description = description
        self.is_unlocked = required_keycard is None


class SectorMap:
    """Represents a 2D tile map for a single sector."""
    def __init__(self, sector: Sector, width: int = 24, height: int = 14):
        self.sector = sector
        self.width = width
        self.height = height
        self.grid: List[List[TileType]] = [[TileType.FLOOR for _ in range(width)] for _ in range(height)]
        self.interactable_positions: Dict[Tuple[int, int], str] = {}  # (x, y) -> object_id
        self.metadata: Dict[str, Any] = {}
        self.hazard_states: Dict[Tuple[int, int], bool] = {}  # Laser active status

    def set_tile(self, x: int, y: int, tile: TileType):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile

    def get_tile(self, x: int, y: int) -> TileType:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return TileType.WALL

    def is_walkable(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        tile = self.grid[y][x]
        if tile in (TileType.WALL, TileType.DOOR_LOCKED, TileType.VAULT_GATE):
            return False
        if tile == TileType.LASER_BARRIER and self.hazard_states.get((x, y), True):
            return False
        return True


class World:
    """
    The complete NEXUS Research Campus containing all interconnected sectors,
    portals, active security states, and spatial query systems.
    """
    def __init__(self):
        self.sectors: Dict[Sector, SectorMap] = {}
        self.portals: List[Portal] = []
        self.current_sector: Sector = Sector.AI_CORE_GARDEN
        self._build_world()

    def _build_world(self):
        """Constructs all sectors and their architectural layouts."""
        for sector in Sector:
            s_map = SectorMap(sector, width=26, height=15)
            self._generate_sector_layout(s_map)
            self.sectors[sector] = s_map

        self._link_sectors()

    def _generate_sector_layout(self, s_map: SectorMap):
        """Builds themed layout for each sector."""
        w, h = s_map.width, s_map.height

        # Outer walls
        for x in range(w):
            s_map.set_tile(x, 0, TileType.WALL)
            s_map.set_tile(x, h - 1, TileType.WALL)
        for y in range(h):
            s_map.set_tile(0, y, TileType.WALL)
            s_map.set_tile(w - 1, y, TileType.WALL)

        sec = s_map.sector

        if sec == Sector.AI_CORE_GARDEN:
            # Sector 1: AI Core in center, conduit lines, power nodes, coolant valves
            s_map.set_tile(13, 7, TileType.AI_CORE)
            s_map.interactable_positions[(13, 7)] = "obj_ai_core_nexus"

            # Terminal stations
            s_map.set_tile(5, 3, TileType.TERMINAL)
            s_map.interactable_positions[(5, 3)] = "obj_core_terminal_alpha"

            s_map.set_tile(20, 3, TileType.POWER_NODE)
            s_map.interactable_positions[(20, 3)] = "obj_power_cell_alpha"

            s_map.set_tile(5, 11, TileType.POWER_NODE)
            s_map.interactable_positions[(5, 11)] = "obj_power_cell_beta"

            s_map.set_tile(20, 11, TileType.TERMINAL)
            s_map.interactable_positions[(20, 11)] = "obj_coolant_console"

            # NPC Hologram Station: Maintenance Subroutine KAVYA
            s_map.set_tile(17, 7, TileType.TERMINAL)
            s_map.interactable_positions[(17, 7)] = "obj_npc_kavya"

            # Secret Quantum Storage Vault (Hidden Room Discovery)
            s_map.set_tile(24, 2, TileType.TERMINAL)
            s_map.interactable_positions[(24, 2)] = "obj_secret_quantum_vault"

            # Environmental Storytelling stations
            s_map.set_tile(2, 11, TileType.TERMINAL)
            s_map.interactable_positions[(2, 11)] = "obj_damaged_drone_delta3"

            s_map.set_tile(9, 7, TileType.MAINTENANCE_TUNNEL)
            s_map.interactable_positions[(9, 7)] = "obj_hidden_alcove_panel"

            s_map.set_tile(13, 2, TileType.TERMINAL)
            s_map.interactable_positions[(13, 2)] = "obj_abandoned_cryo_flask"

            # Hydroponic silicon partitions (internal walls)
            for y in range(4, 11):
                if y != 7:
                    s_map.set_tile(9, y, TileType.WALL)
                    s_map.set_tile(17, y, TileType.WALL)

            # Hazard conduits
            s_map.set_tile(13, 4, TileType.HAZARD)
            s_map.set_tile(13, 10, TileType.HAZARD)

        elif sec == Sector.ROBOT_TRAINING_ARENA:
            # Sector 2: Hexagonal combat ring, tactics console, sentry bot spawn
            s_map.set_tile(4, 3, TileType.TERMINAL)
            s_map.interactable_positions[(4, 3)] = "obj_arena_tactics_console"

            s_map.set_tile(13, 7, TileType.AI_CORE)  # Combat Core
            s_map.interactable_positions[(13, 7)] = "obj_ares7_chassis"

            s_map.set_tile(21, 7, TileType.POWER_NODE)
            s_map.interactable_positions[(21, 7)] = "obj_combat_power_relay"

            # Obstacle pillars
            for (px, py) in [(8, 4), (8, 10), (18, 4), (18, 10), (13, 3), (13, 11)]:
                s_map.set_tile(px, py, TileType.WALL)

        elif sec == Sector.QUANTUM_SECURITY_LAB:
            # Sector 3: Quantum Vault, laser grid, frequency modulators
            s_map.set_tile(22, 7, TileType.VAULT_GATE)
            s_map.interactable_positions[(22, 7)] = "obj_quantum_vault_door"

            s_map.set_tile(4, 4, TileType.TERMINAL)
            s_map.interactable_positions[(4, 4)] = "obj_quantum_frequency_terminal"

            s_map.set_tile(4, 10, TileType.TERMINAL)
            s_map.interactable_positions[(4, 10)] = "obj_prism_calibrator"

            # Laser grid in center corridor
            for y in range(3, 12):
                s_map.set_tile(12, y, TileType.LASER_BARRIER)
                s_map.hazard_states[(12, y)] = True
                s_map.set_tile(16, y, TileType.LASER_BARRIER)
                s_map.hazard_states[(16, y)] = True

            # Laser bypass terminal
            s_map.set_tile(8, 7, TileType.TERMINAL)
            s_map.interactable_positions[(8, 7)] = "obj_laser_grid_controller"

        elif sec == Sector.DIGITAL_FORENSIC_LAB:
            # Sector 4: Server racks, biometric scanner, holographic evidence deck
            s_map.set_tile(5, 4, TileType.SERVER_RACK)
            s_map.interactable_positions[(5, 4)] = "obj_forensic_server_logs"

            s_map.set_tile(5, 10, TileType.SERVER_RACK)
            s_map.interactable_positions[(5, 10)] = "obj_badge_scanner_station"

            s_map.set_tile(13, 7, TileType.TERMINAL)
            s_map.interactable_positions[(13, 7)] = "obj_holographic_investigation_deck"

            s_map.set_tile(20, 4, TileType.SERVER_RACK)
            s_map.interactable_positions[(20, 4)] = "obj_comm_intercept_rack"

            s_map.set_tile(20, 10, TileType.TERMINAL)
            s_map.interactable_positions[(20, 10)] = "obj_scientist_workstation"

            # Partition divider
            for x in range(8, 18):
                if x != 13:
                    s_map.set_tile(x, 3, TileType.WALL)
                    s_map.set_tile(x, 11, TileType.WALL)

        elif sec == Sector.NETWORK_CONTROL_CENTER:
            # Sector 5: Firewall routers, compromised nodes, network gateway
            s_map.set_tile(4, 7, TileType.TERMINAL)
            s_map.interactable_positions[(4, 7)] = "obj_gateway_router"

            s_map.set_tile(13, 4, TileType.SERVER_RACK)
            s_map.interactable_positions[(13, 4)] = "obj_infected_node_alpha"

            s_map.set_tile(13, 10, TileType.SERVER_RACK)
            s_map.interactable_positions[(13, 10)] = "obj_infected_node_beta"

            s_map.set_tile(21, 7, TileType.TERMINAL)
            s_map.interactable_positions[(21, 7)] = "obj_firewall_isolator_console"

            # Network hub server rows
            for y in range(2, 6):
                s_map.set_tile(9, y, TileType.WALL)
            for y in range(9, 13):
                s_map.set_tile(9, y, TileType.WALL)
            for y in range(2, 6):
                s_map.set_tile(17, y, TileType.WALL)
            for y in range(9, 13):
                s_map.set_tile(17, y, TileType.WALL)

        elif sec == Sector.FINAL_NEXUS_CHAMBER:
            # Sector 6: Master sphere, ethical constraint console, uplink platform
            s_map.set_tile(13, 7, TileType.AI_CORE)
            s_map.interactable_positions[(13, 7)] = "obj_nexus_prime_supercore"

            s_map.set_tile(6, 4, TileType.TERMINAL)
            s_map.interactable_positions[(6, 4)] = "obj_ethical_matrix_terminal"

            s_map.set_tile(20, 4, TileType.TERMINAL)
            s_map.interactable_positions[(20, 4)] = "obj_strips_evacuation_console"

            s_map.set_tile(6, 10, TileType.TERMINAL)
            s_map.interactable_positions[(6, 10)] = "obj_adaptive_learning_core"

            s_map.set_tile(20, 10, TileType.POWER_NODE)
            s_map.interactable_positions[(20, 10)] = "obj_nexus_master_uplink"

            # Grand chamber concentric barriers with 4 access gates
            for x in range(10, 17):
                if x != 13:
                    s_map.set_tile(x, 5, TileType.WALL)
                    s_map.set_tile(x, 9, TileType.WALL)

    def _link_sectors(self):
        """Creates bidirectional portals connecting the research campus."""
        # AI Core Garden (East) <-> Network Control (West)
        self._create_bidirectional_portal(
            Sector.AI_CORE_GARDEN, (24, 7),
            Sector.NETWORK_CONTROL_CENTER, (1, 7),
            required_keycard=None,
            desc="Conduit Corridor to Network Control"
        )

        # AI Core Garden (South) <-> Quantum Security Lab (North)
        self._create_bidirectional_portal(
            Sector.AI_CORE_GARDEN, (13, 13),
            Sector.QUANTUM_SECURITY_LAB, (13, 1),
            required_keycard=None,
            desc="Cryogenic Hatch to Quantum Security"
        )

        # Quantum Security Lab (South) <-> Robot Training Arena (North)
        self._create_bidirectional_portal(
            Sector.QUANTUM_SECURITY_LAB, (13, 13),
            Sector.ROBOT_TRAINING_ARENA, (13, 1),
            required_keycard="KEY_SECURITY_LV2",
            desc="Reinforced Bulkhead to Robot Training Arena"
        )

        # Quantum Security Lab (East) <-> Digital Forensic Lab (West)
        self._create_bidirectional_portal(
            Sector.QUANTUM_SECURITY_LAB, (24, 7),
            Sector.DIGITAL_FORENSIC_LAB, (1, 7),
            required_keycard=None,
            desc="Airbridge to Digital Forensic Lab"
        )

        # Digital Forensic Lab (North) <-> Network Control Center (South)
        self._create_bidirectional_portal(
            Sector.DIGITAL_FORENSIC_LAB, (13, 1),
            Sector.NETWORK_CONTROL_CENTER, (13, 13),
            required_keycard=None,
            desc="Optical Data Line to Network Control"
        )

        # Robot Arena (East) <-> Final Nexus Chamber (West)
        self._create_bidirectional_portal(
            Sector.ROBOT_TRAINING_ARENA, (24, 7),
            Sector.FINAL_NEXUS_CHAMBER, (1, 7),
            required_keycard="KEY_NEXUS_PRIME",
            desc="Hyper-gate to Final Nexus Chamber"
        )

        # Digital Forensic Lab (South) <-> Final Nexus Chamber (North)
        self._create_bidirectional_portal(
            Sector.DIGITAL_FORENSIC_LAB, (13, 13),
            Sector.FINAL_NEXUS_CHAMBER, (13, 1),
            required_keycard="KEY_NEXUS_PRIME",
            desc="Quantum Elevator to Final Nexus Chamber"
        )

    def _create_bidirectional_portal(self, s1: Sector, p1: Tuple[int, int],
                                     s2: Sector, p2: Tuple[int, int],
                                     required_keycard: Optional[str] = None,
                                     desc: str = ""):
        port1 = Portal(s1, p1, s2, p2, required_keycard, desc)
        port2 = Portal(s2, p2, s1, p1, required_keycard, desc)
        self.portals.extend([port1, port2])

        # Mark tiles
        self.sectors[s1].set_tile(p1[0], p1[1], TileType.DOOR_UNLOCKED if required_keycard is None else TileType.DOOR_LOCKED)
        self.sectors[s2].set_tile(p2[0], p2[1], TileType.DOOR_UNLOCKED if required_keycard is None else TileType.DOOR_LOCKED)

    def get_current_map(self) -> SectorMap:
        return self.sectors[self.current_sector]

    def get_portal_at(self, sector: Sector, pos: Tuple[int, int]) -> Optional[Portal]:
        for p in self.portals:
            if p.from_sector == sector and p.from_pos == pos:
                return p
        return None

    def unlock_door(self, sector: Sector, pos: Tuple[int, int]):
        s_map = self.sectors[sector]
        if s_map.get_tile(pos[0], pos[1]) == TileType.DOOR_LOCKED:
            s_map.set_tile(pos[0], pos[1], TileType.DOOR_UNLOCKED)
        for p in self.portals:
            if p.from_sector == sector and p.from_pos == pos:
                p.is_unlocked = True

    def disable_lasers(self, sector: Sector):
        s_map = self.sectors[sector]
        for pos in list(s_map.hazard_states.keys()):
            s_map.hazard_states[pos] = False
            s_map.set_tile(pos[0], pos[1], TileType.FLOOR)
