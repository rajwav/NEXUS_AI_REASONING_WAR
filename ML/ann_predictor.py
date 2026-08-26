"""
NEXUS AI REASONING WAR - Artificial Neural Network (ANN) Success Predictor
Pure Python Multi-Layer Perceptron predicting real-time Mission Success Probability
P(Success) from player cognitive telemetry and historical mission performance.
"""

from typing import List, Dict, Tuple, Optional, Any
import math
import random


class ANNSuccessPredictor:
    """
    Feedforward Neural Network (Architecture: 5 Inputs -> 8 Hidden (ReLU) -> 1 Output (Sigmoid))
    Inputs:
    [Normalized Velocity, Error Rate, Hint Dependency, Risk Score, Autonomy Ratio]
    Output:
    Mission Success Probability [0.0 to 1.0]
    """
    def __init__(self):
        # Weights initialized with calibrated values
        self.input_dim = 5
        self.hidden_dim = 8
        self.output_dim = 1

        # Pre-trained weights calibrated for realistic player evaluation
        self.w1 = [
            [-0.35, 0.45, -0.80, -0.60, 0.90],
            [ 0.60, -0.75, -0.50, -0.40, 0.85],
            [-0.20, -0.90, -0.70, -0.50, 0.70],
            [ 0.40, -0.30, -0.40,  0.20, 0.60],
            [-0.50,  0.80,  0.60,  0.70, -0.80],
            [ 0.30, -0.60, -0.50, -0.30, 0.75],
            [-0.10, -0.85, -0.65, -0.45, 0.80],
            [ 0.50, -0.40, -0.30,  0.10, 0.65]
        ]
        self.b1 = [0.10, 0.25, 0.15, -0.05, -0.30, 0.20, 0.18, 0.05]

        self.w2 = [
            [0.65, 0.85, 0.70, 0.40, -0.95, 0.80, 0.75, 0.55]
        ]
        self.b2 = [0.35]

    def _relu(self, x: float) -> float:
        return max(0.0, x)

    def _sigmoid(self, x: float) -> float:
        # Clip to prevent overflow
        x_clipped = max(-20.0, min(20.0, x))
        return 1.0 / (1.0 + math.exp(-x_clipped))

    def predict_probability(self, feature_vector: List[float]) -> float:
        """
        Performs forward pass and returns win probability.
        """
        if len(feature_vector) != self.input_dim:
            # Pad or truncate if necessary
            feature_vector = (feature_vector + [0.5] * self.input_dim)[:self.input_dim]

        # Hidden Layer
        hidden = []
        for i in range(self.hidden_dim):
            z = sum(w * x for w, x in zip(self.w1[i], feature_vector)) + self.b1[i]
            hidden.append(self._relu(z))

        # Output Layer
        z_out = sum(w * h for w, h in zip(self.w2[0], hidden)) + self.b2[0]
        prob = self._sigmoid(z_out)

        return round(prob, 4)

    def get_performance_assessment(self, prob: float) -> Dict[str, Any]:
        """Translates neural probability into immersive in-universe facility diagnostic telemetry."""
        threat_level = max(0.0, min(1.0, 1.0 - prob))
        bars = int(threat_level * 10)
        threat_meter = "█" * bars + "░" * (10 - bars)

        if threat_level <= 0.25:
            threat_desc = "LOW / NOMINAL"
            nova_rec = "Power grid harmonic stable. Northern conduit bypass route recommended."
            hud_color = "#76FF03"
        elif threat_level <= 0.55:
            threat_desc = "MODERATE STRAIN"
            nova_rec = "Cryogenic coolant pressure elevated. Check sub-relay circuit continuity before energizing."
            hud_color = "#00E5FF"
        elif threat_level <= 0.75:
            threat_desc = "ELEVATED RISK"
            nova_rec = "Repeated electrical arcs detected. Verify cable routing to avoid flooded coolant lines."
            hud_color = "#FFD600"
        else:
            threat_desc = "CRITICAL VOLTAGE SURGE"
            nova_rec = "Circuit overload imminent. Disengage flooded relays or allow NOVA autonomous bypass."
            hud_color = "#FF1744"

        return {
            "threat_meter": threat_meter,
            "threat_desc": threat_desc,
            "nova_recommendation": nova_rec,
            "hud_color": hud_color,
            "raw_prob": prob
        }
