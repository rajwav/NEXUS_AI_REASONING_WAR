"""
NEXUS AI REASONING WAR - Mission 2: Digital Crime Investigation
Algorithm Concept: Knowledge Representation & Forward Chaining
Sector: Digital Forensic Lab
Gameplay: Analyze timestamps, badge scans, and encrypted terminal logs to deduce
the traitor scientist who triggered the containment cascade.
"""

from typing import List, Tuple, Dict, Optional, Any, Generator, Set
from .mission_base import MissionBase, MissionStatus
from AI_Algorithms.forward_chaining import ForwardChainingEngine, Fact, Rule
from GameEngine.objects import Item


class Mission02TraitorScientist(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M02",
            title="Digital Crime Investigation: The Rogue Scientist",
            sector_name="Sector 4: Digital Forensic Lab",
            algorithm_concept="Knowledge Representation & Forward Chaining Logic",
            description="The core shutdown was an act of deliberate sabotage. Cross-reference biometric badge logs, surveillance timestamps, and server exports to deduce the culprit."
        )
        self.clues_found = [
            "Log 01: Dr. Rahul Verma badge scanned in AI Core Garden at 02:14 AM.",
            "Log 02: Prof. Meera Iyer was logged at Quantum Security Lab running cryo-stabilization at 02:15 AM.",
            "Log 03: Ananya Rao was authorized at Forensic Terminal compiling neural snapshots at 02:10 AM.",
            "Log 04: AI Core containment failsafe was manually disabled from an internal terminal at 02:14 AM.",
            "Log 05: Unencrypted neural weights were downloaded to an external USB drive using Dr. Rahul Verma's root override.",
            "Log 06: Surveillance footage shows Dr. Rahul Verma left the campus perimeter at 02:22 AM."
        ]
        self.rules: List[Rule] = [
            Rule("R1", ["badge_at_core_0214", "core_disabled_0214"], "suspect_present_at_sabotage",
                 "If a scientist was badged in AI Core at 02:14 when containment was disabled, they are physically implicated."),
            Rule("R2", ["suspect_present_at_sabotage", "root_override_used"], "deliberate_sabotage_verified",
                 "If suspect was present and used root override, the action was unauthorized deliberate sabotage."),
            Rule("R3", ["deliberate_sabotage_verified", "data_extracted_to_usb"], "traitor_identified_rahul_verma",
                 "If deliberate sabotage and USB exfiltration are linked to the same session, Dr. Rahul Verma is the rogue actor.")
        ]
        self.reward_items = [
            Item("ITEM_CRYPTO_KEY", "Forensic Decryption Key",
                 "Decryption cipher retrieved from Dr. Rahul's abandoned workspace.",
                 category="TOOL"),
            Item("KEY_SECURITY_LV2", "Purple Security Keycard (Level 2)",
                 "Unlocks Robot Training Arena and Network Control Center corridors.",
                 category="KEYCARD")
        ]

    def solve_interactive_human(self, selected_suspect: str, selected_fact_keys: List[str]) -> Tuple[bool, str, Dict[str, Any]]:
        """Human selects facts and names the suspect."""
        expected_facts = {"badge_at_core_0214", "core_disabled_0214", "root_override_used", "data_extracted_to_usb"}
        provided = set(selected_fact_keys)

        engine = ForwardChainingEngine()
        for r in self.rules:
            engine.add_rule(r)
        for f in provided:
            engine.add_fact(Fact(f))

        deduced = engine.infer()

        if "traitor_identified_rahul_verma" in deduced and selected_suspect.strip().lower() in ["dr. rahul verma", "rahul verma", "rahul"]:
            self.complete(solved_by_ai=False)
            return True, (
                "INVESTIGATION RESOLVED!\n"
                "Inference Chain Validated:\n"
                "  1. Presence at Core (02:14) + Sabotage Event -> Suspect Implicated\n"
                "  2. Suspect Implicated + Root Override -> Deliberate Sabotage\n"
                "  3. Deliberate Sabotage + USB Download -> Dr. Rahul Verma Confirmed Rogue Actor!\n"
                "Level 2 Keycard and Decryption Key retrieved!"
            ), {"deduced_facts": list(deduced), "suspect": "Dr. Rahul Verma"}
        else:
            return False, (
                "CONTRADICTION DETECTED: The selected evidence does not logically satisfy "
                "the forward chaining rules to prove culprit culpability beyond reasonable doubt."
            ), {"deduced_facts": list(deduced)}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        """NOVA builds the logic graph and fires forward chaining rules."""
        engine = ForwardChainingEngine(
            initial_facts=[
                Fact("badge_at_core_0214", description="Dr. Rahul Verma badged into Core at 02:14 AM"),
                Fact("core_disabled_0214", description="Containment failsafe manually overridden at 02:14 AM"),
                Fact("root_override_used", description="Root override cipher executed during session"),
                Fact("data_extracted_to_usb", description="Neural weights written to unauthorized USB drive")
            ],
            rules=self.rules
        )

        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Injecting forensic facts into Forward Chaining Rule Engine..."
        }

        for step in engine.infer_stepper():
            yield step

        self.complete(solved_by_ai=True)
