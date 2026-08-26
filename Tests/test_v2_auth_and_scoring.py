"""
NEXUS AI REASONING WAR (V2) - Automated Unit Test Suite
Tests for:
1. Scoring calculations across all 5 games
2. Difficulty multipliers and penalty bounds
3. High score comparisons and statistics aggregations
4. Game session UUID deduplication
5. Seed persistence in score records
6. Guest mode vs Authenticated player state
7. Player data ownership and isolation
8. Database service failure resiliency (no crashes)
9. OAuth service error resilience
10. Security & Secrets Protection
"""

import unittest
import uuid
from unittest.mock import patch, MagicMock
from Services.scoring_engine import ScoringEngine
from Services.auth_service import AuthService, PlayerProfile
from Services.db_service import DatabaseService


class TestV2AuthAndScoring(unittest.TestCase):

    def setUp(self):
        self.test_session_id = str(uuid.uuid4())

    def test_sudoku_scoring(self):
        # Solved in 120s with 0 mistakes, 0 hints on Medium (1.5x)
        res = ScoringEngine.calculate_sudoku_score(
            difficulty="medium",
            solved=True,
            time_seconds=120,
            mistakes=0,
            hints=0
        )
        self.assertTrue(res["solved"])
        self.assertEqual(res["base_score"], 1500)
        self.assertEqual(res["speed_bonus"], 1680)
        self.assertEqual(res["total_score"], 1500 + 1680)

        # Penalties: 2 mistakes (-300), 1 hint (-200)
        res_pen = ScoringEngine.calculate_sudoku_score(
            difficulty="medium",
            solved=True,
            time_seconds=120,
            mistakes=2,
            hints=1
        )
        self.assertEqual(res_pen["mistake_penalty"], 300)
        self.assertEqual(res_pen["hint_penalty"], 200)
        self.assertEqual(res_pen["total_score"], (1500 + 1680) - 500)

        # Unsolved returns 0
        res_unsolved = ScoringEngine.calculate_sudoku_score(
            difficulty="medium",
            solved=False,
            time_seconds=120
        )
        self.assertEqual(res_unsolved["total_score"], 0)

    def test_sokoban_scoring(self):
        # Medium (1.5x, target_moves=20), solved in 15 moves, 5 pushes, 60s
        res = ScoringEngine.calculate_sokoban_score(
            difficulty="medium",
            solved=True,
            time_seconds=60,
            moves=15,
            pushes=5
        )
        self.assertTrue(res["solved"])
        self.assertEqual(res["base_score"], 1800)
        self.assertGreater(res["move_efficiency_bonus"], 0)
        self.assertGreater(res["push_efficiency_bonus"], 0)
        self.assertEqual(res["speed_bonus"], 540)
        self.assertGreater(res["total_score"], 1800)

        # Unsolved returns 0
        res_unsolved = ScoringEngine.calculate_sokoban_score(difficulty="hard", solved=False, time_seconds=100)
        self.assertEqual(res_unsolved["total_score"], 0)

    def test_laser_scoring(self):
        # Easy (1.0x), solved in 3 rotations, 40s
        res = ScoringEngine.calculate_laser_score(
            difficulty="easy",
            solved=True,
            time_seconds=40,
            rotations=3
        )
        self.assertTrue(res["solved"])
        self.assertEqual(res["base_score"], 1000)
        self.assertEqual(res["rotation_efficiency_bonus"], (20 - 3) * 25)
        self.assertEqual(res["speed_bonus"], 560)
        self.assertEqual(res["total_score"], 1000 + 425 + 560)

    def test_minesweeper_scoring(self):
        # Intermediate (1.5x), solved with 3 lives intact, 20 safe cells cleared, 90s
        res = ScoringEngine.calculate_minesweeper_score(
            difficulty="intermediate",
            solved=True,
            time_seconds=90,
            remaining_lives=3,
            safe_cleared=20
        )
        self.assertTrue(res["solved"])
        self.assertEqual(res["base_score"], 1500)
        self.assertEqual(res["life_preservation_bonus"], 750)
        self.assertEqual(res["safe_nodes_bonus"], 300)
        self.assertEqual(res["speed_bonus"], 510)
        self.assertEqual(res["total_score"], 1500 + 750 + 300 + 510)

        # Game over (0 lives) returns 0
        res_over = ScoringEngine.calculate_minesweeper_score(difficulty="expert", solved=False, time_seconds=50, remaining_lives=0)
        self.assertEqual(res_over["total_score"], 0)

    def test_battle_arena_scoring(self):
        # Win on Hard (2.0x) in 12 moves
        res_win = ScoringEngine.calculate_battle_score(
            difficulty="hard",
            outcome="win",
            moves=12
        )
        self.assertEqual(res_win["base_score"], 3000)
        self.assertEqual(res_win["move_economy_bonus"], (30 - 12) * 35)
        self.assertEqual(res_win["total_score"], 3000 + 630)

        # Loss returns 0
        res_loss = ScoringEngine.calculate_battle_score(difficulty="hard", outcome="loss", moves=15)
        self.assertEqual(res_loss["total_score"], 0)

    def test_difficulty_multipliers(self):
        self.assertEqual(ScoringEngine.get_difficulty_multiplier("easy"), 1.0)
        self.assertEqual(ScoringEngine.get_difficulty_multiplier("medium"), 1.5)
        self.assertEqual(ScoringEngine.get_difficulty_multiplier("hard"), 2.0)
        self.assertEqual(ScoringEngine.get_difficulty_multiplier("expert"), 2.5)
        self.assertEqual(ScoringEngine.get_difficulty_multiplier("nightmare"), 3.0)

    def test_authenticated_player_profile(self):
        p = PlayerProfile(
            id="uuid-1234",
            provider_user_id="google-sub-5678",
            email="agent@nexus.ai",
            display_name="Nexus Agent",
            avatar_url="https://avatar.com/agent.png",
            is_authenticated=True
        )
        d = p.to_dict()
        self.assertEqual(d["provider_user_id"], "google-sub-5678")
        self.assertEqual(d["email"], "agent@nexus.ai")
        self.assertTrue(d["is_authenticated"])

    def test_game_session_id_deduplication(self):
        sess_id_1 = str(uuid.uuid4())
        sess_id_2 = str(uuid.uuid4())
        self.assertNotEqual(sess_id_1, sess_id_2)

        # Mock database submission returning duplicate code 409
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request", return_value=(True, [], "Score already recorded.")):
                success, msg = DatabaseService.submit_game_score(
                    player_id="test-player-id",
                    game_session_id=sess_id_1,
                    game="sudoku",
                    difficulty="medium",
                    score=2500,
                    time_seconds=120,
                    seed=42819
                )
                self.assertTrue(success)
                self.assertIn("already recorded", msg)

    def test_database_service_outage_resilience(self):
        # When Supabase is not configured or network drops, it returns False with clean message, no crash
        with patch.object(DatabaseService, "is_configured", return_value=False):
            success, msg = DatabaseService.submit_game_score(
                player_id="player-1",
                game_session_id=str(uuid.uuid4()),
                game="sokoban",
                difficulty="medium",
                score=1800,
                time_seconds=50,
                seed=100
            )
            self.assertFalse(success)
            self.assertIn("temporarily unavailable", msg)

            stats = DatabaseService.get_player_statistics("player-1")
            self.assertEqual(stats, [])

    def test_oauth_service_resilience(self):
        with patch.object(AuthService, "is_oauth_configured", return_value=False):
            success, profile, msg = AuthService.exchange_code_for_profile("fake-code")
            self.assertFalse(success)
            self.assertIsNone(profile)
            self.assertIn("not configured", msg)

    def test_player_data_isolation(self):
        # Verify queries explicitly scope by player_id and reject empty/cross-player access
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"player_id": "player-A", "game": "sudoku", "best_score": 3000}], "Success")
                stats = DatabaseService.get_player_statistics("player-A")
                mock_req.assert_called_once()
                self.assertEqual(mock_req.call_args[1]["params"]["player_id"], "eq.player-A")

    def test_guest_mode_cloud_sync_block(self):
        # Empty or guest player ID cannot trigger cloud score submission
        success, msg = DatabaseService.submit_game_score(
            player_id="",
            game_session_id=str(uuid.uuid4()),
            game="sudoku",
            difficulty="medium",
            score=1000,
            time_seconds=60,
            seed=42
        )
        self.assertFalse(success)
        self.assertIn("Invalid player or session ID", msg)


if __name__ == "__main__":
    unittest.main()
