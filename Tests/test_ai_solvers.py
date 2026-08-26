"""
Unit Tests for AI Solvers Package
Verifies:
- Sudoku CSP + MRV Solver
- Sokoban A* Search Solver
- Laser Raytrace Solver
- Minesweeper Constraint Inference Solver
- Battle Arena Minimax Solver
"""

import unittest
from AI_Solvers.sudoku_ai import SudokuAISolver
from AI_Solvers.sokoban_ai import SokobanAISolver
from AI_Solvers.laser_ai import LaserAISolver
from AI_Solvers.minesweeper_ai import MinesweeperAISolver
from AI_Solvers.battle_ai import BattleArenaAISolver
from LogicGames.sokoban_engine import SokobanEngine
from LogicGames.laser_engine import LaserEngine
from LogicGames.minesweeper_engine import CircuitMinesweeperEngine
from LogicGames.sudoku_engine import SudokuEngine
from LogicGames.battle_arena_engine import BattleArenaEngine


class TestAISolvers(unittest.TestCase):
    def test_sudoku_ai_solver(self):
        engine = SudokuEngine(seed=42, difficulty="easy")
        solver = SudokuAISolver(engine.board)
        res = solver.solve()
        self.assertTrue(res["solved"])
        self.assertGreater(len(res["steps"]), 0)
        # Check all cells are filled in final board
        for row in res["final_board"]:
            self.assertTrue(all(1 <= v <= 9 for v in row))

    def test_sokoban_ai_solver(self):
        engine = SokobanEngine(difficulty="easy")
        solver = SokobanAISolver(engine.walls, engine.targets, engine.boxes, engine.player_pos)
        res = solver.solve()
        self.assertTrue(res["solved"])
        self.assertGreater(len(res["steps"]), 0)
        self.assertGreater(res["total_pushes"], 0)

    def test_laser_ai_solver(self):
        engine = LaserEngine(seed=100, difficulty="easy")
        solver = LaserAISolver(engine.width, engine.height, engine.emitters,
                               engine.detectors, engine.obstacles, engine.mirrors)
        res = solver.solve()
        self.assertTrue(res["solved"])

    def test_minesweeper_ai_solver(self):
        engine = CircuitMinesweeperEngine(seed=100, difficulty="beginner")
        solver = MinesweeperAISolver(engine.width, engine.height, engine.mines)
        res = solver.solve()
        self.assertTrue(res["solved"])
        self.assertGreater(len(res["steps"]), 0)

    def test_battle_arena_ai_solver(self):
        engine = BattleArenaEngine(rows=6, cols=7)
        # Place 3 pieces in row for player 1
        engine.board[5][0] = 1
        engine.board[5][1] = 1
        engine.board[5][2] = 1
        solver = BattleArenaAISolver(engine.board, rows=6, cols=7)
        res = solver.solve(piece=1)
        self.assertTrue(res["solved"])
        self.assertEqual(res["recommended_col"], 4)  # Col index 3 (1-indexed: 4)


if __name__ == "__main__":
    unittest.main()
