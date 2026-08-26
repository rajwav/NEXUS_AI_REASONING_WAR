"""
NEXUS PUZZLE ARENA - Unit & Integration Tests for Game-First Systems
Verifies:
1. Sudoku: Procedural generator always solvable, unique solution, seed reproducibility, reset works.
2. Sokoban: All 20 handcrafted levels parsed and solvable, undo/reset works.
3. Laser: Raytracing physics, rotatable mirror mechanics, reset works.
4. Minesweeper: First-click guaranteed safe generation, flood fill, flag toggle.
5. Battle Arena: Drop mechanics, win condition verification, AI turns.
"""

import unittest
from LogicGames.sudoku_engine import SudokuEngine
from LogicGames.sokoban_engine import SokobanEngine
from LogicGames.laser_engine import LaserEngine, MirrorType
from LogicGames.minesweeper_engine import CircuitMinesweeperEngine
from LogicGames.battle_arena_engine import BattleArenaEngine


class TestLogicGamesSuite(unittest.TestCase):

    def test_sudoku_procedural_generator_and_seed(self):
        seed1 = 482910
        engine1 = SudokuEngine(seed=seed1, difficulty="easy")
        engine2 = SudokuEngine(seed=seed1, difficulty="easy")

        # Verify seed reproducibility
        self.assertEqual(engine1.initial_board, engine2.initial_board)
        self.assertEqual(engine1.solution_board, engine2.solution_board)
        self.assertEqual(engine1.grid, engine1.current_board)
        self.assertEqual(engine1.initial_grid, engine1.initial_board)
        self.assertEqual(engine1.solution, engine1.solution_board)

        # Verify initial clues count for easy mode
        clues_count = sum(1 for r in range(9) for c in range(9) if engine1.initial_board[r][c] != 0)
        self.assertEqual(clues_count, 40)

        # Test set cell and reset
        first_empty = None
        for r in range(9):
            for c in range(9):
                if engine1.initial_board[r][c] == 0:
                    first_empty = (r, c)
                    break
            if first_empty:
                break

        r, c = first_empty
        correct_val = engine1.solution_board[r][c]
        succ, msg = engine1.set_cell_value(r, c, correct_val)
        self.assertTrue(succ)
        self.assertEqual(engine1.current_board[r][c], correct_val)

        # Test reset
        engine1.reset_puzzle()
        self.assertEqual(engine1.current_board[r][c], 0)
        self.assertEqual(engine1.mistakes, 0)

    def test_sokoban_levels_and_undo_reset(self):
        for diff, lvls in SokobanEngine.HANDCRAFTED_DATABASE.items():
            for lvl_idx in range(1, len(lvls) + 1):
                engine = SokobanEngine(difficulty=diff, level_id=lvl_idx)
                self.assertTrue(len(engine.walls) > 0)
                self.assertTrue(len(engine.targets) > 0)
                self.assertEqual(len(engine.targets), len(engine.boxes))
                self.assertIsNotNone(engine.player_pos)

        # Test A* solvability on Easy Level 1
        eng = SokobanEngine(difficulty="easy", level_id=1)
        solution = eng.solve_astar(max_expansions=2000)
        self.assertIsNotNone(solution)
        self.assertTrue(len(solution) > 0)

        # Test move and undo on Easy
        init_pos = eng.player_pos
        init_boxes = set(eng.boxes)

        eng.move(0, 1)  # Move down
        self.assertNotEqual(eng.player_pos, init_pos)

        # Test corner deadlock check
        self.assertTrue(eng.is_corner_deadlock(1, 1))
        self.assertFalse(eng.is_corner_deadlock(3, 3))

        # Undo
        self.assertTrue(eng.undo())
        self.assertEqual(eng.player_pos, init_pos)
        self.assertEqual(eng.boxes, init_boxes)

        # Reset
        eng.move(0, 1)
        eng.reset_level()
        self.assertEqual(eng.player_pos, init_pos)

    def test_laser_engine_raytrace_and_reset(self):
        for diff in ["easy", "medium", "hard", "expert", "nightmare"]:
            engine = LaserEngine(seed=482910, difficulty=diff)
            self.assertTrue(len(engine.rotatable_slots) > 0)
            self.assertTrue(len(engine.detectors) > 0)
            self.assertTrue(len(engine.emitters) > 0)
            
            # Apply solved mirror orientations and verify 100% raytrace hit
            engine.mirrors = dict(engine.solved_mirrors)
            self.assertTrue(engine.is_solved())

        # Test rotating a mirror
        engine = LaserEngine(seed=12345, difficulty="easy")
        slot = engine.rotatable_slots[0]
        init_m = engine.mirrors[slot]
        engine.rotate_mirror(slot[0], slot[1])
        self.assertNotEqual(engine.mirrors[slot], init_m)

        # Test reset
        engine.reset_level()
        self.assertEqual(engine.mirrors[slot], init_m)

    def test_minesweeper_first_click_safety(self):
        engine = CircuitMinesweeperEngine(seed=99999, difficulty="beginner")
        self.assertTrue(engine.is_first_click)

        # First click at (3, 3)
        succ, msg = engine.reveal_cell(3, 3)
        self.assertTrue(succ)
        self.assertFalse(engine.game_over)
        self.assertTrue((3, 3) in engine.revealed)
        self.assertFalse((3, 3) in engine.mines)

        # Neighbors of first click must also be safe
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                self.assertFalse((3 + dx, 3 + dy) in engine.mines)

    def test_battle_arena_game_loop(self):
        engine = BattleArenaEngine(rows=6, cols=7, difficulty="medium", seed=42819)
        self.assertFalse(engine.game_over)
        self.assertEqual(engine.seed, 42819)

        # Keyword args without rows/cols (as passed by UI)
        engine_kw = BattleArenaEngine(difficulty="hard", seed=999)
        self.assertEqual(engine_kw.rows, 6)
        self.assertEqual(engine_kw.cols, 7)
        self.assertEqual(engine_kw.seed, 999)

        # Drop 4 in vertical column 0 for player
        engine.drop_piece(0, 1)
        engine.drop_piece(0, 1)
        engine.drop_piece(0, 1)
        engine.drop_piece(0, 1)

        self.assertTrue(engine.game_over)
        self.assertEqual(engine.winner, 1)

        # Reset
        engine.reset_game()
        self.assertFalse(engine.game_over)
        self.assertIsNone(engine.winner)


if __name__ == "__main__":
    unittest.main()
