"""
NEXUS AI REASONING WAR - Decision Tree Dynamic Difficulty Engine
Adapts gameplay challenge, puzzle timer constraints, hint availability,
and enemy lookahead depth based on player performance metrics.
"""

from typing import Dict, List, Tuple, Optional, Any
from enum import Enum


class DifficultyLevel(Enum):
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"
    EXPERT = "EXPERT"


class DecisionTreeNode:
    def __init__(self, feature_idx: Optional[int] = None, threshold: Optional[float] = None,
                 left: Optional['DecisionTreeNode'] = None, right: Optional['DecisionTreeNode'] = None,
                 prediction: Optional[DifficultyLevel] = None, reason: str = ""):
        self.feature_idx = feature_idx
        self.threshold = threshold
        self.left = left    # <= threshold
        self.right = right  # > threshold
        self.prediction = prediction
        self.reason = reason

    def is_leaf(self) -> bool:
        return self.prediction is not None


class DecisionTreeDifficulty:
    """
    Decision Tree Classifier evaluating:
    Feature 0: Error Rate (mistakes / attempts)
    Feature 1: Solving Speed Index (actions per minute)
    Feature 2: Hint Frequency
    Feature 3: Autonomy Level
    """
    def __init__(self):
        self.root = self._build_tree()

    def _build_tree(self) -> DecisionTreeNode:
        """Constructs an interpretable rule-based decision tree."""
        # Node: Error Rate > 0.40?
        # High error rate branch -> Easy/Normal
        left_branch = DecisionTreeNode(
            feature_idx=2, threshold=0.30,  # Hint frequency > 0.30?
            left=DecisionTreeNode(prediction=DifficultyLevel.NORMAL, reason="Moderate errors but independent exploration"),
            right=DecisionTreeNode(prediction=DifficultyLevel.EASY, reason="High error rate and frequent hint reliance")
        )

        # Low error rate branch -> Normal/Hard/Expert
        right_sub = DecisionTreeNode(
            feature_idx=3, threshold=0.75,  # Autonomy > 0.75?
            left=DecisionTreeNode(prediction=DifficultyLevel.HARD, reason="Low error rate with moderate AI assistance"),
            right=DecisionTreeNode(
                feature_idx=1, threshold=0.60,  # High speed?
                left=DecisionTreeNode(prediction=DifficultyLevel.HARD, reason="Deliberate methodical expert solving"),
                right=DecisionTreeNode(prediction=DifficultyLevel.EXPERT, reason="Flawless high-speed autonomous mastery")
            )
        )

        root = DecisionTreeNode(
            feature_idx=0, threshold=0.35,
            left=right_sub,   # Error rate <= 0.35
            right=left_branch # Error rate > 0.35
        )
        return root

    def evaluate(self, error_rate: float, speed_index: float,
                 hint_freq: float, autonomy: float) -> Tuple[DifficultyLevel, str]:
        features = [error_rate, speed_index, hint_freq, autonomy]
        curr = self.root
        path = []

        while not curr.is_leaf():
            val = features[curr.feature_idx]
            if val <= curr.threshold:
                path.append(f"f[{curr.feature_idx}] ({val:.2f}) <= {curr.threshold:.2f}")
                curr = curr.left
            else:
                path.append(f"f[{curr.feature_idx}] ({val:.2f}) > {curr.threshold:.2f}")
                curr = curr.right

        return curr.prediction, curr.reason

    def get_difficulty_parameters(self, level: DifficultyLevel) -> Dict[str, Any]:
        """Maps difficulty to concrete puzzle & gameplay rules."""
        if level == DifficultyLevel.EASY:
            return {
                "max_hints": 5,
                "ai_minimax_depth": 1,
                "csp_variable_count": 3,
                "timer_multiplier": 1.5,
                "hazard_damage": 5
            }
        elif level == DifficultyLevel.NORMAL:
            return {
                "max_hints": 3,
                "ai_minimax_depth": 2,
                "csp_variable_count": 4,
                "timer_multiplier": 1.0,
                "hazard_damage": 10
            }
        elif level == DifficultyLevel.HARD:
            return {
                "max_hints": 2,
                "ai_minimax_depth": 3,
                "csp_variable_count": 5,
                "timer_multiplier": 0.8,
                "hazard_damage": 15
            }
        else:  # EXPERT
            return {
                "max_hints": 1,
                "ai_minimax_depth": 4,
                "csp_variable_count": 6,
                "timer_multiplier": 0.6,
                "hazard_damage": 25
            }
