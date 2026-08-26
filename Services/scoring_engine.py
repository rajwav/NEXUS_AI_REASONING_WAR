"""
NEXUS AI REASONING WAR (V2) - Centralized Game Scoring Engine
Calculates deterministic scores and itemized audit breakdowns for all 5 games:
1. Sudoku
2. Cyber Sokoban
3. Laser Mirror Routing
4. Circuit Minesweeper
5. Tactical Battle Arena
"""

from typing import Dict, Any, Optional


class ScoringEngine:
    """Centralized, deterministic scoring engine with game-specific formula rules."""

    DIFFICULTY_MULTIPLIERS = {
        "easy": 1.0,
        "beginner": 1.0,
        "medium": 1.5,
        "intermediate": 1.5,
        "hard": 2.0,
        "expert": 2.5,
        "nightmare": 3.0
    }

    @classmethod
    def get_difficulty_multiplier(cls, difficulty: str) -> float:
        return cls.DIFFICULTY_MULTIPLIERS.get(str(difficulty).lower(), 1.0)

    @classmethod
    def calculate_sudoku_score(cls,
                               difficulty: str,
                               solved: bool,
                               time_seconds: int,
                               mistakes: int = 0,
                               hints: int = 0,
                               **kwargs) -> Dict[str, Any]:
        mult = cls.get_difficulty_multiplier(difficulty)
        if not solved:
            return {
                "total_score": 0,
                "base_score": 0,
                "difficulty_multiplier": mult,
                "speed_bonus": 0,
                "efficiency_bonus": 0,
                "mistake_penalty": 0,
                "hint_penalty": 0,
                "solved": False,
                "summary": "Puzzle not completed."
            }

        base = int(1000 * mult)
        speed_bonus = max(0, int(1800 - time_seconds))
        mistake_penalty = int(mistakes * 150)
        hint_penalty = int(hints * 200)

        total = max(0, base + speed_bonus - mistake_penalty - hint_penalty)
        return {
            "total_score": total,
            "base_score": base,
            "difficulty_multiplier": mult,
            "speed_bonus": speed_bonus,
            "efficiency_bonus": 0,
            "mistake_penalty": mistake_penalty,
            "hint_penalty": hint_penalty,
            "solved": True,
            "summary": f"Base {base} + Speed {speed_bonus} - Mistakes {mistake_penalty} - Hints {hint_penalty}"
        }

    @classmethod
    def calculate_sokoban_score(cls,
                                difficulty: str,
                                solved: bool,
                                time_seconds: int,
                                moves: int = 0,
                                pushes: int = 0,
                                **kwargs) -> Dict[str, Any]:
        mult = cls.get_difficulty_multiplier(difficulty)
        if not solved:
            return {
                "total_score": 0,
                "base_score": 0,
                "difficulty_multiplier": mult,
                "speed_bonus": 0,
                "move_efficiency_bonus": 0,
                "push_efficiency_bonus": 0,
                "solved": False,
                "summary": "Warehouse puzzle not completed."
            }

        base = int(1200 * mult)
        target_moves = {"easy": 10, "medium": 20, "hard": 30, "expert": 40, "nightmare": 50}.get(str(difficulty).lower(), 20)
        move_efficiency = max(0, int((target_moves * 2 - moves) * 20))
        push_efficiency = max(0, int((target_moves - pushes) * 15))
        speed_bonus = max(0, int(600 - time_seconds))

        total = max(0, base + move_efficiency + push_efficiency + speed_bonus)
        return {
            "total_score": total,
            "base_score": base,
            "difficulty_multiplier": mult,
            "speed_bonus": speed_bonus,
            "move_efficiency_bonus": move_efficiency,
            "push_efficiency_bonus": push_efficiency,
            "solved": True,
            "summary": f"Base {base} + MoveEff {move_efficiency} + PushEff {push_efficiency} + Speed {speed_bonus}"
        }

    @classmethod
    def calculate_laser_score(cls,
                              difficulty: str,
                              solved: bool,
                              time_seconds: int,
                              rotations: int = 0,
                              **kwargs) -> Dict[str, Any]:
        mult = cls.get_difficulty_multiplier(difficulty)
        if not solved:
            return {
                "total_score": 0,
                "base_score": 0,
                "difficulty_multiplier": mult,
                "speed_bonus": 0,
                "rotation_efficiency_bonus": 0,
                "solved": False,
                "summary": "Laser matrix not energized."
            }

        base = int(1000 * mult)
        rotation_efficiency = max(0, int((20 - rotations) * 25))
        speed_bonus = max(0, int(600 - time_seconds))

        total = max(0, base + rotation_efficiency + speed_bonus)
        return {
            "total_score": total,
            "base_score": base,
            "difficulty_multiplier": mult,
            "speed_bonus": speed_bonus,
            "rotation_efficiency_bonus": rotation_efficiency,
            "solved": True,
            "summary": f"Base {base} + RotationEff {rotation_efficiency} + Speed {speed_bonus}"
        }

    @classmethod
    def calculate_minesweeper_score(cls,
                                    difficulty: str,
                                    solved: bool,
                                    time_seconds: int,
                                    remaining_lives: int = 3,
                                    safe_cleared: int = 0,
                                    **kwargs) -> Dict[str, Any]:
        mult = cls.get_difficulty_multiplier(difficulty)
        if not solved or remaining_lives <= 0:
            return {
                "total_score": 0,
                "base_score": 0,
                "difficulty_multiplier": mult,
                "speed_bonus": 0,
                "life_preservation_bonus": 0,
                "safe_nodes_bonus": 0,
                "solved": False,
                "summary": "Circuit breaker overloaded (0 lives remaining)."
            }

        base = int(1000 * mult)
        life_bonus = int(remaining_lives * 250)
        safe_nodes_bonus = int(safe_cleared * 15)
        speed_bonus = max(0, int(600 - time_seconds))

        total = max(0, base + life_bonus + safe_nodes_bonus + speed_bonus)
        return {
            "total_score": total,
            "base_score": base,
            "difficulty_multiplier": mult,
            "speed_bonus": speed_bonus,
            "life_preservation_bonus": life_bonus,
            "safe_nodes_bonus": safe_nodes_bonus,
            "solved": True,
            "summary": f"Base {base} + Lives {life_bonus} + SafeCleared {safe_nodes_bonus} + Speed {speed_bonus}"
        }

    @classmethod
    def calculate_battle_score(cls,
                               difficulty: str,
                               outcome: str,
                               moves: int = 0,
                               time_seconds: int = 0,
                               **kwargs) -> Dict[str, Any]:
        mult = cls.get_difficulty_multiplier(difficulty)
        outcome_str = str(outcome).lower()
        if outcome_str in ("loss", "defeat", "ai_win"):
            return {
                "total_score": 0,
                "base_score": 0,
                "difficulty_multiplier": mult,
                "move_economy_bonus": 0,
                "outcome": "loss",
                "solved": False,
                "summary": "Defeated by AEGIS Tactical AI."
            }

        if outcome_str in ("draw", "stalemate"):
            base = int(500 * mult)
            move_economy = max(0, int((30 - moves) * 15))
            total = base + move_economy
            return {
                "total_score": total,
                "base_score": base,
                "difficulty_multiplier": mult,
                "move_economy_bonus": move_economy,
                "outcome": "draw",
                "solved": True,
                "summary": f"Draw Base {base} + MoveEconomy {move_economy}"
            }

        # Win
        base = int(1500 * mult)
        move_economy = max(0, int((30 - moves) * 35))
        total = base + move_economy
        return {
            "total_score": total,
            "base_score": base,
            "difficulty_multiplier": mult,
            "move_economy_bonus": move_economy,
            "outcome": "win",
            "solved": True,
            "summary": f"Victory Base {base} + MoveEconomy {move_economy}"
        }

    @classmethod
    def calculate_score(cls, game: str, **kwargs) -> Dict[str, Any]:
        """Routes to the game-specific scoring calculation."""
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
            mult = cls.get_difficulty_multiplier(kwargs.get("difficulty", "medium"))
            base = int(1000 * mult) if kwargs.get("solved", False) else 0
            return {
                "total_score": base,
                "base_score": base,
                "difficulty_multiplier": mult,
                "solved": kwargs.get("solved", False),
                "summary": f"Standard calculation: {base}"
            }
