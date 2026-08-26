"""
Unit Tests - NEXUS Missions (10 Playable Challenges)
Tests Human Interactive Solving and NOVA AI Autonomous Solving for all 10 missions.
"""

import unittest
from GameEngine.player import Player
from GameEngine.inventory import Inventory
from GameEngine.objects import Item
from GameEngine.events import EventBus
from GameEngine.missions import MissionManager, MissionStatus
from Missions.m01_restore_ai_core import Mission01RestoreAICore
from AI_Algorithms.minimax import CombatAction


class TestMissions(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.inventory = Inventory()
        self.bus = EventBus()
        self.manager = MissionManager(self.player, self.inventory, self.bus)

    def test_mission_01_restore_ai_core(self):
        m: Mission01RestoreAICore = self.manager.get_mission("M01")
        self.assertIsNotNone(m)

        # 0. Test Voltage Balancer Mini-Puzzle
        m.toggle_voltage_switch("SW_1")  # +15V -> 110V
        m.toggle_voltage_switch("SW_2")  # +10V -> 120V
        self.assertTrue(m.is_voltage_balanced)
        self.assertEqual(m.current_balanced_voltage, 120.0)

        # 1. Test Fast Route: N0 -> N5 -> N8 -> N9
        m.connected_route = ["N0"]
        m.status = MissionStatus.ACTIVE
        m.connect_next_node("N5", self.inventory)
        m.connect_next_node("N8", self.inventory)
        success_fast, msg_fast, data_fast = m.connect_next_node("N9", self.inventory)
        self.assertTrue(success_fast)
        self.assertTrue(data_fast.get("ready_for_moral_decision"))
        
        # Test executing moral decision RESTORE
        succ_dec, msg_dec, res_dec = m.execute_final_moral_decision("RESTORE")
        self.assertTrue(succ_dec)
        self.assertEqual(res_dec.get("decision"), "RESTORE")
        self.assertEqual(m.status, MissionStatus.COMPLETED)

        # 1b. Test Cryo-Valve Venting Mini-Puzzle
        m.toggle_cryo_valve("VALVE_A")
        m.toggle_cryo_valve("VALVE_C")
        self.assertTrue(m.cryo_vented_safe)
        self.assertFalse(m.power_nodes["N6"].is_hazard)

        # 2. Test Safe Route & CONTAIN decision
        m.connected_route = ["N0"]
        m.status = MissionStatus.ACTIVE
        for nid in ["N1", "N2", "N3", "N4", "N8", "N9"]:
            m.connect_next_node(nid, self.inventory)
        succ_contain, _, res_contain = m.execute_final_moral_decision("CONTAIN")
        self.assertTrue(succ_contain)
        self.assertEqual(res_contain.get("decision"), "CONTAIN")

        # 3. Test Experimental Route with Logic Probe & MERGE decision
        self.inventory.add_item(Item("ITEM_LOGIC_PROBE", "Standard Logic Probe", "Test tool", category="TOOL"))
        m.connected_route = ["N0"]
        m.status = MissionStatus.ACTIVE
        for nid in ["N6", "N4", "N8", "N9"]:
            m.connect_next_node(nid, self.inventory)
        succ_merge, _, res_merge = m.execute_final_moral_decision("MERGE")
        self.assertTrue(succ_merge)
        self.assertEqual(res_merge.get("decision"), "MERGE")

        # 4. Test Autonomous AI Solve
        steps = list(m.solve_autonomous_ai())
        self.assertTrue(len(steps) > 0)
        self.assertEqual(m.status, MissionStatus.COMPLETED)
        self.assertTrue(m.is_solved_by_ai)

    def test_mission_02_traitor_scientist(self):
        m = self.manager.get_mission("M02")
        facts = ["badge_at_core_0214", "core_disabled_0214", "root_override_used", "data_extracted_to_usb"]
        success, msg, data = m.solve_interactive_human("Dr. Rahul Verma", facts)
        self.assertTrue(success)
        self.assertEqual(m.status, MissionStatus.COMPLETED)

    def test_mission_03_quantum_lock(self):
        m = self.manager.get_mission("M03")
        # Valid assignment: A=1, B=2, C=4, D=1, E=2 -> A+C=5, E>A, A!=B, B!=C, C!=D, D!=E, B!=D
        assignment = {"Emitter_A": 1, "Emitter_B": 2, "Emitter_C": 4, "Emitter_D": 1, "Emitter_E": 2}
        success, msg, data = m.solve_interactive_human(assignment)
        self.assertTrue(success)

    def test_mission_04_defeat_training_ai(self):
        m = self.manager.get_mission("M04")
        state = m.create_initial_combat_state()
        next_state, msg, stats = m.execute_turn(state, CombatAction.ATTACK)
        self.assertIsNotNone(next_state)

    def test_mission_05_stop_malware(self):
        m = self.manager.get_mission("M05")
        steps = list(m.solve_autonomous_ai())
        self.assertTrue(len(steps) > 0)
        self.assertEqual(m.status, MissionStatus.COMPLETED)

    def test_mission_06_recover_memory(self):
        m = self.manager.get_mission("M06")
        success, msg, data = m.solve_interactive_human(m.required_triples)
        self.assertTrue(success)

    def test_mission_07_ai_ethics_dilemma(self):
        m = self.manager.get_mission("M07")
        success, msg, data = m.solve_interactive_human("OPT_HARMONIC_SHUNT")
        self.assertTrue(success)

    def test_mission_08_robot_escape(self):
        m = self.manager.get_mission("M08")
        seq = ["hack_safe_with_probe", "activate_generator", "unlock_airlock_door", "evacuate_drone"]
        success, msg, data = m.solve_interactive_human(seq)
        self.assertTrue(success)

    def test_mission_09_adaptive_ai_test(self):
        m = self.manager.get_mission("M09")
        success, msg, data = m.solve_interactive_human([(0.1, 0.8), (0.2, 0.85), (0.3, 0.9)])
        self.assertTrue(success)

    def test_mission_10_final_nexus_core(self):
        m = self.manager.get_mission("M10")
        inputs = {
            "phase1_path": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
            "phase2_csp": {"Alpha": 3, "Beta": 4, "Gamma": 5},
            "phase3_auth": "NEXUS_ROOT_2088",
            "phase4_action": "CONSENSUS_HARMONIC_EQUILIBRIUM"
        }
        success, msg, data = m.solve_interactive_human(inputs)
        self.assertTrue(success)
        self.assertEqual(m.status, MissionStatus.COMPLETED)


if __name__ == "__main__":
    unittest.main()
