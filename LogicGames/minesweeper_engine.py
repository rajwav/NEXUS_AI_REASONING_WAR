"""
NEXUS PUZZLE ARENA - Circuit Minesweeper Engine (Game-First Architecture)
Features:
- Guaranteed safe first-click generation
- Flood fill reveal on zero-neighbor cells
- Flagging and unflagging
- Difficulty presets:
  * Beginner: 8x8 with 10 mines
  * Intermediate: 12x12 with 25 mines
  * Expert: 16x16 with 45 mines
- Seed support and instant reset
"""

from typing import List, Tuple, Dict, Set, Optional, Any
import random


class CircuitMinesweeperEngine:
    def __init__(self, seed: Optional[int] = None, difficulty: str = "beginner"):
        self.seed = seed if seed is not None else random.randint(100000, 999999)
        self.difficulty = difficulty.lower()

        self.width = 8
        self.height = 8
        self.num_mines = 10

        self.mines: Set[Tuple[int, int]] = set()
        self.revealed: Set[Tuple[int, int]] = set()
        self.flagged: Set[Tuple[int, int]] = set()
        self.is_first_click = True
        self.game_over = False
        self.won = False

        self.setup_difficulty(self.difficulty)

    def setup_difficulty(self, difficulty: str):
        self.difficulty = difficulty.lower()
        if self.difficulty == "intermediate":
            self.width, self.height = 12, 12
            self.num_mines = 25
        elif self.difficulty == "expert":
            self.width, self.height = 16, 16
            self.num_mines = 45
        else:  # beginner
            self.width, self.height = 8, 8
            self.num_mines = 10

        self.reset_game()

    def reset_game(self):
        """Restores to virgin unclicked state."""
        self.revealed.clear()
        self.flagged.clear()
        self.mines.clear()
        self.is_first_click = True
        self.game_over = False
        self.won = False

    def generate_mines(self, safe_x: int, safe_y: int):
        """Guarantees first click and its 8 neighbors are 100% safe."""
        rng = random.Random(self.seed)
        forbidden = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                forbidden.add((safe_x + dx, safe_y + dy))

        candidates = [
            (x, y) for x in range(self.width) for y in range(self.height)
            if (x, y) not in forbidden
        ]
        rng.shuffle(candidates)
        self.mines = set(candidates[:self.num_mines])

    def get_adjacent_mines_count(self, x: int, y: int) -> int:
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in self.mines:
                    count += 1
        return count

    def reveal_cell(self, x: int, y: int) -> Tuple[bool, str]:
        if self.game_over or self.won or (x, y) in self.flagged:
            return False, "Cell cannot be revealed."

        # Handle first click safety
        if self.is_first_click:
            self.generate_mines(x, y)
            self.is_first_click = False

        if (x, y) in self.mines:
            self.revealed.add((x, y))
            self.game_over = True
            return False, "💥 BOOM! Triggered overload fuse! Game Over!"

        # Flood fill reveal
        queue = [(x, y)]
        self.revealed.add((x, y))

        while queue:
            cx, cy = queue.pop(0)
            if self.get_adjacent_mines_count(cx, cy) == 0:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if (nx, ny) not in self.revealed and (nx, ny) not in self.flagged:
                                self.revealed.add((nx, ny))
                                if self.get_adjacent_mines_count(nx, ny) == 0:
                                    queue.append((nx, ny))

        # Check win condition
        total_cells = self.width * self.height
        if len(self.revealed) == total_cells - len(self.mines):
            self.won = True
            return True, "🎉 CONGRATULATIONS! All safe nodes revealed!"

        return True, "Node revealed."

    def toggle_flag(self, x: int, y: int) -> Tuple[bool, str]:
        if self.game_over or self.won or (x, y) in self.revealed:
            return False, "Cannot flag revealed node."
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))
            return True, "Removed flag."
        else:
            self.flagged.add((x, y))
            return True, "Placed flag."

    @property
    def remaining_mines(self) -> int:
        return self.num_mines - len(self.flagged)

    def get_hint(self) -> Optional[Tuple[int, int]]:
        """Returns a guaranteed safe unrevealed coordinate (x, y)."""
        if self.is_first_click:
            return (self.width // 2, self.height // 2)
        safe_candidates = [
            (x, y) for x in range(self.width) for y in range(self.height)
            if (x, y) not in self.mines and (x, y) not in self.revealed and (x, y) not in self.flagged
        ]
        return safe_candidates[0] if safe_candidates else None
