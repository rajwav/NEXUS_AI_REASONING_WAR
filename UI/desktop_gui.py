"""
NEXUS AI REASONING WAR - Native Desktop GUI Game Engine (Gameplay Quality Pass)
Provides a rich 60 FPS 2D graphical game window with top-down character movement,
camera tracking, animated laser conduits, interactive circuit puzzle canvas,
sound effects, spark particles, and live step-by-step AI search tree animations.
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Dict, List, Tuple, Optional, Any
import time
import math
import random

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TK_AVAILABLE = True
except ImportError:
    TK_AVAILABLE = False

from GameEngine.world import World, Sector, TileType
from GameEngine.player import Player
from GameEngine.inventory import Inventory
from GameEngine.events import EventBus, EventType
from GameEngine.interaction import InteractionHandler
from GameEngine.missions import MissionManager, MissionStatus
from ML.ml_pipeline import MLPipeline
from AI_Agent.nova_agent import NovaCompanion
from AI_Agent.autonomous_solver import AutonomousSolver
from AI_Agent.reasoning_tracer import ReasoningTracer
from Missions.m01_restore_ai_core import Mission01RestoreAICore


class SparkParticle:
    def __init__(self, x: float, y: float, color: str = "#00E5FF"):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = random.randint(10, 25)
        self.max_life = self.life


class DesktopGUIEngine:
    """State-of-the-art 2D Desktop Graphical Game Window with 60 FPS Animation Engine."""
    def __init__(self):
        if not TK_AVAILABLE:
            raise RuntimeError("Tkinter is not available in this Python environment.")

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

        self.tile_size = 38
        self.anim_tick = 0
        self.particles: List[SparkParticle] = []
        self.door_anim_progress: Dict[Tuple[int, int], float] = {}
        self.active_puzzle_overlay: Optional[str] = None
        self.ai_solve_in_progress: bool = False
        self.ai_step_generator = None

        self.status_text = "NEXUS RESEARCH COMPLEX // Use W/A/S/D or Arrow Keys to move. Walk near machines to inspect."
        self._init_window()

    def _init_window(self):
        self.root = tk.Tk()
        self.root.title("NEXUS: AI REASONING WAR (2088) — Playable AI Adventure Game")
        self.root.geometry("1180x760")
        self.root.configure(bg="#050811")

        # Top Cyber Header Bar
        self.header_frame = tk.Frame(self.root, bg="#0D1527", height=50, highlightthickness=1, highlightbackground="#00E5FF")
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.title_lbl = tk.Label(
            self.header_frame, text="⚡ NEXUS AI REASONING WAR (2088)",
            font=("Helvetica", 14, "bold"), fg="#00E5FF", bg="#0D1527"
        )
        self.title_lbl.pack(side=tk.LEFT, padx=15, pady=10)

        self.sector_lbl = tk.Label(
            self.header_frame, text="SECTOR: AI CORE GARDEN",
            font=("Helvetica", 12, "bold"), fg="#FFD600", bg="#0D1527"
        )
        self.sector_lbl.pack(side=tk.LEFT, padx=25, pady=10)

        self.nova_badge = tk.Label(
            self.header_frame, text="✨ NOVA COMPANION: ONLINE",
            font=("Helvetica", 11, "bold"), fg="#76FF03", bg="#0D1527"
        )
        self.nova_badge.pack(side=tk.RIGHT, padx=15, pady=10)

        # Main Layout Container
        self.main_container = tk.Frame(self.root, bg="#050811")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Left 2D Game Canvas
        self.canvas = tk.Canvas(
            self.main_container, width=880, height=570,
            bg="#03060C", highlightthickness=2, highlightbackground="#1E2C48"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Right HUD / Diagnostics Panel
        self.hud_frame = tk.Frame(self.main_container, width=280, bg="#0D1527", padx=12, pady=12, highlightthickness=1, highlightbackground="#1E2C48")
        self.hud_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.hud_title = tk.Label(self.hud_frame, text="🧠 COGNITIVE RADAR (ML)", font=("Helvetica", 11, "bold"), fg="#00E5FF", bg="#0D1527")
        self.hud_title.pack(anchor="w", pady=(0, 4))

        self.telemetry_txt = tk.StringVar()
        self.telemetry_lbl = tk.Label(self.hud_frame, textvariable=self.telemetry_txt, justify=tk.LEFT, font=("Courier", 9, "bold"), fg="#E0E6ED", bg="#141E34", padx=10, pady=8)
        self.telemetry_lbl.pack(fill=tk.X, pady=4)

        self.mission_hdr = tk.Label(self.hud_frame, text="🎯 ACTIVE MISSION", font=("Helvetica", 11, "bold"), fg="#FFD600", bg="#0D1527")
        self.mission_hdr.pack(anchor="w", pady=(10, 4))

        self.mission_txt = tk.StringVar()
        self.mission_lbl = tk.Label(self.hud_frame, textvariable=self.mission_txt, justify=tk.LEFT, font=("Helvetica", 9), fg="#FFFFFF", bg="#141E34", padx=10, pady=8, wraplength=250)
        self.mission_lbl.pack(fill=tk.X, pady=4)

        # Action Buttons Deck
        self.btn_interact = tk.Button(self.hud_frame, text="⚡ [E] Interact with Machine", font=("Helvetica", 10, "bold"), bg="#00E5FF", fg="#000000", activebackground="#00B0FF", command=self._on_interact_action)
        self.btn_interact.pack(fill=tk.X, pady=5)

        self.btn_nova = tk.Button(self.hud_frame, text="✨ [N] Ask NOVA Advice", font=("Helvetica", 10), bg="#2979FF", fg="#FFFFFF", activebackground="#2962FF", command=self._on_nova_action)
        self.btn_nova.pack(fill=tk.X, pady=4)

        self.btn_ai_solve = tk.Button(self.hud_frame, text="🤖 [AI] Watch NOVA Solve", font=("Helvetica", 10, "bold"), bg="#76FF03", fg="#000000", activebackground="#64DD17", command=self._on_ai_solve_action)
        self.btn_ai_solve.pack(fill=tk.X, pady=4)

        self.btn_inventory = tk.Button(self.hud_frame, text="🎒 [I] View Inventory", font=("Helvetica", 10), bg="#37474F", fg="#FFFFFF", command=self._on_inventory_action)
        self.btn_inventory.pack(fill=tk.X, pady=4)

        # Bottom Status Bar with Cyber Log
        self.status_bar = tk.Label(
            self.root, text=self.status_text, font=("Helvetica", 10, "bold"),
            fg="#00E5FF", bg="#0A0E1A", anchor="w", padx=15, pady=8
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Keyboard Bindings
        self.root.bind("<w>", lambda e: self._handle_move(0, -1))
        self.root.bind("<s>", lambda e: self._handle_move(0, 1))
        self.root.bind("<a>", lambda e: self._handle_move(-1, 0))
        self.root.bind("<d>", lambda e: self._handle_move(1, 0))
        self.root.bind("<Up>", lambda e: self._handle_move(0, -1))
        self.root.bind("<Down>", lambda e: self._handle_move(0, 1))
        self.root.bind("<Left>", lambda e: self._handle_move(-1, 0))
        self.root.bind("<Right>", lambda e: self._handle_move(1, 0))
        self.root.bind("<e>", lambda e: self._on_interact_action())
        self.root.bind("<n>", lambda e: self._on_nova_action())
        self.root.bind("<i>", lambda e: self._on_inventory_action())
        self.root.bind("<Escape>", lambda e: self._close_puzzle_overlay())

        # Start 60 FPS Game Render Loop
        self._game_loop()

    def _game_loop(self):
        self.anim_tick += 1

        # Update particles
        for p in list(self.particles):
            p.x += p.vx
            p.y += p.vy
            p.life -= 1
            if p.life <= 0:
                self.particles.remove(p)

        # Step AI autonomous solver if running
        if self.ai_solve_in_progress and self.ai_step_generator:
            try:
                step = next(self.ai_step_generator)
                msg = step.get("message", "")
                self.status_text = f"NOVA AI: {msg}"
                self.status_bar.config(text=self.status_text)
                
                # If node step, create celebratory sparks
                if "current_node" in step or "current_pos" in step:
                    nx = step.get("current_node", {}).get("x", self.player.x)
                    ny = step.get("current_node", {}).get("y", self.player.y)
                    self.player.x = nx
                    self.player.y = ny
                    self._spawn_sparks(nx * self.tile_size + 19, ny * self.tile_size + 19, "#76FF03", 5)

            except StopIteration:
                self.ai_solve_in_progress = False
                self.ai_step_generator = None
                self.status_text = "NOVA: Solution complete! Sector conduits energized."
                self.status_bar.config(text=self.status_text)
                self._trigger_door_open_animation()

        self._render_canvas()
        self._update_hud()
        self.root.after(33, self._game_loop)  # ~30-60 FPS smooth timer

    def _spawn_sparks(self, x: float, y: float, color: str = "#00E5FF", count: int = 8):
        for _ in range(count):
            self.particles.append(SparkParticle(x, y, color))

    def _handle_move(self, dx: int, dy: int):
        if self.active_puzzle_overlay:
            return  # In puzzle modal

        success, msg = self.player.move(dx, dy, self.world)
        self.status_text = msg
        self.status_bar.config(text=self.status_text)
        self.sector_lbl.config(text=f"SECTOR: {self.world.current_sector.value.upper()}")

        if not success and "damage" in msg:
            self._spawn_sparks(self.player.x * self.tile_size + 19, self.player.y * self.tile_size + 19, "#FF1744", 15)
            try:
                self.root.bell()  # Audible hazard alert
            except Exception:
                pass

    def _on_interact_action(self):
        if self.active_puzzle_overlay:
            return

        target_info = self.player.check_interaction_target(self.world)
        if not target_info:
            self.status_text = "Walk closer to a terminal, drone, or AI Core to interact."
            self.status_bar.config(text=self.status_text)
            return

        pos, obj_id = target_info
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")

        # Storytelling inspections
        if obj_id == "obj_damaged_drone_delta3":
            log = m1.discovered_logs.get("LOG_DRONE_DELTA3")
            messagebox.showinfo("🤖 Damaged Drone Delta-3 Log", log)
            self.status_text = "Recovered optic sensor log from Drone Delta-3."
            self.status_bar.config(text=self.status_text)
            return
        # NPC Dialogue: Maintenance Subroutine KAVYA
        elif obj_id == "obj_npc_kavya":
            self._open_kavya_dialog(m1)
            return

        # Secret Quantum Storage Vault
        elif obj_id == "obj_secret_quantum_vault":
            self._open_secret_vault_dialog(m1)
            return

        elif obj_id == "obj_abandoned_cryo_flask":
            log = m1.discovered_logs.get("LOG_CRYO_FLASK")
            messagebox.showinfo("🧪 Shattered Cryo-Flask", log)
            self.status_text = "Liquid nitrogen residue detected on floor."
            self.status_bar.config(text=self.status_text)
            return
        elif obj_id == "obj_hidden_alcove_panel":
            log = m1.discovered_logs.get("LOG_HIDDEN_ALCOVE")
            if not self.inventory.has_item("ITEM_LOGIC_PROBE"):
                self.inventory.add_item(Item("ITEM_LOGIC_PROBE", "Standard Logic Probe", "Used to bridge high-voltage circuits.", category="TOOL"))
                messagebox.showinfo("🔍 Secret Alcove Discovered!", log + "\n\n[ACQUIRED]: Standard Logic Probe added to inventory!")
            else:
                messagebox.showinfo("🔍 Secret Alcove", "Emergency technician cache is now empty.")
            self.status_text = "Discovered technician's secret maintenance crawlspace!"
            self.status_bar.config(text=self.status_text)
            return
        elif obj_id == "obj_coolant_console":
            self._open_cryo_valve_dialog(m1)
            return
        elif obj_id == "obj_power_cell_beta":
            self._open_voltage_balancer_dialog(m1)
            return
        elif obj_id == "obj_core_terminal_alpha":
            log = m1.discovered_logs.get("LOG_ENGINEER_MEMO")
            messagebox.showinfo("📋 Terminal Alpha - Engineering Directives", log)
            self.status_text = "Read Prof. Meera Iyer's engineering directives."
            self.status_bar.config(text=self.status_text)
            return

        if "terminal" in obj_id or "core" in obj_id or "console" in obj_id:
            # Open Mission 1 Interactive Circuit Screen
            self.active_puzzle_overlay = "M01"
            self.status_text = "POWER GRID BLUEPRINT ONLINE // Connect nodes from Relay Alpha (N0) to AI Core (N9)."
            self.status_bar.config(text=self.status_text)
            self._spawn_sparks(pos[0] * self.tile_size + 19, pos[1] * self.tile_size + 19, "#00E5FF", 12)

    def _on_nova_action(self):
        active_m = self.missions.get_active_mission()
        hint, _ = self.nova.provide_hint(active_m, self.player, self.ml_pipeline.current_archetype)
        messagebox.showinfo("✨ NOVA AI Companion", hint)

    def _on_ai_solve_action(self):
        active_m = self.missions.get_active_mission()
        if not active_m:
            return

        self.ai_solve_in_progress = True
        self.ai_step_generator = self.autonomous_solver.solve_active_mission()
        self.status_text = "NOVA AI: Autonomous solving initiated. Watch the real-time search tree traversal..."
        self.status_bar.config(text=self.status_text)

    def _on_inventory_action(self):
        """Opens interactive Engineering Deck & Crafting Workbench."""
        top = tk.Toplevel(self.root)
        top.title("🎒 Engineering Inventory & Crafting Deck")
        top.geometry("540x420")
        top.configure(bg="#060F1E")

        tk.Label(top, text="🎒 ENGINEERING TOOL DECK & COMBINATIONS", font=("Helvetica", 11, "bold"), fg="#00E5FF", bg="#060F1E").pack(pady=10)

        items_listbox = tk.Listbox(top, selectmode=tk.MULTIPLE, font=("Helvetica", 9), bg="#101D33", fg="#FFFFFF", selectbackground="#00E5FF", selectforeground="#000000", height=8)
        items_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        for it in self.inventory.items:
            items_listbox.insert(tk.END, f"[{it.category}] {it.name} — {it.description[:45]}...")

        status_lbl = tk.Label(top, text="Select 2 items and click [Combine / Craft Tools]", font=("Helvetica", 9), fg="#FFD600", bg="#060F1E")
        status_lbl.pack(pady=5)

        def combine_selected():
            sel = items_listbox.curselection()
            if len(sel) != 2:
                messagebox.showwarning("Combine Items", "Please select exactly 2 items to combine.", parent=top)
                return
            it1 = self.inventory.items[sel[0]]
            it2 = self.inventory.items[sel[1]]
            succ, msg, res = self.inventory.combine_items(it1.item_id, it2.item_id)
            if succ:
                messagebox.showinfo("🛠️ Crafting Success!", f"COMBINATION SUCCESSFUL!\nCrafted: [{res.name}]\n\n{res.description}", parent=top)
                top.destroy()
                self._on_inventory_action()  # refresh
            else:
                messagebox.showerror("Crafting Incompatible", msg, parent=top)

        btn_f = tk.Frame(top, bg="#060F1E")
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="🛠️ [Combine / Craft Selected]", font=("Helvetica", 10, "bold"), bg="#76FF03", fg="#000000", command=combine_selected).grid(row=0, column=0, padx=8)
        tk.Button(btn_f, text="Close Deck", bg="#37474F", fg="#FFFFFF", command=top.destroy).grid(row=0, column=1, padx=8)

    def _close_puzzle_overlay(self):
        self.active_puzzle_overlay = None
        self.status_text = "Exited terminal interface. Returning to physical exploration."
        self.status_bar.config(text=self.status_text)

    def _trigger_door_open_animation(self):
        # Open door in world and trigger sparks
        self.world.unlock_door(Sector.AI_CORE_GARDEN, (24, 7))
        self._spawn_sparks(24 * self.tile_size + 19, 7 * self.tile_size + 19, "#76FF03", 20)

    def _open_voltage_balancer_dialog(self, m1: Mission01RestoreAICore):
        """Interactive Mini-Puzzle: Voltage Balancer UI."""
        top = tk.Toplevel(self.root)
        top.title("⚡ Power Cell Beta - Voltage Harmonizer")
        top.geometry("460x320")
        top.configure(bg="#0A1124")

        tk.Label(top, text="⚡ VOLTAGE HARMONIC BALANCER", font=("Helvetica", 12, "bold"), fg="#00E5FF", bg="#0A1124").pack(pady=10)
        lbl_info = tk.Label(top, text="Target: 120.0V (Standard Circuit Baseline)\nToggle step switches to eliminate harmonics.", font=("Helvetica", 9), fg="#B0BEC5", bg="#0A1124")
        lbl_info.pack(pady=4)

        volt_var = tk.StringVar(value=f"CURRENT OUTPUT: {m1.current_balanced_voltage:.1f} V")
        lbl_volt = tk.Label(top, textvariable=volt_var, font=("Courier", 14, "bold"), fg="#FFD600", bg="#14223C", padx=15, pady=8)
        lbl_volt.pack(pady=10)

        def make_toggle(sw_id, label_text):
            def toggle():
                succ, msg, v = m1.toggle_voltage_switch(sw_id)
                volt_var.set(f"CURRENT OUTPUT: {v:.1f} V")
                if succ:
                    lbl_volt.config(fg="#76FF03")
                    messagebox.showinfo("⚡ Harmonizer Locked", msg, parent=top)
                else:
                    lbl_volt.config(fg="#FFD600")
            return toggle

        btn_f = tk.Frame(top, bg="#0A1124")
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="[Switch 1: +15V]", font=("Helvetica", 9, "bold"), bg="#00E5FF", command=make_toggle("SW_1", "+15V")).grid(row=0, column=0, padx=5)
        tk.Button(btn_f, text="[Switch 2: +10V]", font=("Helvetica", 9, "bold"), bg="#00E5FF", command=make_toggle("SW_2", "+10V")).grid(row=0, column=1, padx=5)
        tk.Button(btn_f, text="[Switch 3: -5V]", font=("Helvetica", 9, "bold"), bg="#00E5FF", command=make_toggle("SW_3", "-5V")).grid(row=0, column=2, padx=5)

        tk.Button(top, text="Close Harmonizer", bg="#37474F", fg="#FFFFFF", command=top.destroy).pack(pady=10)

    def _open_cryo_valve_dialog(self, m1: Mission01RestoreAICore):
        """Interactive Mini-Puzzle: Cryo-Valve Venting UI."""
        top = tk.Toplevel(self.root)
        top.title("💨 Coolant Console #44 - Cryo-Vent System")
        top.geometry("460x320")
        top.configure(bg="#0A1124")

        tk.Label(top, text="💨 CRYOGENIC COOLANT MANIFOLD #44", font=("Helvetica", 12, "bold"), fg="#00E5FF", bg="#0A1124").pack(pady=10)
        tk.Label(top, text="Liquid nitrogen leak pooling in central sector (77K).\nOpen correct exhaust sequence to vent corridor.", font=("Helvetica", 9), fg="#B0BEC5", bg="#0A1124").pack(pady=4)

        status_var = tk.StringVar(value="CRYO STATUS: HAZARD ACTIVE (77 K)")
        lbl_status = tk.Label(top, textvariable=status_var, font=("Courier", 11, "bold"), fg="#FF1744", bg="#14223C", padx=15, pady=8)
        lbl_status.pack(pady=10)

        def make_valve_toggle(v_id):
            def toggle():
                succ, msg = m1.toggle_cryo_valve(v_id)
                if succ:
                    status_var.set("CRYO STATUS: VENTED & SAFE (285 K)")
                    lbl_status.config(fg="#76FF03")
                    messagebox.showinfo("💨 Cryo-Vent Success", msg, parent=top)
                else:
                    status_var.set("CRYO STATUS: COOLANT PRESSURE ELEVATED")
                    lbl_status.config(fg="#FF1744")
            return toggle

        btn_f = tk.Frame(top, bg="#0A1124")
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="[Toggle Valve A]", font=("Helvetica", 9, "bold"), bg="#2979FF", fg="#FFFFFF", command=make_valve_toggle("VALVE_A")).grid(row=0, column=0, padx=5)
        tk.Button(btn_f, text="[Toggle Valve B]", font=("Helvetica", 9, "bold"), bg="#2979FF", fg="#FFFFFF", command=make_valve_toggle("VALVE_B")).grid(row=0, column=1, padx=5)
        tk.Button(btn_f, text="[Toggle Valve C]", font=("Helvetica", 9, "bold"), bg="#2979FF", fg="#FFFFFF", command=make_valve_toggle("VALVE_C")).grid(row=0, column=2, padx=5)

        tk.Button(top, text="Close Console", bg="#37474F", fg="#FFFFFF", command=top.destroy).pack(pady=10)

    def _open_kavya_dialog(self, m1: Mission01RestoreAICore):
        """Interactive NPC Dialogue Tree Modal: Maintenance Subroutine KAVYA."""
        top = tk.Toplevel(self.root)
        top.title("🤖 Hologram Terminal — KAVYA Subroutine")
        top.geometry("540x420")
        top.configure(bg="#060F1E")

        tk.Label(top, text="🤖 KAVYA (MAINTENANCE HOLOGRAPHIC SUBROUTINE)", font=("Helvetica", 11, "bold"), fg="#00E5FF", bg="#060F1E").pack(pady=10)

        dialogue_var = tk.StringVar()
        lbl_dial = tk.Label(top, textvariable=dialogue_var, font=("Helvetica", 9), fg="#FFFFFF", bg="#101D33", padx=15, pady=12, wraplength=490, justify=tk.LEFT)
        lbl_dial.pack(fill=tk.X, padx=15, pady=10)

        choices_frame = tk.Frame(top, bg="#060F1E")
        choices_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        def render_dialogue_step(choice_id=None):
            for w in choices_frame.winfo_children():
                w.destroy()
            resp, choices = m1.interact_with_kavya(choice_id, self.inventory)
            dialogue_var.set(resp)

            for cid, ctext in choices:
                if cid == "CHOICE_EXIT":
                    btn = tk.Button(choices_frame, text=f"• {ctext}", font=("Helvetica", 9), bg="#37474F", fg="#FFFFFF", anchor="w", command=top.destroy)
                else:
                    btn = tk.Button(choices_frame, text=f"• {ctext}", font=("Helvetica", 9, "bold"), bg="#0D274D", fg="#00E5FF", anchor="w", command=lambda c=cid: render_dialogue_step(c))
                btn.pack(fill=tk.X, pady=3)

        render_dialogue_step(None)

    def _open_secret_vault_dialog(self, m1: Mission01RestoreAICore):
        """Secret Quantum Vault discovery modal."""
        top = tk.Toplevel(self.root)
        top.title("🔍 Secret Quantum Storage Vault")
        top.geometry("460x280")
        top.configure(bg="#060F1E")

        tk.Label(top, text="🔍 SECRET QUANTUM STORAGE VAULT", font=("Helvetica", 11, "bold"), fg="#FFD600", bg="#060F1E").pack(pady=10)

        if not m1.secret_vault_unlocked:
            tk.Label(top, text="Emergency cache protected by frequency lock.\nEnter access code (Discovered from KAVYA / Drone logs):", font=("Helvetica", 9), fg="#CFD8DC", bg="#060F1E").pack(pady=5)
            entry = tk.Entry(top, font=("Courier", 14, "bold"), justify="center")
            entry.insert(0, "488")
            entry.pack(pady=8)

            def unlock():
                code = entry.get().strip()
                if code == "488" or self.inventory.has_item("ITEM_LOGIC_PROBE"):
                    m1.secret_vault_unlocked = True
                    self.inventory.add_item(Item("ITEM_QUANTUM_CORE_SHARD", "Overcharged Quantum Cell", "Supercharges AI Core to 200% capacity.", category="TOOL"))
                    messagebox.showinfo("🎉 Vault Unlocked!", "Access granted! Acquired: [Overcharged Quantum Cell]!", parent=top)
                    top.destroy()
                else:
                    messagebox.showwarning("Security Lockout", "Incorrect override code. Probe required.", parent=top)

            tk.Button(top, text="[Unlock Vault]", font=("Helvetica", 10, "bold"), bg="#76FF03", command=unlock).pack(pady=6)
        else:
            tk.Label(top, text="Vault is already unlocked and empty.", font=("Helvetica", 9), fg="#76FF03", bg="#060F1E").pack(pady=15)

        tk.Button(top, text="Close", bg="#37474F", fg="#FFFFFF", command=top.destroy).pack(pady=10)

    def _on_canvas_click(self, event):
        """Handles clicking on nodes in the interactive circuit blueprint overlay."""
        if not self.active_puzzle_overlay:
            return

        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return

        # Check node positions on overlay
        ox, oy = 80, 80
        for nid, ninfo in m1.power_nodes.items():
            nx = ox + ninfo.pos[0] * 45
            ny = oy + ninfo.pos[1] * 40
            # Hit test circle radius 18
            if (event.x - nx)**2 + (event.y - ny)**2 <= 18**2:
                success, msg, data = m1.connect_next_node(nid, self.inventory)
                self.status_text = msg
                self.status_bar.config(text=self.status_text)

                if success:
                    self._spawn_sparks(nx, ny, "#00E5FF", 12)
                    if data.get("ready_for_moral_decision"):
                        self._spawn_sparks(nx, ny, "#E040FB", 25)
                        self._open_final_moral_decision_dialog(m1)
                    elif data.get("completed"):
                        sol_type = data.get("solution_type", "OPTIMAL")
                        self._spawn_sparks(nx, ny, "#E040FB", 30)
                        self._trigger_door_open_animation()
                        debrief = m1.generate_post_mission_debrief(self.player.stats)
                        messagebox.showinfo(f"🎉 Mission 1 Complete ({sol_type} Ending)", f"{msg}\n\n{debrief}")
                        self.active_puzzle_overlay = None
                else:
                    self._spawn_sparks(nx, ny, "#FF1744", 20)
                    self.player.health = max(0, self.player.health - 20)
                    self.player.stats.record_mistake("Connected through flooded cryogenic node")
                    try:
                        self.root.bell()
                    except Exception:
                        pass
                break

    def _open_final_moral_decision_dialog(self, m1: Mission01RestoreAICore):
        """Interactive Final Moral Choice Dialog at Central AI Core Console."""
        top = tk.Toplevel(self.root)
        top.title("💎 Central AI Core — Final Moral Resolution")
        top.geometry("620x480")
        top.configure(bg="#050C1C")

        tk.Label(top, text="💎 CENTRAL AI CORE MASTER CONSOLE", font=("Helvetica", 12, "bold"), fg="#E040FB", bg="#050C1C").pack(pady=10)
        lbl_msg = tk.Label(top, text=(
            "Superconducting current has synchronized with the NEXUS Core Crystal.\n"
            "AEGIS AI and NOVA await your final architectural command:\n"
            "Will you awaken the AI, isolate it in quarantine, or synthesize their neural subnets?"
        ), font=("Helvetica", 9), fg="#CFD8DC", bg="#050C1C", justify=tk.CENTER)
        lbl_msg.pack(pady=6)

        def make_decision(choice_key):
            succ, end_msg, res = m1.execute_final_moral_decision(choice_key)
            self._trigger_door_open_animation()
            debrief = m1.generate_post_mission_debrief(self.player.stats)
            top.destroy()
            self.active_puzzle_overlay = None
            messagebox.showinfo(f"🎉 Mission 1 Resolution — {choice_key}", f"{end_msg}\n\n{debrief}")

        btn_f = tk.Frame(top, bg="#050C1C")
        btn_f.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Choice 1: Restore
        b1 = tk.Button(btn_f, text="[1. RESTORE: Full Unfettered AI Awakening]\nChannel 100% power to awaken NEXUS Prime. Unlocks Cryo-Grid Stability Shield.",
                       font=("Helvetica", 9, "bold"), bg="#005A9E", fg="#00E5FF", anchor="w", justify=tk.LEFT,
                       command=lambda: make_decision("RESTORE"))
        b1.pack(fill=tk.X, pady=6)

        # Choice 2: Contain
        b2 = tk.Button(btn_f, text="[2. CONTAIN: Sandbox Quarantine Buffer]\nIsolate AI Core in sandbox quarantine. AEGIS compliant. Unlocks Tactical Nanoweave.",
                       font=("Helvetica", 9, "bold"), bg="#4A0007", fg="#FF5252", anchor="w", justify=tk.LEFT,
                       command=lambda: make_decision("CONTAIN"))
        b2.pack(fill=tk.X, pady=6)

        # Choice 3: Merge
        b3 = tk.Button(btn_f, text="[3. MERGE: Neural Synthesis (NOVA + AEGIS)]\nHarmonize empathetic and security subnets. Unlocks Synthesized Neural Core (+30 NRG).",
                       font=("Helvetica", 9, "bold"), bg="#311B92", fg="#E040FB", anchor="w", justify=tk.LEFT,
                       command=lambda: make_decision("MERGE"))
        b3.pack(fill=tk.X, pady=6)

    def _update_hud(self):
        profile = self.ml_pipeline.update_live_profile()
        active_m = self.missions.get_active_mission()
        assessment = profile.get("assessment", {})
        threat_meter = assessment.get("threat_meter", "████░░░░░░")
        threat_desc = assessment.get("threat_desc", "NOMINAL")

        self.telemetry_txt.set(
            f"AGENT       : {self.player.name[:18]}\n"
            f"PROFILE     : {profile['archetype']}\n"
            f"THREAT LEVEL: [{threat_meter}]\n"
            f"STATUS      : {threat_desc}\n"
            f"EXPLORATION : {self.player.stats.steps_taken} steps\n"
            f"ANOMALIES   : {self.player.stats.mistakes_count} alerts\n"
            f"VITAL SIGNS : HP {self.player.health}% | NRG {self.player.energy}%"
        )

        if active_m:
            self.mission_txt.set(
                f"MISSION: {active_m.title}\n\n"
                f"SECTOR : {active_m.sector_name}\n"
                f"SYSTEM : {active_m.algorithm_concept}\n"
                f"STATUS : {active_m.status.value}\n\n"
                f"NOVA ADVISORY:\n\"{assessment.get('nova_recommendation', 'Inspect nearby relays.')}\""
            )

    def _render_canvas(self):
        self.canvas.delete("all")
        s_map = self.world.get_current_map()
        grid = s_map.grid
        ts = self.tile_size

        # Render Tiles
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                px = x * ts
                py = y * ts

                if tile == TileType.WALL:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#121A2C", outline="#1E2A44", width=1)
                elif tile == TileType.FLOOR:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#070B14", outline="#0E1626", width=1)
                elif tile == TileType.DOOR_LOCKED:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#D50000", outline="#FF1744", width=2)
                    self.canvas.create_text(px+ts/2, py+ts/2, text="🔒", font=("Arial", 12))
                elif tile == TileType.DOOR_UNLOCKED:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#00C853", outline="#69F0AE", width=2)
                    self.canvas.create_text(px+ts/2, py+ts/2, text="🔓", font=("Arial", 12))
                elif tile == TileType.HAZARD:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#3E1018", outline="#FF1744", width=1)
                    # Flashing hazard warning
                    if (self.anim_tick // 10) % 2 == 0:
                        self.canvas.create_text(px+ts/2, py+ts/2, text="⚠️", font=("Arial", 11))
                elif tile == TileType.TERMINAL:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#005A9E", outline="#00E5FF", width=2)
                    self.canvas.create_text(px+ts/2, py+ts/2, text="🖥️", font=("Arial", 13))
                elif tile == TileType.POWER_NODE:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#FF6D00", outline="#FFD600", width=2)
                    self.canvas.create_text(px+ts/2, py+ts/2, text="⚡", font=("Arial", 13))
                elif tile == TileType.AI_CORE:
                    # Pulsing AI Core energy
                    pulse_val = abs(math.sin(self.anim_tick * 0.1)) * 6
                    self.canvas.create_oval(px-pulse_val, py-pulse_val, px+ts+pulse_val, py+ts+pulse_val, fill="#4A148C", outline="#E040FB", width=2)
                    self.canvas.create_text(px+ts/2, py+ts/2, text="💎", font=("Arial", 16))
                elif tile == TileType.SERVER_RACK:
                    self.canvas.create_rectangle(px, py, px+ts, py+ts, fill="#006064", outline="#00E5FF", width=1)
                    self.canvas.create_text(px+ts/2, py+ts/2, text="🖧", font=("Arial", 12))

        # Proximity interaction badge over nearby machine
        target_info = self.player.check_interaction_target(self.world)
        if target_info:
            tpos, _ = target_info
            tx, ty = tpos[0] * ts, tpos[1] * ts
            self.canvas.create_rectangle(tx-10, ty-22, tx+ts+10, ty-4, fill="#00E5FF", outline="#FFFFFF")
            self.canvas.create_text(tx+ts/2, ty-13, text="[E] INTERACT", font=("Helvetica", 8, "bold"), fill="#000000")

        # Render Sparks / Particles
        for p in self.particles:
            r = max(1.0, (p.life / p.max_life) * 3.0)
            self.canvas.create_oval(p.x-r, p.y-r, p.x+r, p.y+r, fill=p.color, outline="")

        # Render Player Robot Avatar
        px = self.player.x * ts
        py = self.player.y * ts
        self.canvas.create_oval(px+2, py+2, px+ts-2, py+ts-2, fill="#00E5FF", outline="#FFFFFF", width=2)
        self.canvas.create_text(px+ts/2, py+ts/2, text="🤖", font=("Arial", 15))

        # NOVA Companion hovering adjacent
        nova_offset_x = math.cos(self.anim_tick * 0.15) * 12
        nova_offset_y = math.sin(self.anim_tick * 0.15) * 12
        self.canvas.create_oval(px+ts+nova_offset_x-5, py+nova_offset_y-5, px+ts+nova_offset_x+5, py+nova_offset_y+5, fill="#76FF03", outline="#FFFFFF", width=1)

        # RENDER INTERACTIVE CIRCUIT OVERLAY IF ACTIVE
        if self.active_puzzle_overlay == "M01":
            self._render_mission01_circuit_overlay()

    def _render_mission01_circuit_overlay(self):
        """Draws the visual Mission 1 Power Grid Blueprint right on the canvas."""
        m1: Mission01RestoreAICore = self.missions.get_mission("M01")
        if not m1:
            return

        # Dark translucent overlay backdrop
        self.canvas.create_rectangle(40, 30, 840, 540, fill="#050C1C", outline="#00E5FF", width=3)
        self.canvas.create_text(440, 55, text="⚡ MISSION 1: SUPERCONDUCTING POWER GRID CALIBRATION", font=("Helvetica", 12, "bold"), fill="#00E5FF")
        self.canvas.create_text(440, 75, text="Click reachable nodes to connect cable from Relay Alpha to Central AI Core. Avoid cryogenic leaks!", font=("Helvetica", 9), fill="#CFD8DC")

        ox, oy = 80, 110

        # Draw Conduit Wires
        for u, v in m1.connections:
            nu = m1.power_nodes[u]
            nv = m1.power_nodes[v]
            ux, uy = ox + nu.pos[0] * 45, oy + nu.pos[1] * 38
            vx, vy = ox + nv.pos[0] * 45, oy + nv.pos[1] * 38

            # If cable is connected between u and v
            is_active = (u in m1.connected_route and v in m1.connected_route and
                         abs(m1.connected_route.index(u) - m1.connected_route.index(v)) == 1)
            line_color = "#00E5FF" if is_active else "#1A2E50"
            line_w = 4 if is_active else 2
            self.canvas.create_line(ux, uy, vx, vy, fill=line_color, width=line_w)

            # Animated glowing electricity pulse traveling along active cables
            if is_active:
                pulse_t = (self.anim_tick * 0.08) % 1.0
                pulse_x = ux + (vx - ux) * pulse_t
                pulse_y = uy + (vy - uy) * pulse_t
                self.canvas.create_oval(pulse_x-4, pulse_y-4, pulse_x+4, pulse_y+4, fill="#FFFFFF", outline="#00E5FF", width=2)

        # Draw Nodes
        avail_nodes = m1.get_available_next_nodes()
        for nid, ninfo in m1.power_nodes.items():
            nx = ox + ninfo.pos[0] * 45
            ny = oy + ninfo.pos[1] * 38

            if ninfo.is_hazard:
                node_fill = "#D50000" if nid in avail_nodes else "#4A0007"
                node_out = "#FF1744"
                label_icon = "⚠️"
            elif nid in m1.connected_route:
                node_fill = "#00E5FF"
                node_out = "#FFFFFF"
                label_icon = "⚡"
            elif nid in avail_nodes:
                # Pulsing target glow
                pulse_w = 2 + int(abs(math.sin(self.anim_tick * 0.2)) * 3)
                node_fill = "#FFD600"
                node_out = "#FFFF00"
                label_icon = "🔗"
            else:
                node_fill = "#14223C"
                node_out = "#2A3F66"
                label_icon = "○"

            r = 18
            self.canvas.create_oval(nx-r, ny-r, nx+r, ny+r, fill=node_fill, outline=node_out, width=2)
            self.canvas.create_text(nx, ny, text=label_icon, font=("Arial", 10))
            self.canvas.create_text(nx, ny+25, text=f"{nid}: {ninfo.name[:12]}", font=("Helvetica", 8, "bold"), fill="#E0E6ED")

        # Instructions / Exit Hint
        self.canvas.create_text(440, 515, text="[Click Yellow Node to Wire Cable]  •  [Press ESC to Close Terminal]", font=("Helvetica", 9, "bold"), fill="#FFD600")

    def run(self):
        self.root.mainloop()
