"""
Unit Tests - NEXUS Machine Learning Engine
Tests K-Means Player Archetyping, Decision Tree Difficulty, and ANN Success Prediction.
"""

import unittest
from ML.kmeans_analyzer import KMeansAnalyzer, PlayerArchetype
from ML.decision_tree_difficulty import DecisionTreeDifficulty, DifficultyLevel
from ML.ann_predictor import ANNSuccessPredictor
from ML.ml_pipeline import MLPipeline
from GameEngine.player import Player
from GameEngine.events import EventBus


class TestMachineLearning(unittest.TestCase):
    def setUp(self):
        self.kmeans = KMeansAnalyzer()
        self.dt = DecisionTreeDifficulty()
        self.ann = ANNSuccessPredictor()

    def test_kmeans_archetype_prediction(self):
        # Explorer vector (high velocity, moderate error, low hint, low risk, high autonomy)
        vec_explorer = [0.85, 0.20, 0.15, 0.25, 0.80]
        archetype, conf, dists = self.kmeans.predict(vec_explorer)
        self.assertEqual(archetype, PlayerArchetype.EXPLORER)
        self.assertGreater(conf, 0.3)

        # Beginner vector (moderate velocity, high error, high hint, moderate risk, low autonomy)
        vec_beginner = [0.40, 0.65, 0.70, 0.40, 0.30]
        arch_beg, conf_b, _ = self.kmeans.predict(vec_beginner)
        self.assertEqual(arch_beg, PlayerArchetype.BEGINNER)

    def test_decision_tree_difficulty_routing(self):
        # High error rate and frequent hints -> EASY
        diff, reason = self.dt.evaluate(error_rate=0.60, speed_index=0.40, hint_freq=0.50, autonomy=0.30)
        self.assertEqual(diff, DifficultyLevel.EASY)

        # Flawless high speed -> EXPERT
        diff_exp, _ = self.dt.evaluate(error_rate=0.05, speed_index=0.85, hint_freq=0.05, autonomy=0.95)
        self.assertEqual(diff_exp, DifficultyLevel.EXPERT)

    def test_ann_forward_propagation(self):
        # High skill vector -> High success prob
        feat_high = [0.80, 0.05, 0.05, 0.10, 0.95]
        prob_high = self.ann.predict_probability(feat_high)
        self.assertTrue(0.0 <= prob_high <= 1.0)
        self.assertGreater(prob_high, 0.70)

        # Struggling vector -> Lower success prob
        feat_low = [0.20, 0.80, 0.90, 0.80, 0.10]
        prob_low = self.ann.predict_probability(feat_low)
        self.assertTrue(0.0 <= prob_low <= 1.0)
        self.assertLess(prob_low, prob_high)

    def test_unified_ml_pipeline(self):
        player = Player()
        bus = EventBus()
        pipeline = MLPipeline(player, bus)

        profile = pipeline.update_live_profile()
        self.assertIn("archetype", profile)
        self.assertIn("difficulty", profile)
        self.assertIn("win_probability", profile)


if __name__ == "__main__":
    unittest.main()
