"""
NEXUS AI REASONING WAR - Interactive Terminal Game Engine (Gameplay Quality Pass)
Provides real-time character movement, proximity interaction badges,
interactive multi-choice circuit wiring menus, live hazard feedback,
and step-by-step algorithm animations.
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Dict, List, Tuple, Optional, Any
import time

from GameEngine.world import World, Sector
from GameEngine.player import Player
from GameEngine.inventory import Inventory
from GameEngine.objects import Terminal, InteractiveObject, Item, ObjectState
from GameEngine.events import EventBus, EventType
from GameEngine.interaction import InteractionHandler
from GameEngine.missions import MissionManager, MissionStatus
from ML.ml_pipeline import MLPipeline
from AI_Agent.nova_agent import NovaCompanion
from AI_Agent.autonomous_solver import AutonomousSolver
from AI_Agent.reasoning_tracer import ReasoningTracer
from Missions.m01_restore_ai_core import Mission01RestoreAICore
from .ascii_art import AsciiArt
from .game_visualizer import GameVisualizer


class TerminalGameEngine:
    """Main terminal game controller supporting physical exploration and interactive visual puzzles."""
    def __init__(self):
        self.world = World()
        self.player = Player()
        self.inventory = Inventory()
        self.event_bus = EventBus()
        self.interaction = InteractionHandler(self.world, self.player, self.inventory, self.event_bus)
        self.missions = MissionManager(self.player, self.inventory, self.event_bus)
        self.ml_pipeline = MLPipeline(self.player, self.event_bus)
        self.nova = NovaCompanion()
        self.autonomous_solver = AutonomousSolver(self.world, self.player, self.missions)
        self.tracer = ReasoningTracer()

        self.is_running = True
        self.status_message = "NEXUS RESEARCH FACILITY // Navigate using W/A/S/D. Approach machines to interact."
        self.current_tracer_text = ""

        self._register_world_objects()

    def _register_world_objects(self):
        m1 = self.missions.get_mission("M01")
        for sector_name, s_map in self.world.sectors.items():
            for pos, obj_id in s_map.interactable_positions.items():
                if obj_id == "obj_core_terminal_alpha":
                    desc = m1.discovered_logs.get("LOG_ENGINEER_MEMO", "Diagnostic console.") if m1 else "Diagnostic console."
                    term = Terminal(obj_id, "Terminal Alpha (Engineering Directives)", desc, pos, sector_name.value, puzzle_id="M01")
                    self.interaction.register_object(term)
                elif obj_id == "obj_coolant_console":
                    desc = m1.discovered_logs.get("LOG_MAINTENANCE_44", "Coolant system monitor.") if m1 else "Coolant system monitor."
                    term = Terminal(obj_id, "Coolant Valve Console #44", desc, pos, sector_name.value, puzzle_id=None)
                    self.interaction.register_object(term)
                elif obj_id == "obj_damaged_drone_delta3":
                    desc = m1.discovered_logs.get("LOG_DRONE_DELTA3", "Damaged drone.") if m1 else "Damaged drone."
                    term = Terminal(obj_id, "Damaged Drone Unit Delta-3", desc, pos, sector_name.value, puzzle_id=None)
                    self.interaction.register_object(term)
                elif obj_id == "obj_hidden_alcove_panel":
                    desc = m1.discovered_logs.get("LOG_HIDDEN_ALCOVE", "Maintenance crawlspace.") if m1 else "Maintenance crawlspace."
                    term = Terminal(obj_id, "Secret Maintenance Crawlspace Panel", desc, pos, sector_name.value, puzzle_id=None)
                    self.interaction.register_object(term)
                elif obj_id == "obj_abandoned_cryo_flask":
                    desc = m1.discovered_logs.get("LOG_CRYO_FLASK", "Abandoned cryo-flask.") if m1 else "Abandoned cryo-flask."
                    term = Terminal(obj_id, "Abandoned Cryo-Flask Containment", desc, pos, sector_name.value, puzzle_id=None)
                    self.interaction.register_object(term)
                elif obj_id == "obj_power_cell_beta":
                    desc = m1.discovered_logs.get("LOG_BREAKER_SCHEMATIC", "Power cell telemetry.") if m1 else "Power cell telemetry."
                    term = Terminal(obj_id, "Power Cell Beta Telemetry Port", desc, pos, sector_name.value, puzzle_id=None)
                    self.interaction.register_object(term)
                elif "terminal" in obj_id or "console" in obj_id or "deck" in obj_id or "core" in obj_id:
                    term = Terminal(obj_id, obj_id.replace("obj_", "").replace("_", " ").title(),
                                    f"Interactive console terminal located in {sector_name.value}.",
                                    pos, sector_name.value, puzzle_id=self._map_obj_to_mission(obj_id))
                    self.interaction.register_object(term)
                else:
                    iobj = InteractiveObject(obj_id, obj_id.replace("obj_", "").replace("_", " ").title(),
                                             f"Quantum/Physical machine unit in {sector_name.value}.",
                                             pos, sector_name.value)
                    self.interaction.register_object(iobj)

    def _map_obj_to_mission(self, obj_id: str) -> Optional[str]:
        mapping = {
            "obj_core_terminal_alpha": "M01",
            "obj_ai_core_nexus": "M01",
            "obj_holographic_investigation_deck": "M02",
            "obj_quantum_frequency_terminal": "M03",
            "obj_arena_tactics_console": "M04",
            "obj_gateway_router": "M05",
            "obj_coolant_console": "M06",
            "obj_ethical_matrix_terminal": "M07",
            "obj_strips_evacuation_console": "M08",
            "obj_prism_calibrator": "M09",
            "obj_nexus_prime_supercore": "M10"
        }
        return mapping.get(obj_id)

    def render_current_screen(self) -> str:
        active_m = self.missions.get_active_mission()
        return GameVisualizer.render_viewport(
            self.world, self.player, self.ml_pipeline, active_m,
            self.inventory, self.status_message, self.current_tracer_text
        )

    def handle_input_command(self, cmd: str) -> str:
        cmd = cmd.strip().lower()
        if not cmd:
            return "No command entered."

        # Movement commands
        if cmd in ("w", "up", "north"):
            success, msg = self.player.move(0, -1, self.world)
            self.status_message = msg
        elif cmd in ("s", "down", "south"):
            success, msg = self.player.move(0, 1, self.world)
            self.status_message = msg
        elif cmd in ("a", "left", "west"):
            success, msg = self.player.move(-1, 0, self.world)
            self.status_message = msg
        elif cmd in ("d", "right", "east"):
            success, msg = self.player.move(1, 0, self.world)
            self.status_message = msg

        # Interaction / Puzzle Mode
        elif cmd in ("e", "interact", "use"):
            target_info = self.player.check_interaction_target(self.world)
            if target_info:
                pos, obj_id = target_info
                if obj_id == "obj_npc_kavya":
                    return self.run_terminal_kavya_dialogue()
                elif obj_id == "obj_secret_quantum_vault":
                    return self.run_terminal_secret_vault()
                elif obj_id == "obj_power_cell_beta":
                    return self.run_terminal_voltage_balancer()
                elif obj_id == "obj_coolant_console":
                    return self.run_terminal_cryo_valves()
                elif obj_id == "obj_hidden_alcove_panel":
                    if not self.inventory.has_item("ITEM_LOGIC_PROBE"):
                        self.inventory.add_item(Item("ITEM_LOGIC_PROBE", "Standard Logic Probe", "Used to bridge high-voltage circuits.", category="TOOL"))
                        self.status_message = "🔍 DISCOVERED HIDDEN ALCOVE! [ACQUIRED]: Standard Logic Probe added to inventory!"
                    else:
                        self.status_message = "🔍 Secret maintenance crawlspace is now empty."
                    return self.status_message

            success, msg, puzzle_id = self.interaction.handle_interact()
            self.status_message = msg
            if puzzle_id == "M01":
                return self.run_interactive_mission01_puzzle()
            elif puzzle_id:
                return self.open_generic_puzzle_interface(puzzle_id)

        # Inspection
        elif cmd in ("insp", "inspect", "look"):
            success, msg = self.interaction.handle_inspect()
            self.status_message = msg

        # Hacking
        elif cmd in ("h", "hack"):
            success, msg, puzzle_id = self.interaction.handle_hack()
            self.status_message = msg
            if puzzle_id == "M01":
                return self.run_interactive_mission01_puzzle()

        # NOVA Companion Hint
        elif cmd in ("n", "nova", "hint"):
            active_m = self.missions.get_active_mission()
            hint, count = self.nova.provide_hint(active_m, self.player, self.ml_pipeline.current_archetype)
            self.status_message = f"NOVA: {hint}"

        # Autonomous AI Solving Mode
        elif cmd in ("ai", "solve", "watch"):
            return self.run_autonomous_ai_demonstration()

        # Inventory
        elif cmd in ("i", "inventory", "items"):
            items_str = ", ".join(self.inventory.list_items_summary()) if self.inventory.items else "Empty"
            self.status_message = f"INVENTORY: {items_str}"

        # Help
        elif cmd in ("help", "?"):
            self.status_message = "CONTROLS: W/A/S/D (Move) | E (Interact/Wire) | H (Hack) | N (NOVA Hint) | AI (Watch AI) | I (Items) | Q (Quit)"

        elif cmd in ("q", "quit", "exit"):
            self.is_running = False
            self.status_message = "Shutting down simulation."

        else:
            self.status_message = f"Unknown command: '{cmd}'. Press 'help' for command list."

        return self.status_message

    def run_interactive_mission01_puzzle(self) -> str:
        """Dedicated interactive circuit wiring game for Mission 1."""
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return "Mission 1 not found."

        print("\n" + "="*70)
        print("⚡ POWER CONDUIT BLUEPRINT TERMINAL — MISSION 01")
        print("="*70)
        print("The AI Core is dark. Wire the conduit from Relay Alpha (N0) to AI Core (N9).")
        print("WARNING: Relays with sub-zero coolant (⚠️) will trigger electrical discharge!\n")

        while m1.status != MissionStatus.COMPLETED:
            curr_route = " -> ".join(m1.connected_route)
            print(f"CURRENT ENERGIZED ROUTE: [{curr_route}]")
            avail = m1.get_available_next_nodes()

            if not avail:
                print("No further connections from this branch. Resetting route.")
                m1.connected_route = ["N0"]
                continue

            print("\nReachable Conduit Nodes:")
            for idx, nid in enumerate(avail):
                ninfo = m1.power_nodes[nid]
                hazard_warn = " [⚠️ CRYO-COOLANT WARNING]" if ninfo.is_hazard else ""
                print(f"  [{idx+1}] Connect to {nid}: {ninfo.name}{hazard_warn}")
            print("  [A] Switch to NOVA Autonomous AI Solve Mode")
            print("  [X] Exit Terminal")

            choice = input("\nSelect Node to Wire (1-N/A/X): ").strip().lower()
            if choice == "x":
                self.status_message = "Exited terminal interface."
                return self.status_message
            elif choice == "a":
                return self.run_autonomous_ai_demonstration()
            elif choice.isdigit() and 1 <= int(choice) <= len(avail):
                selected_nid = avail[int(choice) - 1]
                success, msg, data = m1.connect_next_node(selected_nid, self.inventory)
                print(f"\n>> {msg}")

                if not success and data.get("hazard_triggered"):
                    self.player.health = max(0, self.player.health - 20)
                    self.player.stats.record_mistake("Triggered cryogenic hazard in circuit")
                    print(f">> DAMAGE TAKEN: 20 HP! Current HP: {self.player.health}/100")
                elif data.get("ready_for_moral_decision"):
                    print("\n" + "="*70)
                    print("💎 CENTRAL AI CORE MASTER CONSOLE: FINAL ARCHITECTURAL COMMAND")
                    print("="*70)
                    print("AEGIS AI and NOVA await your final command:")
                    print("  [1] RESTORE: Full Unfettered AI Awakening (100% Core Energy)")
                    print("  [2] CONTAIN: Sandbox Quarantine Buffer (AEGIS Precaution)")
                    print("  [3] MERGE: Neural Synthesis (NOVA Empathy + AEGIS Safety)")

                    while True:
                        dec = input("\nEnter Decision (1/2/3): ").strip()
                        dec_map = {"1": "RESTORE", "2": "CONTAIN", "3": "MERGE"}
                        if dec in dec_map:
                            succ, end_msg, res = m1.execute_final_moral_decision(dec_map[dec])
                            self.world.unlock_door(Sector.AI_CORE_GARDEN, (24, 7))
                            print(f"\n>> {end_msg}\n")
                            debrief = m1.generate_post_mission_debrief(self.player.stats)
                            print(f"{debrief}\n")
                            self.status_message = f"🎉 MISSION 1 COMPLETE! [{dec_map[dec]} ENDING ACHIEVED]"
                            return self.status_message
                elif success and data.get("completed"):
                    self.world.unlock_door(Sector.AI_CORE_GARDEN, (24, 7))
                    debrief = m1.generate_post_mission_debrief(self.player.stats)
                    print(f"\n{debrief}\n")
                    self.status_message = f"🎉 MISSION 1 COMPLETE! [{data.get('solution_type', 'OPTIMAL')} STRATEGY VERIFIED]"
                    return self.status_message
            else:
                print("Invalid selection.")

        return self.status_message

    def open_generic_puzzle_interface(self, puzzle_id: str) -> str:
        mission = self.missions.get_mission(puzzle_id)
        if not mission:
            return f"No puzzle bound to {puzzle_id}."

        self.missions.active_mission_id = puzzle_id
        if mission.status == MissionStatus.LOCKED:
            mission.activate()

        info = [
            f"╔═══ [PUZZLE TERMINAL: {mission.title}] ═══",
            f"║ CONCEPT: {mission.algorithm_concept}",
            f"║ DETAILS: {mission.description}",
            f"║ CLUES GATHERED:",
            f"║ {mission.get_clue_summary()}",
            f"╠═══════════════════════════════════════════════════════════════",
            f"║ Press [AI] to watch NOVA execute the live algorithmic solution!",
            f"╚═══════════════════════════════════════════════════════════════"
        ]
        self.current_tracer_text = "\n".join(info)
        return self.current_tracer_text

    def run_terminal_voltage_balancer(self) -> str:
        """Interactive CLI Mini-Puzzle: Voltage Balancer."""
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return "Mission 1 not found."

        print("\n" + "="*60)
        print("⚡ POWER CELL BETA: VOLTAGE HARMONIC BALANCER")
        print("="*60)
        print("Target: 120.0V (Standard Line Output). Eliminate voltage harmonics.")

        while True:
            print(f"\nCURRENT OUTPUT: [{m1.current_balanced_voltage:.1f} V]")
            print(f"SWITCH STATUS : [SW1 (+15V): {m1.voltage_switches['SW_1']} | SW2 (+10V): {m1.voltage_switches['SW_2']} | SW3 (-5V): {m1.voltage_switches['SW_3']}]")
            print("  [1] Toggle Switch 1 (+15V)")
            print("  [2] Toggle Switch 2 (+10V)")
            print("  [3] Toggle Switch 3 (-5V)")
            print("  [X] Exit Console")

            c = input("\nSelect switch (1/2/3/X): ").strip().lower()
            if c == "x":
                break
            elif c == "1":
                succ, msg, v = m1.toggle_voltage_switch("SW_1")
                print(f">> {msg}")
                if succ: break
            elif c == "2":
                succ, msg, v = m1.toggle_voltage_switch("SW_2")
                print(f">> {msg}")
                if succ: break
            elif c == "3":
                succ, msg, v = m1.toggle_voltage_switch("SW_3")
                print(f">> {msg}")
                if succ: break

        self.status_message = f"Voltage Balancer status: Output is {m1.current_balanced_voltage:.1f}V."
        return self.status_message

    def run_terminal_cryo_valves(self) -> str:
        """Interactive CLI Mini-Puzzle: Cryogenic Valve Venting."""
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return "Mission 1 not found."

        print("\n" + "="*60)
        print("💨 COOLANT CONSOLE #44: CRYOGENIC MANIFOLD")
        print("="*60)
        print("Liquid nitrogen leak at Relay N6 (77K). Align valves to vent corridor.")

        while True:
            v_status = "VENTED (SAFE)" if m1.cryo_vented_safe else "HAZARD ACTIVE (77K)"
            print(f"\nMANIFOLD STATUS: [{v_status}]")
            print(f"VALVES: [Valve A: {m1.cryo_valves['VALVE_A']} | Valve B: {m1.cryo_valves['VALVE_B']} | Valve C: {m1.cryo_valves['VALVE_C']}]")
            print("  [1] Toggle Valve A")
            print("  [2] Toggle Valve B")
            print("  [3] Toggle Valve C")
            print("  [X] Exit Console")

            c = input("\nSelect valve (1/2/3/X): ").strip().lower()
            if c == "x":
                break
            elif c == "1":
                succ, msg = m1.toggle_cryo_valve("VALVE_A")
                print(f">> {msg}")
                if succ: break
            elif c == "2":
                succ, msg = m1.toggle_cryo_valve("VALVE_B")
                print(f">> {msg}")
                if succ: break
            elif c == "3":
                succ, msg = m1.toggle_cryo_valve("VALVE_C")
                print(f">> {msg}")
                if succ: break

        self.status_message = f"Coolant Console: Manifold vented={m1.cryo_vented_safe}."
        return self.status_message

    def run_terminal_kavya_dialogue(self) -> str:
        """Interactive NPC Dialogue Tree with Maintenance AI KAVYA."""
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return "Mission 1 not found."

        choice_id = None
        while True:
            resp, choices = m1.interact_with_kavya(choice_id, self.inventory)
            print("\n" + "="*65)
            print(resp)
            print("="*65)

            for idx, (cid, ctext) in enumerate(choices):
                print(f"  [{idx+1}] {ctext}")

            sel = input("\nSelect response (1-N): ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(choices):
                selected_choice_id, _ = choices[int(sel) - 1]
                if selected_choice_id == "CHOICE_EXIT":
                    break
                choice_id = selected_choice_id
            else:
                break

        self.status_message = "Completed conversation with Maintenance Hologram KAVYA."
        return self.status_message

    def run_terminal_secret_vault(self) -> str:
        """Interactive Secret Vault Terminal."""
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return "Mission 1 not found."

        print("\n" + "="*60)
        print("🔍 SECRET QUANTUM STORAGE VAULT")
        print("="*60)
        if m1.secret_vault_unlocked:
            print("Vault is already unlocked. Cache is empty.")
            input("Press ENTER to return...")
            return "Secret Vault already unlocked."

        print("Frequency lock engaged. Enter 3-digit access code (from logs) or [X] to exit:")
        code = input("Override Code: ").strip()
        if code == "488" or self.inventory.has_item("ITEM_LOGIC_PROBE"):
            m1.secret_vault_unlocked = True
            self.inventory.add_item(Item("ITEM_QUANTUM_CORE_SHARD", "Overcharged Quantum Cell", "Supercharges AI Core to 200% capacity.", category="TOOL"))
            print("\n🎉 ACCESS GRANTED! Discovered: [Overcharged Quantum Cell] added to inventory!")
            input("Press ENTER to continue...")
            self.status_message = "Discovered Secret Quantum Storage Vault!"
        else:
            print("❌ ACCESS DENIED: Invalid frequency code.")
            self.status_message = "Secret Vault access denied."

        return self.status_message

    def run_autonomous_ai_demonstration(self) -> str:
        """Runs NOVA's live step-by-step visual solution with step pacing."""
        active_m = self.missions.get_active_mission()
        if not active_m:
            return "No active mission."

        print(f"\n[*] NOVA AI: Initializing Autonomous Solution for {active_m.title}...")
        for step in self.autonomous_solver.solve_active_mission():
            msg = step.get("message", "")
            print(f"  -> {msg}")
            time.sleep(0.08)  # Dramatic visual step pacing

        self.world.unlock_door(Sector.AI_CORE_GARDEN, (24, 7))
        self.status_message = f"NOVA: Autonomous solution finished! Sector conduits energized."
        return self.status_message

    def run_interactive_loop(self):
        print(AsciiArt.BANNER)
        print(self.nova.greet(self.player.name))
        print("\nPress ENTER to enter the NEXUS Research Campus...")
        try:
            input()
        except EOFError:
            pass

        while self.is_running:
            print("\033[H\033[J", end="")  # Clear ANSI screen
            print(self.render_current_screen())
            try:
                cmd = input("\n[NEXUS_OS >> Action (WASD/E/H/N/AI/I/Q)]: ")
                self.handle_input_command(cmd)
            except (EOFError, KeyboardInterrupt):
                break

        print("\nThank you for playing NEXUS AI REASONING WAR!")
