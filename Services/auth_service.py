"""
NEXUS AI REASONING WAR (V2) - Authentication Service
Provides secure Google OAuth2 / OpenID Connect authentication and Streamlit session management.
Zero hardcoded secrets. Production only recognizes authenticated Google accounts or guest users.
"""

from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import urllib.request
import urllib.parse
import json
import os
import streamlit as st


@dataclass
class PlayerProfile:
    id: Optional[str]
    provider_user_id: str
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    is_authenticated: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "provider_user_id": self.provider_user_id,
            "email": self.email,
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "is_authenticated": self.is_authenticated
        }


class AuthService:
    """Manages Google OAuth2 / OpenID Connect authentication and player sessions."""

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    @classmethod
    def get_oauth_config(cls) -> Dict[str, str]:
        """Reads OAuth credentials safely from st.secrets or environment variables."""
        client_id = ""
        client_secret = ""
        redirect_uri = ""

        # Check st.secrets first
        try:
            if hasattr(st, "secrets"):
                if "GOOGLE_CLIENT_ID" in st.secrets:
                    client_id = str(st.secrets["GOOGLE_CLIENT_ID"])
                elif "auth" in st.secrets and "google_client_id" in st.secrets["auth"]:
                    client_id = str(st.secrets["auth"]["google_client_id"])

                if "GOOGLE_CLIENT_SECRET" in st.secrets:
                    client_secret = str(st.secrets["GOOGLE_CLIENT_SECRET"])
                elif "auth" in st.secrets and "google_client_secret" in st.secrets["auth"]:
                    client_secret = str(st.secrets["auth"]["google_client_secret"])

                if "REDIRECT_URI" in st.secrets:
                    redirect_uri = str(st.secrets["REDIRECT_URI"])
                elif "auth" in st.secrets and "redirect_uri" in st.secrets["auth"]:
                    redirect_uri = str(st.secrets["auth"]["redirect_uri"])
        except Exception:
            pass

        # Fallback to environment variables
        if not client_id:
            client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        if not client_secret:
            client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
        if not redirect_uri:
            redirect_uri = os.environ.get("REDIRECT_URI", "http://localhost:8501")

        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }

    @classmethod
    def is_oauth_configured(cls) -> bool:
        cfg = cls.get_oauth_config()
        return bool(cfg["client_id"] and cfg["client_secret"])

    @classmethod
    def get_google_auth_url(cls, state: str = "nexus_auth") -> Optional[str]:
        """Generates the Google OAuth2 authorization URL."""
        cfg = cls.get_oauth_config()
        if not cfg["client_id"]:
            return None

        params = {
            "client_id": cfg["client_id"],
            "redirect_uri": cfg["redirect_uri"],
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "online",
            "state": state,
            "prompt": "select_account"
        }
        return f"{cls.GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

    @classmethod
    def exchange_code_for_profile(cls, code: str) -> Tuple[bool, Optional[PlayerProfile], str]:
        """Exchanges authorization code for Google profile data using standard HTTPS request."""
        cfg = cls.get_oauth_config()
        if not cfg["client_id"] or not cfg["client_secret"]:
            return False, None, "Google OAuth is not configured on this deployment."

        try:
            # 1. Exchange code for access token
            token_data = urllib.parse.urlencode({
                "code": code,
                "client_id": cfg["client_id"],
                "client_secret": cfg["client_secret"],
                "redirect_uri": cfg["redirect_uri"],
                "grant_type": "authorization_code"
            }).encode("utf-8")

            req = urllib.request.Request(
                cls.GOOGLE_TOKEN_URL,
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                token_resp = json.loads(resp.read().decode("utf-8"))
                access_token = token_resp.get("access_token")

            if not access_token:
                return False, None, "Failed to retrieve access token from Google."

            # 2. Fetch userinfo
            userinfo_req = urllib.request.Request(
                cls.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            with urllib.request.urlopen(userinfo_req, timeout=10) as resp:
                user_data = json.loads(resp.read().decode("utf-8"))

            provider_id = user_data.get("id") or user_data.get("sub")
            email = user_data.get("email")
            display_name = user_data.get("name") or (email.split("@")[0] if email else "Agent")
            avatar_url = user_data.get("picture")

            if not provider_id or not email:
                return False, None, "Incomplete profile payload returned from identity provider."

            profile = PlayerProfile(
                id=None,
                provider_user_id=str(provider_id),
                email=str(email),
                display_name=str(display_name),
                avatar_url=avatar_url,
                is_authenticated=True
            )
            return True, profile, "Authentication successful."

        except Exception as ex:
            return False, None, f"OAuth token exchange error: {str(ex)}"

    @classmethod
    def check_streamlit_native_auth(cls) -> Optional[PlayerProfile]:
        """Checks for Streamlit 1.39+ Native Auth (st.user)."""
        try:
            if hasattr(st, "user") and st.user is not None:
                if getattr(st.user, "is_logged_in", False):
                    email = getattr(st.user, "email", None) or "agent@nexus.ai"
                    provider_id = getattr(st.user, "id", None) or getattr(st.user, "sub", None) or email
                    name = getattr(st.user, "name", None) or email.split("@")[0]
                    picture = getattr(st.user, "picture", None) or getattr(st.user, "avatar_url", None)
                    return PlayerProfile(
                        id=None,
                        provider_user_id=str(provider_id),
                        email=str(email),
                        display_name=str(name),
                        avatar_url=picture,
                        is_authenticated=True
                    )
        except Exception:
            pass
        return None

    @classmethod
    def get_current_user(cls) -> Optional[PlayerProfile]:
        """Retrieves active authenticated player from Streamlit session state or native auth."""
        # 1. Check session state
        if "authenticated_player" in st.session_state and st.session_state.authenticated_player:
            player_dict = st.session_state.authenticated_player
            return PlayerProfile(
                id=player_dict.get("id"),
                provider_user_id=player_dict.get("provider_user_id", ""),
                email=player_dict.get("email", ""),
                display_name=player_dict.get("display_name", "Agent"),
                avatar_url=player_dict.get("avatar_url"),
                is_authenticated=player_dict.get("is_authenticated", True)
            )

        # 2. Check native auth
        native_user = cls.check_streamlit_native_auth()
        if native_user:
            st.session_state.authenticated_player = native_user.to_dict()
            return native_user

        return None

    @classmethod
    def set_authenticated_user(cls, profile: PlayerProfile):
        """Stores authenticated player profile in session state."""
        st.session_state.authenticated_player = profile.to_dict()

    @classmethod
    def logout(cls):
        """Clears authenticated session and resets to guest mode."""
        if "authenticated_player" in st.session_state:
            del st.session_state.authenticated_player
        try:
            if hasattr(st, "logout"):
                st.logout()
        except Exception:
            pass
