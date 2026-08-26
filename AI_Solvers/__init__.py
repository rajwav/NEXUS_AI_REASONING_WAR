"""
NEXUS PUZZLE ARENA - AI Solvers Package
Unified step-by-step AI Solver Suite for all 5 Logic Games:
- Sudoku: CSP + MRV + Forward Checking
- Sokoban: A* Search + Deadlock Detection
- Laser Mirror: Search + Beam Raytracing
- Minesweeper: Logical Constraint Inference / SAT
- Battle Arena: Minimax + Alpha-Beta Pruning
"""

from .sudoku_ai import SudokuAISolver
from .sokoban_ai import SokobanAISolver
from .laser_ai import LaserAISolver
from .minesweeper_ai import MinesweeperAISolver
from .battle_ai import BattleArenaAISolver

__all__ = [
    "SudokuAISolver",
    "SokobanAISolver",
    "LaserAISolver",
    "MinesweeperAISolver",
    "BattleArenaAISolver",
]
