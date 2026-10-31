"""
NEXUS AI REASONING WAR — Centralized Game Scoring Engine
Universal, Deterministic Time-Based Scoring:
    SCORE = max(0, 10000 - (elapsed_seconds * 10))

Principles:
- Lower completion time = Higher score.
- Exactly reproducible: The same elapsed time always produces the exact same score.
- Zero randomness, zero artificial bonuses, zero fake multipliers.
- Unsolved / incomplete attempts receive a score of 0.
- Raw gameplay telemetry (moves, pushes, rotations, safe cells, mistakes, hints, seed)
  is preserved in the record and JSONB payload for deep game statistics.
"""

from typing import Dict, Any, Optional


class ScoringEngine:
    """Universal deterministic scoring engine for all NEXUS reasoning games."""

    BASE_SCORE = 10000
    TIME_PENALTY_PER_SECOND = 10

    DIFFICULTY_DESCRIPTIONS = {
        "easy": "Standard Operative Protocol",
        "beginner": "Standard Operative Protocol",
        "medium": "Advanced Tactical Matrix",
        "intermediate": "Advanced Tactical Matrix",
        "hard": "Expert Cyber Warfare",
        "expert": "Elite Neural Challenge",
        "nightmare": "Singularity Vector"
    }

    @classmethod
    def get_difficulty_multiplier(cls, difficulty: str) -> float:
        """
        Returns 1.0 (difficulty is descriptive for baseline competitive leaderboards).
        No hidden score inflation.
        """
        return 1.0

    @classmethod
    def compute_formula(cls, elapsed_seconds: int, solved: bool = True) -> int:
        """
        Core universal formula:
            SCORE = max(0, 10000 - (elapsed_seconds * 10))
        """
        if not solved:
            return 0
        t = max(0, int(elapsed_seconds))
        penalty = t * cls.TIME_PENALTY_PER_SECOND
        return max(0, cls.BASE_SCORE - penalty)

    @classmethod
    def calculate_sudoku_score(cls,
                               difficulty: str = "medium",
                               solved: bool = True,
                               time_seconds: int = 0,
                               mistakes: int = 0,
                               hints: int = 0,
                               hints_used: int = 0,
                               seed: int = 0,
                               **kwargs) -> Dict[str, Any]:
        """Calculates deterministic score and telemetry for Sudoku."""
        elapsed = max(0, int(time_seconds))
        total_score = cls.compute_formula(elapsed, solved=solved)
        time_penalty = elapsed * cls.TIME_PENALTY_PER_SECOND if solved else 0
        h_used = hints or hints_used

        return {
            "game": "sudoku",
            "total_score": total_score,
            "base_score": cls.BASE_SCORE if solved else 0,
            "time_penalty": time_penalty,
            "elapsed_seconds": elapsed,
            "difficulty": str(difficulty).lower(),
            "difficulty_multiplier": 1.0,
            "mistakes": int(mistakes),
            "hints_used": int(h_used),
            "seed": int(seed) if seed else None,
            "solved": bool(solved),
            "summary": f"Base {cls.BASE_SCORE:,} - Time Penalty {time_penalty:,} ({elapsed}s × 10) = {total_score:,}" if solved else "Protocol incomplete (0 pts)"
        }

    @classmethod
    def calculate_sokoban_score(cls,
                                difficulty: str = "medium",
                                solved: bool = True,
                                time_seconds: int = 0,
                                moves: int = 0,
                                pushes: int = 0,
                                target_moves: Optional[int] = None,
                                optimal_moves: Optional[int] = None,
                                seed: int = 0,
                                **kwargs) -> Dict[str, Any]:
        """Calculates deterministic score and telemetry for Cyber Sokoban."""
        elapsed = max(0, int(time_seconds))
        total_score = cls.compute_formula(elapsed, solved=solved)
        time_penalty = elapsed * cls.TIME_PENALTY_PER_SECOND if solved else 0
        t_moves = target_moves or optimal_moves or 20

        return {
            "game": "sokoban",
            "total_score": total_score,
            "base_score": cls.BASE_SCORE if solved else 0,
            "time_penalty": time_penalty,
            "elapsed_seconds": elapsed,
            "difficulty": str(difficulty).lower(),
            "difficulty_multiplier": 1.0,
            "moves": int(moves),
            "pushes": int(pushes),
            "target_moves": int(t_moves),
            "seed": int(seed) if seed else None,
            "solved": bool(solved),
            "summary": f"Base {cls.BASE_SCORE:,} - Time Penalty {time_penalty:,} ({elapsed}s × 10) = {total_score:,}" if solved else "Protocol incomplete (0 pts)"
        }

    @classmethod
    def calculate_laser_score(cls,
                              difficulty: str = "medium",
                              solved: bool = True,
                              time_seconds: int = 0,
                              rotations: int = 0,
                              moves: int = 0,
                              seed: int = 0,
                              **kwargs) -> Dict[str, Any]:
        """Calculates deterministic score and telemetry for Laser Mirror Routing."""
        elapsed = max(0, int(time_seconds))
        total_score = cls.compute_formula(elapsed, solved=solved)
        time_penalty = elapsed * cls.TIME_PENALTY_PER_SECOND if solved else 0
        r_count = rotations or moves

        return {
            "game": "laser",
            "total_score": total_score,
            "base_score": cls.BASE_SCORE if solved else 0,
            "time_penalty": time_penalty,
            "elapsed_seconds": elapsed,
            "difficulty": str(difficulty).lower(),
            "difficulty_multiplier": 1.0,
            "rotations": int(r_count),
            "seed": int(seed) if seed else None,
            "solved": bool(solved),
            "summary": f"Base {cls.BASE_SCORE:,} - Time Penalty {time_penalty:,} ({elapsed}s × 10) = {total_score:,}" if solved else "Protocol incomplete (0 pts)"
        }

    @classmethod
    def calculate_minesweeper_score(cls,
                                    difficulty: str = "medium",
                                    solved: bool = True,
                                    time_seconds: int = 0,
                                    remaining_lives: int = 3,
                                    safe_cleared: int = 0,
                                    safe_cells_cleared: int = 0,
                                    seed: int = 0,
                                    **kwargs) -> Dict[str, Any]:
        """Calculates deterministic score and telemetry for Circuit Minesweeper."""
        elapsed = max(0, int(time_seconds))
        is_completed = bool(solved and remaining_lives > 0)
        total_score = cls.compute_formula(elapsed, solved=is_completed)
        time_penalty = elapsed * cls.TIME_PENALTY_PER_SECOND if is_completed else 0
        s_cleared = safe_cleared or safe_cells_cleared

        return {
            "game": "minesweeper",
            "total_score": total_score,
            "base_score": cls.BASE_SCORE if is_completed else 0,
            "time_penalty": time_penalty,
            "elapsed_seconds": elapsed,
            "difficulty": str(difficulty).lower(),
            "difficulty_multiplier": 1.0,
            "remaining_lives": int(remaining_lives),
            "safe_cells_cleared": int(s_cleared),
            "seed": int(seed) if seed else None,
            "solved": is_completed,
            "summary": f"Base {cls.BASE_SCORE:,} - Time Penalty {time_penalty:,} ({elapsed}s × 10) = {total_score:,}" if is_completed else "Circuit overload / incomplete (0 pts)"
        }

    @classmethod
    def calculate_battle_score(cls,
                               difficulty: str = "medium",
                               outcome: str = "win",
                               moves: int = 0,
                               time_seconds: int = 0,
                               solved: bool = True,
                               **kwargs) -> Dict[str, Any]:
        """Calculates deterministic score and telemetry for Tactical Battle Arena."""
        elapsed = max(0, int(time_seconds))
        outcome_str = str(outcome).lower()
        is_win_or_draw = outcome_str in ("win", "victory", "player_win", "draw", "stalemate") and solved
        is_victory = outcome_str in ("win", "victory", "player_win") and solved

        total_score = cls.compute_formula(elapsed, solved=is_victory)
        time_penalty = elapsed * cls.TIME_PENALTY_PER_SECOND if is_victory else 0

        return {
            "game": "battle",
            "total_score": total_score,
            "base_score": cls.BASE_SCORE if is_victory else 0,
            "time_penalty": time_penalty,
            "elapsed_seconds": elapsed,
            "difficulty": str(difficulty).lower(),
            "difficulty_multiplier": 1.0,
            "moves": int(moves),
            "outcome": outcome_str,
            "solved": is_victory,
            "summary": f"Base {cls.BASE_SCORE:,} - Time Penalty {time_penalty:,} ({elapsed}s × 10) = {total_score:,}" if is_victory else f"Outcome: {outcome_str.upper()} (0 pts)"
        }

    @classmethod
    def calculate_score(cls, game: str, **kwargs) -> Dict[str, Any]:
        """Universal router for deterministic game scoring."""
        g = str(game).lower()
        if "sudoku" in g:
            return cls.calculate_sudoku_score(**kwargs)
        elif "sokoban" in g:
            return cls.calculate_sokoban_score(**kwargs)
        elif "laser" in g:
            return cls.calculate_laser_score(**kwargs)
        elif "minesweeper" in g:
            return cls.calculate_minesweeper_score(**kwargs)
        elif "battle" in g:
            return cls.calculate_battle_score(**kwargs)
        else:
            elapsed = max(0, int(kwargs.get("time_seconds", kwargs.get("elapsed_seconds", 0))))
            solved = bool(kwargs.get("solved", True))
            total_score = cls.compute_formula(elapsed, solved=solved)
            time_penalty = elapsed * cls.TIME_PENALTY_PER_SECOND if solved else 0
            return {
                "game": g,
                "total_score": total_score,
                "base_score": cls.BASE_SCORE if solved else 0,
                "time_penalty": time_penalty,
                "elapsed_seconds": elapsed,
                "difficulty": str(kwargs.get("difficulty", "medium")).lower(),
                "difficulty_multiplier": 1.0,
                "solved": solved,
                "summary": f"Base {cls.BASE_SCORE:,} - Time Penalty {time_penalty:,} = {total_score:,}" if solved else "Incomplete (0 pts)"
            }

