"""
NEXUS AI REASONING WAR - K-Means Player Archetype Classifier
Pure Python K-Means clustering classifying real-time telemetry into:
Explorer, Strategist, Hacker, and Beginner.
"""

from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
import math
import random
import json


class PlayerArchetype(Enum):
    EXPLORER = "EXPLORER"      # High exploration, visits all nodes, curious
    STRATEGIST = "STRATEGIST"  # Highly analytical, minimal errors, calculates moves
    HACKER = "HACKER"          # Aggressive, high speed, takes risks, direct terminal hacks
    BEGINNER = "BEGINNER"      # Needs guidance, higher error rate, relies on hints/NOVA


class KMeansAnalyzer:
    """
    K-Means clustering algorithm trained on player telemetry vectors:
    [Velocity, Error Rate, Hint Dependency, Risk Index, Autonomy Ratio]
    """
    def __init__(self, k: int = 4):
        self.k = k
        self.archetype_labels = [
            PlayerArchetype.EXPLORER,
            PlayerArchetype.STRATEGIST,
            PlayerArchetype.HACKER,
            PlayerArchetype.BEGINNER
        ]
        # Pre-calibrated initial cluster centroids
        self.centroids: List[List[float]] = [
            [0.85, 0.20, 0.15, 0.25, 0.80],  # Explorer
            [0.35, 0.05, 0.10, 0.10, 0.95],  # Strategist
            [0.90, 0.35, 0.05, 0.75, 0.85],  # Hacker
            [0.40, 0.65, 0.70, 0.40, 0.30]   # Beginner
        ]

    def _euclidean_distance(self, v1: List[float], v2: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def fit(self, dataset: List[List[float]], max_iters: int = 100):
        """Fits K-Means centroids on telemetry data."""
        if not dataset or len(dataset) < self.k:
            return

        # Randomly initialize if dataset is large enough
        indices = random.sample(range(len(dataset)), self.k)
        self.centroids = [list(dataset[i]) for i in indices]

        for _ in range(max_iters):
            clusters: List[List[List[float]]] = [[] for _ in range(self.k)]
            for vec in dataset:
                best_c = min(range(self.k), key=lambda i: self._euclidean_distance(vec, self.centroids[i]))
                clusters[best_c].append(vec)

            new_centroids = []
            changed = False
            for i in range(self.k):
                if clusters[i]:
                    mean_vec = [sum(dim) / len(clusters[i]) for dim in zip(*clusters[i])]
                    new_centroids.append(mean_vec)
                    if self._euclidean_distance(mean_vec, self.centroids[i]) > 1e-4:
                        changed = True
                else:
                    new_centroids.append(self.centroids[i])

            self.centroids = new_centroids
            if not changed:
                break

    def predict(self, feature_vector: List[float]) -> Tuple[PlayerArchetype, float, Dict[str, float]]:
        """
        Classifies player telemetry vector and returns predicted Archetype,
        confidence score, and distance breakdown to each centroid.
        """
        distances = [self._euclidean_distance(feature_vector, c) for c in self.centroids]
        best_idx = min(range(self.k), key=lambda i: distances[i])
        
        # Softmax-style confidence from inverse distances
        inv_dists = [1.0 / max(1e-5, d) for d in distances]
        sum_inv = sum(inv_dists)
        probabilities = [inv / sum_inv for inv in inv_dists]

        archetype = self.archetype_labels[best_idx]
        confidence = probabilities[best_idx]

        dist_dict = {
            self.archetype_labels[i].value: round(probabilities[i], 3)
            for i in range(self.k)
        }

        return archetype, round(confidence, 3), dist_dict

    def get_gameplay_modifiers(self, archetype: PlayerArchetype) -> Dict[str, Any]:
        """Provides dynamic gameplay adaptations based on player profile."""
        if archetype == PlayerArchetype.EXPLORER:
            return {
                "nova_dialogue_style": "Curious & Lore-Enriched",
                "bonus_secret_clues": True,
                "hint_verbosity": "Medium",
                "enemy_aggression": "Standard"
            }
        elif archetype == PlayerArchetype.STRATEGIST:
            return {
                "nova_dialogue_style": "Concise & Analytical",
                "bonus_secret_clues": False,
                "hint_verbosity": "Low / Formulaic",
                "enemy_aggression": "High Tactical"
            }
        elif archetype == PlayerArchetype.HACKER:
            return {
                "nova_dialogue_style": "High-Tech & Cyber-Focused",
                "bonus_secret_clues": True,
                "hint_verbosity": "Cryptic",
                "enemy_aggression": "Counter-intrusion Heavy"
            }
        else:  # BEGINNER
            return {
                "nova_dialogue_style": "Encouraging & Instructive",
                "bonus_secret_clues": True,
                "hint_verbosity": "High / Step-by-Step",
                "enemy_aggression": "Forgiving"
            }
