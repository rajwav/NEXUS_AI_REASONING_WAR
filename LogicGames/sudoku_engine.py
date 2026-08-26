"""
NEXUS PUZZLE ARENA - Quantum Sudoku Engine (Commercial Polish Pass)
Features:
- Las Vegas procedural generator with unique solution verification
- Number tracking (counts 1-9 completed)
- Number highlighting support (same number, same row, same col, same 3x3 block)
- Difficulty levels: Easy (40 clues), Medium (32 clues), Hard (27 clues), Expert (22 clues), Nightmare (18 clues)
- 3-strike mistake detection, pencil notes, seed reproducibility, and instant reset
"""

from typing import List, Tuple, Dict, Set, Optional, Any
import random
import copy


class SudokuEngine:
    def __init__(self, seed: Optional[int] = None, difficulty: str = "medium"):
        self.size = 9
        self.box_size = 3
        self.seed = seed if seed is not None else random.randint(100000, 999999)
        self.difficulty = difficulty.lower()
        
        self.solution_board: List[List[int]] = [[0]*9 for _ in range(9)]
        self.initial_board: List[List[int]] = [[0]*9 for _ in range(9)]
        self.current_board: List[List[int]] = [[0]*9 for _ in range(9)]
        self.notes: Dict[Tuple[int, int], Set[int]] = {}
        self.initial_fixed: Set[Tuple[int, int]] = set()

        self.mistakes = 0
        self.max_mistakes = 3
        self.is_game_over = False
        self.is_completed = False
        self.move_history: List[Dict[str, Any]] = []

        self.generate_new_puzzle(self.seed, self.difficulty)

    @property
    def board(self) -> List[List[int]]:
        return self.current_board

    @property
    def grid(self) -> List[List[int]]:
        return self.current_board

    @grid.setter
    def grid(self, value: List[List[int]]):
        self.current_board = value

    @property
    def initial_grid(self) -> List[List[int]]:
        return self.initial_board

    @property
    def solution(self) -> List[List[int]]:
        return self.solution_board

    def generate_new_puzzle(self, seed: int, difficulty: str = "medium"):
        self.seed = seed
        self.difficulty = difficulty.lower()
        self.mistakes = 0
        self.is_game_over = False
        self.is_completed = False
        self.move_history.clear()
        self.notes.clear()

        rng = random.Random(seed)

        # Step 1: Generate solved 9x9 board
        self.solution_board = [[0]*9 for _ in range(9)]
        self._fill_board_random(self.solution_board, rng)

        # Step 2: Difficulty target clues
        clue_counts = {
            "easy": 40,
            "medium": 32,
            "hard": 27,
            "expert": 22,
            "nightmare": 18
        }
        target_clues = clue_counts.get(self.difficulty, 32)
        cells_to_remove = 81 - target_clues

        # Step 3: Dig cells with solvability check
        puzzle_grid = [row[:] for row in self.solution_board]
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        rng.shuffle(all_positions)

        removed = 0
        for r, c in all_positions:
            if removed >= cells_to_remove:
                break
            temp = puzzle_grid[r][c]
            puzzle_grid[r][c] = 0

            if self._count_solutions(puzzle_grid) != 1:
                puzzle_grid[r][c] = temp
            else:
                removed += 1

        self.initial_board = [row[:] for row in puzzle_grid]
        self.current_board = [row[:] for row in puzzle_grid]
        self.initial_fixed = {(r, c) for r in range(9) for c in range(9) if puzzle_grid[r][c] != 0}

    def reset_puzzle(self):
        """Returns to exact starting state of the current seed."""
        self.current_board = [row[:] for row in self.initial_board]
        self.notes.clear()
        self.mistakes = 0
        self.is_game_over = False
        self.is_completed = False
        self.move_history.clear()

    def set_cell_value(self, row: int, col: int, num: int, auto_check_mistakes: bool = True) -> Tuple[bool, str]:
        if self.is_game_over or self.is_completed:
            return False, "Game is already finished."
        if (row, col) in self.initial_fixed:
            return False, "Fixed starting clue cannot be modified."

        if num == 0:
            self.current_board[row][col] = 0
            return True, "Cell cleared."

        # Check mistake against solution
        if auto_check_mistakes and num != self.solution_board[row][col]:
            self.mistakes += 1
            if self.mistakes >= self.max_mistakes:
                self.is_game_over = True
                return False, f"Mistake #{self.mistakes}! Strike 3 — Game Over!"
            return False, f"Incorrect digit. Mistake {self.mistakes}/{self.max_mistakes}."

        self.current_board[row][col] = num
        self.notes.pop((row, col), None)

        if self._is_board_complete():
            self.is_completed = True
            return True, "🎉 CONGRATULATIONS! Puzzle Completed Successfully!"

        return True, f"Placed {num}."

    def get_number_counts(self) -> Dict[int, int]:
        """Returns how many of each digit (1-9) are currently placed on the board."""
        counts = {n: 0 for n in range(1, 10)}
        for r in range(9):
            for c in range(9):
                val = self.current_board[r][c]
                if val in counts:
                    counts[val] += 1
        return counts

    def is_number_completed(self, num: int) -> bool:
        """Returns True if all 9 instances of a number are correctly placed."""
        if num < 1 or num > 9:
            return False
        count = 0
        for r in range(9):
            for c in range(9):
                if self.current_board[r][c] == num:
                    if self.current_board[r][c] == self.solution_board[r][c]:
                        count += 1
                    else:
                        return False
        return count == 9

    def get_hint(self) -> Optional[Tuple[int, int, int]]:
        """Returns (row, col, value) for the first empty cell."""
        for r in range(9):
            for c in range(9):
                if self.current_board[r][c] == 0:
                    return (r, c, self.solution_board[r][c])
        return None

    def toggle_note(self, row: int, col: int, num: int) -> bool:
        if (row, col) in self.initial_fixed or self.current_board[row][col] != 0:
            return False
        if (row, col) not in self.notes:
            self.notes[(row, col)] = set()
        
        if num in self.notes[(row, col)]:
            self.notes[(row, col)].remove(num)
        else:
            self.notes[(row, col)].add(num)
        return True

    def _is_board_complete(self) -> bool:
        for r in range(9):
            for c in range(9):
                if self.current_board[r][c] != self.solution_board[r][c]:
                    return False
        return True

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        return self._is_valid_on_grid(self.current_board, row, col, num)

    def is_solved(self) -> bool:
        return self._is_board_complete()

    @staticmethod
    def _is_valid_on_grid(grid: List[List[int]], row: int, col: int, num: int) -> bool:
        for c in range(9):
            if c != col and grid[row][c] == num:
                return False
        for r in range(9):
            if r != row and grid[r][col] == num:
                return False
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r != row or c != col) and grid[r][c] == num:
                    return False
        return True

    def _fill_board_random(self, grid: List[List[int]], rng: random.Random) -> bool:
        empty = None
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    empty = (r, c)
                    break
            if empty:
                break
        if not empty:
            return True

        r, c = empty
        nums = list(range(1, 10))
        rng.shuffle(nums)

        for num in nums:
            if self._is_valid_on_grid(grid, r, c, num):
                grid[r][c] = num
                if self._fill_board_random(grid, rng):
                    return True
                grid[r][c] = 0
        return False

    def _count_solutions(self, grid: List[List[int]], limit: int = 2) -> int:
        grid_copy = [row[:] for row in grid]
        count = [0]

        def backtrack():
            if count[0] >= limit:
                return
            empty = None
            for r in range(9):
                for c in range(9):
                    if grid_copy[r][c] == 0:
                        empty = (r, c)
                        break
                if empty:
                    break
            if not empty:
                count[0] += 1
                return

            r, c = empty
            for num in range(1, 10):
                if self._is_valid_on_grid(grid_copy, r, c, num):
                    grid_copy[r][c] = num
                    backtrack()
                    grid_copy[r][c] = 0

        backtrack()
        return count[0]
