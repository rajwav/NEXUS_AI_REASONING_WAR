"""
NEXUS PUZZLE ARENA - Tactical Battle Arena Engine (Game-First Architecture)
Features:
- 7x6 tactical gravity grid
- Dynamic player vs AI turns
- 3 AI difficulty tiers:
  * Easy (Random exploratory moves)
  * Medium (1-step lookahead + block player wins)
  * Hard (Full evaluation heuristic)
- Win detection, draw detection, move history, and instant reset
"""

from typing import List, Tuple, Dict, Optional, Any
import random


class BattleArenaEngine:
    """
    Rows: 6, Columns: 7
    Player 1: Blue Quantum Ion (1)
    AI Opponent: Red Neural Core (2)
    Empty: 0
    """
    def __init__(self, rows: int = 6, cols: int = 7, difficulty: str = "medium", seed: Optional[int] = None):
        self.rows = rows
        self.cols = cols
        self.difficulty = difficulty.lower()
        self.seed = seed
        self.rng = random.Random(seed) if seed is not None else random.Random()
        self.board: List[List[int]] = [[0]*cols for _ in range(rows)]
        self.game_over = False
        self.winner: Optional[int] = None
        self.winning_line: List[Tuple[int, int]] = []
        self.move_history: List[Tuple[int, int, int]] = []  # (r, c, piece)

    def reset_game(self, seed: Optional[int] = None):
        if seed is not None:
            self.seed = seed
            self.rng = random.Random(seed)
        elif self.seed is not None:
            self.rng = random.Random(self.seed)
        self.board = [[0]*self.cols for _ in range(self.rows)]
        self.game_over = False
        self.winner = None
        self.winning_line.clear()
        self.move_history.clear()

    def get_valid_columns(self) -> List[int]:
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def get_next_open_row(self, col: int) -> Optional[int]:
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def drop_piece(self, col: int, piece: int) -> Tuple[bool, str]:
        if self.game_over:
            return False, "Battle is finished."
        if col < 0 or col >= self.cols or self.board[0][col] != 0:
            return False, "Invalid or full column."

        row = self.get_next_open_row(col)
        if row is None:
            return False, "Column is full."

        self.board[row][col] = piece
        self.move_history.append((row, col, piece))

        if self.check_win(piece):
            self.game_over = True
            self.winner = piece
            label = "PLAYER" if piece == 1 else "AEGIS AI"
            return True, f"💥 {label} WINS THE BATTLE!"

        if not self.get_valid_columns():
            self.game_over = True
            self.winner = 0  # Draw
            return True, "⚡ DRAW! Grid energy saturated."

        return True, f"Piece dropped into column {col + 1}."

    def get_ai_move(self) -> Optional[int]:
        valid_cols = self.get_valid_columns()
        if not valid_cols:
            return None

        # Easy: Random choice
        if self.difficulty == "easy":
            return self.rng.choice(valid_cols)

        # Medium / Hard: Check immediate winning move
        for c in valid_cols:
            r = self.get_next_open_row(c)
            self.board[r][c] = 2
            if self.check_win(2):
                self.board[r][c] = 0
                return c
            self.board[r][c] = 0

        # Block opponent's immediate winning move
        for c in valid_cols:
            r = self.get_next_open_row(c)
            self.board[r][c] = 1
            if self.check_win(1):
                self.board[r][c] = 0
                return c
            self.board[r][c] = 0

        if self.difficulty == "medium":
            # Prefer center columns
            center = self.cols // 2
            valid_cols.sort(key=lambda c: abs(c - center))
            return valid_cols[0]

        # Hard: Simple position scoring
        best_score = -999999
        best_col = valid_cols[0]
        for c in valid_cols:
            r = self.get_next_open_row(c)
            self.board[r][c] = 2
            score = self._score_position(2)
            self.board[r][c] = 0
            if score > best_score:
                best_score = score
                best_col = c
        return best_col

    def _score_position(self, piece: int) -> int:
        score = 0
        center = [self.board[r][self.cols // 2] for r in range(self.rows)]
        score += center.count(piece) * 4
        return score

    def check_win(self, piece: int) -> bool:
        # Optimization: Avoid generator overhead in check_win by unrolling the 4-in-a-row checks
        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    self.winning_line = [(r, c + i) for i in range(4)]
                    return True
        # Vertical
        for r in range(self.rows - 3):
            for c in range(self.cols):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    self.winning_line = [(r + i, c) for i in range(4)]
                    return True
        # Positive Diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    self.winning_line = [(r + i, c + i) for i in range(4)]
                    return True
        # Negative Diagonal
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    self.winning_line = [(r - i, c + i) for i in range(4)]
                    return True
        return False

    def get_hint(self) -> Optional[int]:
        """Recommends the best tactical column for Player 1 (Blue)."""
        valid = self.get_valid_columns()
        if not valid:
            return None
        # Check immediate winning move for player
        for c in valid:
            r = self.get_next_open_row(c)
            self.board[r][c] = 1
            if self.check_win(1):
                self.board[r][c] = 0
                return c
            self.board[r][c] = 0
        # Block AI winning move
        for c in valid:
            r = self.get_next_open_row(c)
            self.board[r][c] = 2
            if self.check_win(2):
                self.board[r][c] = 0
                return c
            self.board[r][c] = 0
        # Prefer center
        center = self.cols // 2
        valid.sort(key=lambda c: abs(c - center))
        return valid[0]
