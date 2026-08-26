"""
NEXUS AI REASONING WAR - Mission 6: Recover Lost Memory
Algorithm Concept: Knowledge Representation & Semantic Networks / Ontologies
Sector: AI Core Garden
Gameplay: Reconstruct fragmented neural ontologies by linking nodes via semantic relations
(is_a, part_of, requires, causes).
"""

from typing import List, Tuple, Dict, Optional, Any, Generator
from .mission_base import MissionBase, MissionStatus
from GameEngine.objects import Item


class SemanticTriple:
    def __init__(self, subject: str, predicate: str, obj: str):
        self.subject = subject
        self.predicate = predicate
        self.obj = obj

    def to_tuple(self) -> Tuple[str, str, str]:
        return (self.subject, self.predicate, self.obj)


class Mission06RecoverMemory(MissionBase):
    def __init__(self):
        super().__init__(
            mission_id="M06",
            title="Recover Fragmented Neural Memory",
            sector_name="Sector 1: AI Core Garden",
            algorithm_concept="Knowledge Representation & Semantic Ontological Graphs",
            description="NOVA's long-term memory matrix is scrambled. Reconstruct the semantic ontology triples connecting AI concepts (is_a, part_of, requires, causes) to restore cognitive coherence."
        )
        self.required_triples = [
            ("A_Star_Search", "is_a", "Heuristic_Algorithm"),
            ("Heuristic_Algorithm", "is_a", "Informed_Search"),
            ("A_Star_Search", "requires", "Admissible_Heuristic"),
            ("Admissible_Heuristic", "causes", "Optimal_Pathfinding"),
            ("Minimax", "is_a", "Adversarial_Search"),
            ("Alpha_Beta_Pruning", "part_of", "Minimax"),
            ("Alpha_Beta_Pruning", "causes", "Reduced_Search_Space")
        ]
        self.clues_found = [
            "Ontology rule: An admissible heuristic guarantees optimal pathfinding without overestimating distance.",
            "Concept hierarchy: A* Search is an instance of Heuristic Algorithm, which belongs to Informed Search.",
            "Game tree structure: Alpha-Beta Pruning is a branch reduction technique inside Minimax."
        ]
        self.reward_items = [
            Item("ITEM_NEURAL_COGNITION_KEY", "NOVA Cognition Key",
                 "Unlocks NOVA's advanced predictive intuition and multi-step lookahead.",
                 category="TOOL")
        ]

    def solve_interactive_human(self, submitted_triples: List[Tuple[str, str, str]]) -> Tuple[bool, str, Dict[str, Any]]:
        """Human player submits assembled semantic triples."""
        submitted_set = set(submitted_triples)
        expected_set = set(self.required_triples)

        matching = submitted_set.intersection(expected_set)
        accuracy = len(matching) / len(expected_set)

        if accuracy >= 0.85:
            self.complete(solved_by_ai=False)
            return True, (
                f"NEURAL MEMORY MATRIX RECONSTRUCTED!\n"
                f"Assembled {len(matching)}/{len(expected_set)} correct semantic ontological relationships.\n"
                "NOVA's episodic memory restored to nominal capacity. Cognition Key acquired!"
            ), {"accuracy": accuracy, "triples": list(matching)}
        else:
            return False, (
                f"Semantic dissonance detected. Only {len(matching)}/{len(expected_set)} triples correct. "
                "Review ontology inheritance and causal links."
            ), {"accuracy": accuracy}

    def solve_autonomous_ai(self) -> Generator[Dict[str, Any], None, None]:
        yield {
            "status": "NOVA_INIT",
            "message": "NOVA AI: Parsing knowledge graph triples and resolving semantic taxonomy..."
        }

        for i, triple in enumerate(self.required_triples):
            yield {
                "status": "TRIPLE_ALIGNED",
                "step": i + 1,
                "triple": triple,
                "message": f"Semantic link verified: ({triple[0]}) --[{triple[1]}]--> ({triple[2]})."
            }

        self.complete(solved_by_ai=True)
        yield {
            "status": "ONTOLOGY_COMPLETE",
            "message": "NOVA: Full ontological knowledge base re-indexed successfully."
        }
