"""
NEXUS AI REASONING WAR - 2D Map & Algorithm Frame Visualizer
Renders the real-time game viewport, player coordinates, nearby interactable machines,
live telemetry radar, and algorithm execution windows.
"""

from typing import List, Dict, Tuple, Optional, Any
from GameEngine.world import World, SectorMap, TileType, Sector
from GameEngine.player import Player
from GameEngine.inventory import Inventory
from GameEngine.missions import MissionBase, MissionManager
from ML.ml_pipeline import MLPipeline


class GameVisualizer:
    """Renders composite game frames for terminal canvas and debugging views."""
    TILE_SYMBOLS = {
        TileType.FLOOR: " .",
        TileType.WALL: "██",
        TileType.DOOR_LOCKED: "▓D",
        TileType.DOOR_UNLOCKED: "░O",
        TileType.HAZARD: "▲▲",
        TileType.TERMINAL: "🖥️ ",
        TileType.POWER_NODE: "⚡",
        TileType.AI_CORE: "💎",
        TileType.SERVER_RACK: "🖧 ",
        TileType.LASER_BARRIER: "══",
        TileType.VAULT_GATE: "🔒",
        TileType.EMPTY: "  "
    }

    PLAYER_SYMBOL = "🤖"  # Dr. Aarav Sharma in engineering exoskeleton
    NOVA_SYMBOL = "✨"

    @classmethod
    def render_viewport(cls, world: World, player: Player,
                        ml_pipeline: MLPipeline,
                        active_mission: Optional[MissionBase],
                        inventory: Inventory,
                        status_message: str = "",
                        tracer_output: str = "") -> str:
        s_map = world.get_current_map()
        grid = s_map.grid
        h, w = len(grid), len(grid[0])

        # Render 2D Grid
        map_lines = []
        for y in range(h):
            row_str = ""
            for x in range(w):
                if (x, y) == (player.x, player.y):
                    row_str += cls.PLAYER_SYMBOL
                else:
                    tile = grid[y][x]
                    row_str += cls.TILE_SYMBOLS.get(tile, " .")
            map_lines.append(row_str)

        # ML Telemetry Profile
        profile = ml_pipeline.update_live_profile()
        assessment = profile.get("assessment", {})
        threat_meter = assessment.get("threat_meter", "████░░░░░░")
        threat_desc = assessment.get("threat_desc", "NOMINAL")
        archetype = profile["archetype"]

        # Compose Layout Frame
        lines = [
            "╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗",
            f"║ NEXUS OS v4.88 // {world.current_sector.value:<40} [NOVA COMPANION: ACTIVE] ║",
            "╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣"
        ]

        # Combine Map on Left with Status / Telemetry on Right
        sidebar_rows = [
            f" AGENT : {player.name} [HP: {player.health}/100 | NRG: {player.energy}/100]",
            f" TACTICAL PROFILE : {archetype}",
            f" THREAT MONITOR   : [{threat_meter}] {threat_desc}",
            f" NOVA ADVISORY    : {assessment.get('nova_recommendation', 'Inspect nearby relays.')[:42]}",
            f" EXPLORATION      : {player.stats.steps_taken} steps | Anomalies: {player.stats.mistakes_count}",
            "────────────────────────────────────────────────────────",
            f" OBJECTIVE : {active_mission.title if active_mission else 'Explore Sector'}",
            f" PROTOCOL  : {active_mission.algorithm_concept if active_mission else 'Environmental Recon'}",
            "────────────────────────────────────────────────────────",
            f" TOOL DECK ({len(inventory.items)}/{inventory.capacity}):"
        ]

        for i, it in enumerate(inventory.items[:4]):
            sidebar_rows.append(f"  [{i+1}] {it.name[:38]}")

        while len(sidebar_rows) < len(map_lines):
            sidebar_rows.append("")

        for y in range(len(map_lines)):
            map_part = map_lines[y]
            side_part = sidebar_rows[y] if y < len(sidebar_rows) else ""
            lines.append(f"║ {map_part:<52} │ {side_part:<46} ║")

        lines.append("╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
        lines.append(f"║ STATUS: {status_message[:92]:<92} ║")
        lines.append("║ CONTROLS: [W/A/S/D] Move | [E] Interact/Solve | [H] Hack | [I] Items | [N] NOVA Advisor | [Q] Quit    ║")

        if tracer_output:
            lines.append("╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
            for t_line in tracer_output.split("\n"):
                lines.append(f"║ {t_line[:98]:<98} ║")

        lines.append("╚════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
        return "\n".join(lines)
