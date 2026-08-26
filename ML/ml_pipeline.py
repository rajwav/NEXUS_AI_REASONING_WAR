"""
NEXUS AI REASONING WAR - Unified Machine Learning Runtime Pipeline
Subscribes to live gameplay telemetry, runs real-time inference across
K-Means, Decision Tree, and ANN, and dynamically updates game parameters.
"""

from typing import Dict, List, Tuple, Optional, Any
import time
from .kmeans_analyzer import KMeansAnalyzer, PlayerArchetype
from .decision_tree_difficulty import DecisionTreeDifficulty, DifficultyLevel
from .ann_predictor import ANNSuccessPredictor
from GameEngine.player import Player, PlayerStats
from GameEngine.events import EventBus, Event, EventType


class MLPipeline:
    """Unified telemetry collector and online adaptation engine."""
    def __init__(self, player: Player, event_bus: EventBus):
        self.player = player
        self.event_bus = event_bus

        self.kmeans = KMeansAnalyzer(k=4)
        self.decision_tree = DecisionTreeDifficulty()
        self.ann = ANNSuccessPredictor()

        self.current_archetype = PlayerArchetype.BEGINNER
        self.archetype_confidence = 0.50
        self.current_difficulty = DifficultyLevel.NORMAL
        self.difficulty_reason = "Initial benchmark"
        self.predicted_win_probability = 0.75
        self.last_update_time = time.time()

        self._subscribe_events()

    def _subscribe_events(self):
        """Hook into game events to trigger real-time ML adaptation."""
        for et in [
            EventType.PLAYER_MOVED,
            EventType.OBJECT_INSPECTED,
            EventType.PUZZLE_ATTEMPT,
            EventType.PUZZLE_SOLVED,
            EventType.PUZZLE_FAILED,
            EventType.ITEM_USED
        ]:
            self.event_bus.subscribe(et, self._on_game_event)

    def _on_game_event(self, event: Event):
        # Throttle evaluation to at most once per 0.5 seconds of game time
        now = time.time()
        if now - self.last_update_time >= 0.5:
            self.update_live_profile()
            self.last_update_time = now

    def update_live_profile(self) -> Dict[str, Any]:
        """Runs full ML pipeline inference on current player telemetry."""
        feat_vec = self.player.stats.get_telemetry_vector()
        velocity, error_rate, hint_dep, risk_idx, autonomy = feat_vec

        # 1. K-Means Player Archetype
        archetype, confidence, dist_dict = self.kmeans.predict(feat_vec)
        self.current_archetype = archetype
        self.archetype_confidence = confidence

        # 2. Decision Tree Dynamic Difficulty
        speed_idx = velocity
        difficulty, reason = self.decision_tree.evaluate(error_rate, speed_idx, hint_dep, autonomy)
        self.current_difficulty = difficulty
        self.difficulty_reason = reason

        # 3. ANN Mission Success Predictor
        win_prob = self.ann.predict_probability(feat_vec)
        self.predicted_win_probability = win_prob

        profile = {
            "archetype": self.current_archetype.value,
            "archetype_confidence": self.archetype_confidence,
            "difficulty": self.current_difficulty.value,
            "difficulty_reason": self.difficulty_reason,
            "win_probability": self.predicted_win_probability,
            "gameplay_modifiers": self.kmeans.get_gameplay_modifiers(self.current_archetype),
            "difficulty_params": self.decision_tree.get_difficulty_parameters(self.current_difficulty),
            "assessment": self.ann.get_performance_assessment(win_prob),
            "telemetry_features": {
                "velocity": round(velocity, 3),
                "error_rate": round(error_rate, 3),
                "hint_dependency": round(hint_dep, 3),
                "risk_index": round(risk_idx, 3),
                "autonomy_ratio": round(autonomy, 3)
            }
        }
        return profile
