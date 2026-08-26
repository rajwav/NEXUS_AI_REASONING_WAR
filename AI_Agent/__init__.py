# AI_Agent Package Init
"""
NEXUS AI REASONING WAR - AI Companion & Autonomous Solver Suite
Provides NOVA AI companion personality, step-by-step autonomous solver,
and real-time algorithm reasoning tracer.
"""

from .nova_agent import NovaCompanion
from .autonomous_solver import AutonomousSolver
from .reasoning_tracer import ReasoningTracer

__all__ = [
    "NovaCompanion",
    "AutonomousSolver",
    "ReasoningTracer",
]
