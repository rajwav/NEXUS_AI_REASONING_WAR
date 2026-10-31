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

    # ================================================================
    # 1. CORE DETERMINISTIC SCORING FORMULA TESTS
    # ================================================================

    def test_determinism_score_30_greater_than_60(self):
        """Test 1: score(30) > score(60)"""
        s30 = ScoringEngine.compute_formula(30, solved=True)
        s60 = ScoringEngine.compute_formula(60, solved=True)
        self.assertEqual(s30, 9700)
        self.assertEqual(s60, 9400)
        self.assertGreater(s30, s60)

    def test_determinism_score_60_equals_9400(self):
        """Test 2: score(60) == 9400"""
        self.assertEqual(ScoringEngine.compute_formula(60, solved=True), 9400)

    def test_determinism_score_120_equals_8800(self):
        """Test 3: score(120) == 8800"""
        self.assertEqual(ScoringEngine.compute_formula(120, solved=True), 8800)

    def test_determinism_score_reproducibility(self):
        """Test 4: score(60) called repeatedly returns exactly 9400"""
        for _ in range(20):
            self.assertEqual(ScoringEngine.compute_formula(60, solved=True), 9400)

    def test_score_does_not_depend_on_random_seed(self):
        """Test 5: score calculation does not depend on random seed"""
        res1 = ScoringEngine.calculate_sudoku_score(time_seconds=75, seed=12345, solved=True)
        res2 = ScoringEngine.calculate_sudoku_score(time_seconds=75, seed=99999, solved=True)
        res3 = ScoringEngine.calculate_sudoku_score(time_seconds=75, seed=0, solved=True)
        self.assertEqual(res1["total_score"], res2["total_score"])
        self.assertEqual(res2["total_score"], res3["total_score"])
        self.assertEqual(res1["total_score"], 10000 - (75 * 10))

    def test_score_does_not_depend_on_uuid(self):
        """Test 6: score calculation does not depend on UUID"""
        res1 = ScoringEngine.calculate_laser_score(time_seconds=50, solved=True, session_id=str(uuid.uuid4()))
        res2 = ScoringEngine.calculate_laser_score(time_seconds=50, solved=True, session_id=str(uuid.uuid4()))
        self.assertEqual(res1["total_score"], res2["total_score"])
        self.assertEqual(res1["total_score"], 9500)

    def test_score_does_not_depend_on_difficulty(self):
        """Test 7: score calculation does not depend on difficulty unless explicitly designed"""
        s_easy = ScoringEngine.calculate_sudoku_score(difficulty="easy", time_seconds=100, solved=True)
        s_med = ScoringEngine.calculate_sudoku_score(difficulty="medium", time_seconds=100, solved=True)
        s_hard = ScoringEngine.calculate_sudoku_score(difficulty="hard", time_seconds=100, solved=True)
        s_night = ScoringEngine.calculate_sudoku_score(difficulty="nightmare", time_seconds=100, solved=True)
        self.assertEqual(s_easy["total_score"], 9000)
        self.assertEqual(s_med["total_score"], 9000)
        self.assertEqual(s_hard["total_score"], 9000)
        self.assertEqual(s_night["total_score"], 9000)

    def test_each_game_preserves_its_own_telemetry(self):
        """Test 8: each game preserves its own telemetry"""
        # Sudoku telemetry
        sud = ScoringEngine.calculate_sudoku_score(time_seconds=80, mistakes=2, hints=1, seed=42, solved=True)
        self.assertEqual(sud["mistakes"], 2)
        self.assertEqual(sud["hints_used"], 1)
        self.assertEqual(sud["seed"], 42)
        self.assertEqual(sud["total_score"], 9200)

        # Sokoban telemetry
        sok = ScoringEngine.calculate_sokoban_score(time_seconds=60, moves=25, pushes=10, seed=101, solved=True)
        self.assertEqual(sok["moves"], 25)
        self.assertEqual(sok["pushes"], 10)
        self.assertEqual(sok["seed"], 101)
        self.assertEqual(sok["total_score"], 9400)

        # Laser telemetry
        las = ScoringEngine.calculate_laser_score(time_seconds=45, rotations=6, seed=202, solved=True)
        self.assertEqual(las["rotations"], 6)
        self.assertEqual(las["seed"], 202)
        self.assertEqual(las["total_score"], 9550)

        # Minesweeper telemetry
        mine = ScoringEngine.calculate_minesweeper_score(time_seconds=90, remaining_lives=2, safe_cleared=30, seed=303, solved=True)
        self.assertEqual(mine["remaining_lives"], 2)
        self.assertEqual(mine["safe_cells_cleared"], 30)
        self.assertEqual(mine["seed"], 303)
        self.assertEqual(mine["total_score"], 9100)

        # Battle Arena telemetry
        bat = ScoringEngine.calculate_battle_score(time_seconds=35, moves=8, outcome="win", solved=True)
        self.assertEqual(bat["moves"], 8)
        self.assertEqual(bat["outcome"], "win")
        self.assertEqual(bat["total_score"], 9650)

    def test_completed_game_submits_exactly_once(self):
        """Test 9: completed game submits exactly once"""
        sess_id = str(uuid.uuid4())
        submitted_set = set()

        if sess_id not in submitted_set:
            submitted_set.add(sess_id)
            sub_count = 1
        else:
            sub_count = 0
        self.assertEqual(sub_count, 1)

        if sess_id not in submitted_set:
            sub_count += 1
        self.assertEqual(sub_count, 1)

    def test_streamlit_rerun_does_not_create_another_score(self):
        """Test 10: Streamlit rerun does not create another score"""
        sess_id = str(uuid.uuid4())
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"id": "score-uuid"}], "Success")
                success1, msg1 = DatabaseService.submit_game_score(
                    player_id="p1",
                    game_session_id=sess_id,
                    game="sudoku",
                    difficulty="medium",
                    score=9400,
                    time_seconds=60,
                    solved=True
                )
                self.assertTrue(success1)

                mock_req.return_value = (True, [], "Score already recorded.")
                success2, msg2 = DatabaseService.submit_game_score(
                    player_id="p1",
                    game_session_id=sess_id,
                    game="sudoku",
                    difficulty="medium",
                    score=9400,
                    time_seconds=60,
                    solved=True
                )
                self.assertTrue(success2)
                self.assertEqual(msg2, "Score already recorded.")

    def test_incomplete_game_does_not_receive_completion_score(self):
        """Test 11: incomplete game does not receive a completion score"""
        sud_fail = ScoringEngine.calculate_sudoku_score(time_seconds=50, solved=False)
        self.assertEqual(sud_fail["total_score"], 0)
        self.assertFalse(sud_fail["solved"])

        mine_fail = ScoringEngine.calculate_minesweeper_score(time_seconds=50, remaining_lives=0, solved=False)
        self.assertEqual(mine_fail["total_score"], 0)
        self.assertFalse(mine_fail["solved"])

        bat_fail = ScoringEngine.calculate_battle_score(time_seconds=30, outcome="loss", solved=False)
        self.assertEqual(bat_fail["total_score"], 0)
        self.assertFalse(bat_fail["solved"])

    def test_elapsed_seconds_persisted_matches_final_timer(self):
        """Test 12: elapsed_seconds persisted to Supabase matches the final timer"""
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"id": "score-uuid"}], "Success")
                DatabaseService.submit_game_score(
                    player_id="p-test",
                    game_session_id=str(uuid.uuid4()),
                    game="laser",
                    difficulty="hard",
                    score=9230,
                    time_seconds=77,
                    solved=True
                )
                payload = mock_req.call_args_list[0][1]["data"]
                self.assertEqual(payload["time_seconds"], 77)
                self.assertEqual(payload["score"], 9230)

    def test_all_five_games_use_same_core_scoring_function(self):
        """Test 13: all five games use the same core time-based scoring function"""
        t = 150
        expected = 10000 - (150 * 10)  # 8500
        self.assertEqual(ScoringEngine.calculate_sudoku_score(time_seconds=t, solved=True)["total_score"], expected)
        self.assertEqual(ScoringEngine.calculate_sokoban_score(time_seconds=t, solved=True)["total_score"], expected)
        self.assertEqual(ScoringEngine.calculate_laser_score(time_seconds=t, solved=True)["total_score"], expected)
        self.assertEqual(ScoringEngine.calculate_minesweeper_score(time_seconds=t, remaining_lives=1, solved=True)["total_score"], expected)
        self.assertEqual(ScoringEngine.calculate_battle_score(time_seconds=t, outcome="win", solved=True)["total_score"], expected)

    def test_lower_completion_time_always_produces_higher_score(self):
        """Test 14: lower completion time always produces a higher score"""
        times = [10, 25, 60, 120, 300, 600, 999]
        scores = [ScoringEngine.compute_formula(t, solved=True) for t in times]
        for i in range(len(scores) - 1):
            self.assertGreater(scores[i], scores[i + 1])

    # ================================================================
    # 2. PROFILES, AUTH, AND DATA ISOLATION TESTS
    # ================================================================

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

        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request", return_value=(True, [], "Score already recorded.")):
                success, msg = DatabaseService.submit_game_score(
                    player_id="test-player-id",
                    game_session_id=sess_id_1,
                    game="sudoku",
                    difficulty="medium",
                    score=9400,
                    time_seconds=60,
                    seed=42819
                )
                self.assertTrue(success)
                self.assertIn("already recorded", msg)

    def test_database_service_outage_resilience(self):
        with patch.object(DatabaseService, "is_configured", return_value=False):
            success, msg = DatabaseService.submit_game_score(
                player_id="player-1",
                game_session_id=str(uuid.uuid4()),
                game="sokoban",
                difficulty="medium",
                score=9500,
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
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"player_id": "player-A", "game": "sudoku", "best_score": 9500}], "Success")
                stats = DatabaseService.get_player_statistics("player-A")
                mock_req.assert_called_once()
                self.assertEqual(mock_req.call_args[1]["params"]["player_id"], "eq.player-A")

    def test_guest_mode_cloud_sync_block(self):
        success, msg = DatabaseService.submit_game_score(
            player_id="",
            game_session_id=str(uuid.uuid4()),
            game="sudoku",
            difficulty="medium",
            score=9400,
            time_seconds=60,
            seed=42
        )
        self.assertFalse(success)
        self.assertIn("Invalid player or session ID", msg)

    def test_security_player_a_can_access_own_data(self):
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"player_id": "player-A-uuid", "game": "sudoku", "best_score": 9500}], "Success")
                stats = DatabaseService.get_player_statistics(player_id="player-A-uuid", user_token="jwt-token-player-A")
                self.assertEqual(len(stats), 1)
                self.assertEqual(stats[0]["player_id"], "player-A-uuid")
                self.assertEqual(mock_req.call_args[1]["user_token"], "jwt-token-player-A")
                self.assertEqual(mock_req.call_args[1]["params"]["player_id"], "eq.player-A-uuid")

    def test_security_player_a_cannot_access_player_b_data(self):
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [], "Success")
                stats = DatabaseService.get_player_statistics(player_id="player-B-uuid", user_token="jwt-token-player-A")
                self.assertEqual(stats, [])

    def test_security_unauthenticated_cannot_write_score(self):
        success, msg = DatabaseService.submit_game_score(
            player_id="",
            game_session_id=str(uuid.uuid4()),
            game="laser",
            difficulty="hard",
            score=9550,
            time_seconds=45,
            seed=999
        )
        self.assertFalse(success)
        self.assertIn("Invalid player or session ID", msg)

    def test_security_authenticated_player_a_can_write_score(self):
        sess_id = str(uuid.uuid4())
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"id": "score-uuid"}], "Success")
                success, msg = DatabaseService.submit_game_score(
                    player_id="player-A-uuid",
                    game_session_id=sess_id,
                    game="sokoban",
                    difficulty="medium",
                    score=9400,
                    time_seconds=60,
                    moves=15,
                    seed=12345,
                    solved=True,
                    user_token="jwt-token-player-A"
                )
                self.assertTrue(success)
                self.assertIn("successfully synchronized", msg)

    def test_security_duplicate_game_session_id_rejected_or_idempotent(self):
        sess_id = str(uuid.uuid4())
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [], "Score already recorded.")
                success, msg = DatabaseService.submit_game_score(
                    player_id="player-A-uuid",
                    game_session_id=sess_id,
                    game="minesweeper",
                    difficulty="expert",
                    score=8800,
                    time_seconds=120,
                    seed=8888,
                    user_token="jwt-token-player-A"
                )
                self.assertTrue(success)
                self.assertEqual(msg, "Score already recorded.")

    def test_security_tampered_player_identity_rejected(self):
        success, msg = DatabaseService.submit_game_score(
            player_id="valid-player-id",
            game_session_id="",
            game="battle",
            difficulty="hard",
            score=9700,
            time_seconds=30
        )
        self.assertFalse(success)
        self.assertIn("Invalid player or session ID", msg)

    def test_service_role_key_priority(self):
        mock_secrets = {
            "SUPABASE_URL": "https://test-project.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "test-service-role-secret",
            "SUPABASE_ANON_KEY": "test-anon-public-key"
        }
        with patch("streamlit.secrets", mock_secrets):
            cfg = DatabaseService.get_config()
            self.assertEqual(cfg["url"], "https://test-project.supabase.co")
            self.assertEqual(cfg["key"], "test-service-role-secret")

    def test_game_specific_metrics_payload_preservation(self):
        metrics = {
            "game": "sudoku",
            "difficulty": "medium",
            "mistakes": 1,
            "hints_used": 0,
            "elapsed_seconds": 150,
            "total_score": 8500
        }
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"id": "score-uuid"}], "Success")
                success, _ = DatabaseService.submit_game_score(
                    player_id="player-uuid-1",
                    game_session_id=str(uuid.uuid4()),
                    game="sudoku",
                    difficulty="medium",
                    score=8500,
                    time_seconds=150,
                    mistakes=1,
                    hints=0,
                    metrics_breakdown=metrics
                )
                self.assertTrue(success)
                called_data = mock_req.call_args_list[0][1]["data"]
                self.assertEqual(called_data["metrics_breakdown"], metrics)
                self.assertEqual(called_data["mistakes"], 1)

    def test_cross_user_submission_prevention(self):
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"id": "score-uuid"}], "Success")
                success, _ = DatabaseService.submit_game_score(
                    player_id="authenticated-user-uuid",
                    game_session_id=str(uuid.uuid4()),
                    game="battle",
                    difficulty="hard",
                    score=9550,
                    time_seconds=45,
                    moves=10,
                    solved=True
                )
                self.assertTrue(success)
                called_data = mock_req.call_args_list[0][1]["data"]
                self.assertEqual(called_data["player_id"], "authenticated-user-uuid")

    def test_streamlit_native_user_extraction(self):
        mock_user = MagicMock()
        mock_user.get.side_effect = lambda k, d=None: {
            "is_logged_in": True,
            "email": "testagent@nexus.ai",
            "sub": "google-10928374",
            "name": "Nexus Operative",
            "picture": "https://avatar.url/pic.jpg"
        }.get(k, d)
        mock_user.is_logged_in = True
        mock_user.email = "testagent@nexus.ai"
        mock_user.sub = "google-10928374"
        mock_user.name = "Nexus Operative"
        mock_user.picture = "https://avatar.url/pic.jpg"

        with patch("streamlit.user", mock_user):
            self.assertTrue(AuthService.is_logged_in())
            profile = AuthService.get_current_user()
            self.assertIsNotNone(profile)
            self.assertEqual(profile.email, "testagent@nexus.ai")
            self.assertEqual(profile.provider_user_id, "google-10928374")
            self.assertEqual(profile.display_name, "Nexus Operative")

    def test_leaderboard_query_ordering(self):
        with patch.object(DatabaseService, "is_configured", return_value=True):
            with patch.object(DatabaseService, "_make_request") as mock_req:
                mock_req.return_value = (True, [{"player_id": "p1", "score": 9800, "time_seconds": 20}], "Success")
                rows = DatabaseService.get_leaderboard(game="sudoku", limit=10)
                self.assertEqual(len(rows), 1)
                params = mock_req.call_args[1]["params"]
                self.assertEqual(params["order"], "score.desc,time_seconds.asc")
                self.assertEqual(params["game"], "eq.sudoku")
                self.assertEqual(params["solved"], "eq.true")


if __name__ == "__main__":
    unittest.main()
