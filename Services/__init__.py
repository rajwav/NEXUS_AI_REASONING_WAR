"""
NEXUS AI REASONING WAR (V2) - Services Package
Exports:
- ScoringEngine: Centralized scoring calculations for all 5 games
- AuthService: Google OAuth2 / OpenID Connect authentication and session management
- DatabaseService: Production Supabase PostgreSQL client with durable deduplication
"""

from .scoring_engine import ScoringEngine
from .auth_service import AuthService, PlayerProfile
from .db_service import DatabaseService

__all__ = ["ScoringEngine", "AuthService", "PlayerProfile", "DatabaseService"]
