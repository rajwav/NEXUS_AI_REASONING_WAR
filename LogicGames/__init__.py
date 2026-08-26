"""
NEXUS AI PUZZLE ARENA - Logic Games & AI Solvers Suite
Exports:
1. Quantum Sudoku (CSP + MRV + AC-3)
2. Cyber Sokoban (A* + Deadlock Detection)
3. Laser Mirror Routing (Vector Raytracing + Beam Search)
4. Circuit Minesweeper (Propositional Logic SAT Reasoning)
5. AI Battle Arena (Minimax + Alpha-Beta Pruning)
"""

from .sudoku_engine import SudokuEngine
from .sokoban_engine import SokobanEngine
from .laser_engine import LaserEngine, MirrorType
from .minesweeper_engine import CircuitMinesweeperEngine
from .battle_arena_engine import BattleArenaEngine

__all__ = [
    "SudokuEngine",
    "SokobanEngine",
    "LaserEngine",
    "MirrorType",
    "CircuitMinesweeperEngine",
    "BattleArenaEngine"
]
