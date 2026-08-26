"""
NEXUS AI REASONING WAR (V2) - Database Service
Production persistence client for Supabase PostgreSQL (PostgREST).
Features:
- Pure Python standard library HTTP requests (urllib.request)
- Strict player data isolation
- Idempotent deduplication via UNIQUE(game_session_id)
- Zero silent SQLite fallback for authenticated production users
- Graceful error responses without uncaught runtime exceptions
"""

from typing import Dict, Any, Optional, List, Tuple
import urllib.request
import urllib.parse
import json
import os
import streamlit as st


class DatabaseService:
    """Manages player profiles, scores, and statistics in Supabase PostgreSQL."""

    @classmethod
    def get_config(cls) -> Dict[str, str]:
        """Reads Supabase credentials safely from st.secrets or environment."""
        url = ""
        key = ""

        try:
            if hasattr(st, "secrets"):
                if "SUPABASE_URL" in st.secrets:
                    url = str(st.secrets["SUPABASE_URL"])
                elif "supabase" in st.secrets and "url" in st.secrets["supabase"]:
                    url = str(st.secrets["supabase"]["url"])

                if "SUPABASE_KEY" in st.secrets:
                    key = str(st.secrets["SUPABASE_KEY"])
                elif "SUPABASE_ANON_KEY" in st.secrets:
                    key = str(st.secrets["SUPABASE_ANON_KEY"])
                elif "supabase" in st.secrets and "key" in st.secrets["supabase"]:
                    key = str(st.secrets["supabase"]["key"])
        except Exception:
            pass

        if not url:
            url = os.environ.get("SUPABASE_URL", "")
        if not key:
            key = os.environ.get("SUPABASE_KEY", os.environ.get("SUPABASE_ANON_KEY", ""))

        url = url.rstrip("/")
        return {"url": url, "key": key}

    @classmethod
    def is_configured(cls) -> bool:
        cfg = cls.get_config()
        return bool(cfg["url"] and cfg["key"])

    @classmethod
    def _make_request(cls,
                      endpoint: str,
                      method: str = "GET",
                      data: Optional[Dict[str, Any]] = None,
                      params: Optional[Dict[str, str]] = None,
                      headers_extra: Optional[Dict[str, str]] = None) -> Tuple[bool, Any, str]:
        """Executes an authenticated HTTP request to the Supabase PostgREST API."""
        cfg = cls.get_config()
        if not cfg["url"] or not cfg["key"]:
            return False, None, "Cloud score synchronization is temporarily unavailable (database not configured)."

        url = f"{cfg['url']}/rest/v1/{endpoint.lstrip('/')}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        headers = {
            "apikey": cfg["key"],
            "Authorization": f"Bearer {cfg['key']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if headers_extra:
            headers.update(headers_extra)

        body_bytes = json.dumps(data).encode("utf-8") if data is not None else None

        try:
            req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                resp_text = response.read().decode("utf-8")
                result_data = json.loads(resp_text) if resp_text else []
                return True, result_data, "Success"
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8") if he.fp else ""
            # If duplicate game_session_id (Postgres 23505 Unique Violation), treat as idempotent success
            if he.code == 409 or "23505" in err_body or "duplicate key" in err_body:
                return True, [], "Score already recorded."
            return False, None, f"Database HTTP Error {he.code}: {err_body[:200]}"
        except Exception as ex:
            return False, None, f"Database connection error: {str(ex)}"

    @classmethod
    def sync_player_profile(cls,
                            provider_user_id: str,
                            email: str,
                            display_name: str,
                            avatar_url: Optional[str] = None) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """Upserts a player profile in Supabase by provider_user_id and returns the player record with UUID."""
        if not cls.is_configured():
            return False, None, "Cloud score synchronization is temporarily unavailable."

        # 1. Look up existing player
        success, records, msg = cls._make_request(
            "players",
            method="GET",
            params={"provider_user_id": f"eq.{provider_user_id}", "select": "*"}
        )
        if success and records and isinstance(records, list) and len(records) > 0:
            player = records[0]
            # Update last_login, display_name, avatar_url
            cls._make_request(
                f"players?provider_user_id=eq.{provider_user_id}",
                method="PATCH",
                data={
                    "display_name": display_name,
                    "avatar_url": avatar_url,
                    "last_login": "now()"
                }
            )
            return True, player, "Profile synchronized."

        # 2. Insert new player
        insert_data = {
            "provider_user_id": provider_user_id,
            "email": email,
            "display_name": display_name,
            "avatar_url": avatar_url
        }
        success, inserted, msg = cls._make_request(
            "players",
            method="POST",
            data=insert_data,
            headers_extra={"Prefer": "return=representation"}
        )
        if success and inserted and isinstance(inserted, list) and len(inserted) > 0:
            return True, inserted[0], "Profile created."

        return False, None, f"Failed to sync player profile: {msg}"

    @classmethod
    def submit_game_score(cls,
                          player_id: str,
                          game_session_id: str,
                          game: str,
                          difficulty: str,
                          score: int,
                          time_seconds: int,
                          moves: int = 0,
                          mistakes: int = 0,
                          hints: int = 0,
                          seed: int = 0,
                          solved: bool = True,
                          metrics_breakdown: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """
        Durable score submission with database-level UNIQUE(game_session_id) deduplication.
        Also updates aggregated statistics for the player and game.
        """
        if not player_id or not game_session_id:
            return False, "Invalid player or session ID."

        if not cls.is_configured():
            return False, "Cloud score synchronization is temporarily unavailable."

        score_record = {
            "player_id": player_id,
            "game_session_id": str(game_session_id),
            "game": str(game).lower(),
            "difficulty": str(difficulty).lower(),
            "score": int(score),
            "time_seconds": int(time_seconds),
            "moves": int(moves),
            "mistakes": int(mistakes),
            "hints": int(hints),
            "seed": int(seed),
            "solved": bool(solved),
            "metrics_breakdown": metrics_breakdown or {}
        }

        # 1. Insert score into game_scores
        success, _, msg = cls._make_request(
            "game_scores",
            method="POST",
            data=score_record,
            headers_extra={"Prefer": "return=minimal"}
        )
        if "already recorded" in msg:
            return True, "Score already recorded."
        if not success:
            return False, msg

        # 2. Update aggregated game_statistics
        cls._update_game_statistics(player_id, game, score, time_seconds, moves, solved)
        return True, "Score successfully synchronized to cloud."

    @classmethod
    def _update_game_statistics(cls,
                                player_id: str,
                                game: str,
                                score: int,
                                time_seconds: int,
                                moves: int,
                                solved: bool):
        """Updates or creates aggregated stats for a player and game."""
        game_norm = str(game).lower()
        success, existing, _ = cls._make_request(
            "game_statistics",
            method="GET",
            params={"player_id": f"eq.{player_id}", "game": f"eq.{game_norm}", "select": "*"}
        )

        if success and existing and isinstance(existing, list) and len(existing) > 0:
            current = existing[0]
            played = current.get("games_played", 0) + 1
            won = current.get("games_won", 0) + (1 if solved else 0)
            best_sc = max(current.get("best_score", 0), score)
            best_tm = min(current.get("best_time", 999999), time_seconds) if time_seconds > 0 else current.get("best_time", 0)
            best_mv = min(current.get("best_moves", 999999), moves) if moves > 0 else current.get("best_moves", 0)
            tot_sc = current.get("total_score", 0) + score

            cls._make_request(
                f"game_statistics?player_id=eq.{player_id}&game=eq.{game_norm}",
                method="PATCH",
                data={
                    "games_played": played,
                    "games_won": won,
                    "best_score": best_sc,
                    "best_time": best_tm if best_tm != 999999 else 0,
                    "best_moves": best_mv if best_mv != 999999 else 0,
                    "total_score": tot_sc,
                    "updated_at": "now()"
                }
            )
        else:
            cls._make_request(
                "game_statistics",
                method="POST",
                data={
                    "player_id": player_id,
                    "game": game_norm,
                    "games_played": 1,
                    "games_won": 1 if solved else 0,
                    "best_score": score,
                    "best_time": time_seconds,
                    "best_moves": moves,
                    "total_score": score
                }
            )

    @classmethod
    def get_player_statistics(cls, player_id: str) -> List[Dict[str, Any]]:
        """Retrieves lifetime game statistics for the authenticated player."""
        if not cls.is_configured() or not player_id:
            return []

        success, stats, _ = cls._make_request(
            "game_statistics",
            method="GET",
            params={"player_id": f"eq.{player_id}", "select": "*"}
        )
        return stats if success and isinstance(stats, list) else []

    @classmethod
    def get_player_high_scores(cls, player_id: str) -> Dict[str, Any]:
        """Returns aggregated high scores across all games for the player."""
        stats = cls.get_player_statistics(player_id)
        result = {
            "total_score": sum(s.get("total_score", 0) for s in stats),
            "games_played": sum(s.get("games_played", 0) for s in stats),
            "games_won": sum(s.get("games_won", 0) for s in stats),
            "games": {}
        }
        for s in stats:
            g = s.get("game", "unknown")
            result["games"][g] = {
                "best_score": s.get("best_score", 0),
                "best_time": s.get("best_time", 0),
                "best_moves": s.get("best_moves", 0),
                "games_played": s.get("games_played", 0),
                "games_won": s.get("games_won", 0)
            }
        return result

    @classmethod
    def get_player_recent_scores(cls, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns the most recent game score history for the authenticated player."""
        if not cls.is_configured() or not player_id:
            return []

        success, scores, _ = cls._make_request(
            "game_scores",
            method="GET",
            params={"player_id": f"eq.{player_id}", "order": "created_at.desc", "limit": str(limit), "select": "*"}
        )
        return scores if success and isinstance(scores, list) else []
