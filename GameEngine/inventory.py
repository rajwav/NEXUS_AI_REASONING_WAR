"""
NEXUS AI REASONING WAR - Player Inventory & Item Combination System
Manages items, equipment, forensic evidence, and multi-component crafting/combinations.
"""

from typing import Dict, List, Optional, Tuple, Any
from .objects import Item


class Inventory:
    """Manages player items, capacity, and item combinations."""
    def __init__(self, capacity: int = 12):
        self.capacity = capacity
        self.items: List[Item] = []
        self._combination_recipes: Dict[Tuple[str, str], Item] = {}
        self._init_default_recipes()

    def _init_default_recipes(self):
        """Predefined engineering item combination recipes."""
        # Logic Probe + Cryo Stabilizer -> Superconducting Shunt
        self.register_recipe(
            "ITEM_LOGIC_PROBE", "ITEM_CRYO_STABILIZER",
            Item("ITEM_SUPERCONDUCTING_SHUNT", "Superconducting Cryo-Shunt",
                 "Eliminates thermal resistance, allowing zero-damage routing through flooded liquid nitrogen nodes.",
                 category="TOOL")
        )

        # Optic Lens + Spectrometer -> Optical Decoder
        self.register_recipe(
            "ITEM_OPTIC_LENS", "ITEM_SPECTROMETER",
            Item("ITEM_OPTICAL_DECODER", "AEGIS Optical Decoder",
                 "Decodes encrypted laser override frequencies and secret access codes.",
                 category="TOOL")
        )

        # Logic Probe + Raw Cryo-Crystal -> Superconducting Logic Probe
        self.register_recipe(
            "ITEM_LOGIC_PROBE", "ITEM_CRYO_CRYSTAL",
            Item("ITEM_SUPERCONDUCTING_PROBE", "Superconducting Logic Probe",
                 "High-frequency probe capable of analyzing quantum state superposition circuits.",
                 category="TOOL")
        )

        # Forensic Drive + Cryptographic Key -> Decrypted Forensic Ledger
        self.register_recipe(
            "ITEM_ENCRYPTED_USB", "ITEM_CRYPTO_KEY",
            Item("ITEM_DECRYPTED_LEDGER", "Decrypted Forensic Ledger",
                 "Contains unredacted timestamped biometric logs and unauthorized terminal commands.",
                 category="EVIDENCE")
        )

        # Optical Prism + Frequency Filter -> Quantum Polarizer
        self.register_recipe(
            "ITEM_OPTICAL_PRISM", "ITEM_FREQUENCY_FILTER",
            Item("ITEM_QUANTUM_POLARIZER", "Harmonic Quantum Polarizer",
                 "Calibrates CSP laser emitters to prevent frequency interference.",
                 category="TOOL")
        )

    def register_recipe(self, item_id_a: str, item_id_b: str, result_item: Item):
        key1 = (item_id_a, item_id_b)
        key2 = (item_id_b, item_id_a)
        self._combination_recipes[key1] = result_item
        self._combination_recipes[key2] = result_item

    def add_item(self, item: Item) -> Tuple[bool, str]:
        if len(self.items) >= self.capacity:
            return False, "Inventory is full! (Max 12 items)"
        self.items.append(item)
        return True, f"Acquired item: [{item.name}]"

    def remove_item(self, item_id: str) -> Optional[Item]:
        for i, item in enumerate(self.items):
            if item.item_id == item_id:
                return self.items.pop(i)
        return None

    def has_item(self, item_id: str) -> bool:
        return any(item.item_id == item_id for item in self.items)

    def get_item(self, item_id: str) -> Optional[Item]:
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def combine_items(self, item_id_a: str, item_id_b: str) -> Tuple[bool, str, Optional[Item]]:
        if not self.has_item(item_id_a) or not self.has_item(item_id_b):
            return False, "You do not have both items to combine.", None

        recipe_key = (item_id_a, item_id_b)
        if recipe_key not in self._combination_recipes:
            return False, "These items cannot be combined.", None

        result_item = self._combination_recipes[recipe_key]
        self.remove_item(item_id_a)
        self.remove_item(item_id_b)
        self.add_item(result_item)
        return True, f"Successfully combined items into: [{result_item.name}]!", result_item

    def list_items_summary(self) -> List[str]:
        return [f"[{i+1}] {item.name} ({item.category})" for i, item in enumerate(self.items)]
