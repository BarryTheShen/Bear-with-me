"""Runtime configuration with fail-closed production secrets."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass

from .errors import ConfigurationError


@dataclass(frozen=True)
class Settings:
    database_path: str
    base_url: str
    web_origin: str
    master_key: bytes
    platform_admin_token: str
    session_ttl_seconds: int = 60 * 60 * 24 * 14
    finder_session_ttl_seconds: int = 60 * 60 * 24 * 7
    push_url: str = "https://exp.host/--/api/v2/push/send"
    livekit_url: str = ""
    livekit_api_key: str = ""
    livekit_api_secret: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        raw_key = os.environ.get("BEARWITHME_MASTER_KEY", "")
        if not raw_key:
            raise ConfigurationError(
                "BEARWITHME_MASTER_KEY must be a base64-encoded 32-byte key"
            )
        try:
            key = base64.urlsafe_b64decode(raw_key.encode("ascii"))
        except (ValueError, UnicodeEncodeError) as exc:
            raise ConfigurationError("BEARWITHME_MASTER_KEY is not valid base64") from exc
        if len(key) != 32:
            raise ConfigurationError("BEARWITHME_MASTER_KEY must decode to 32 bytes")

        admin_token = os.environ.get("BEARWITHME_PLATFORM_ADMIN_TOKEN", "")
        if len(admin_token) < 32:
            raise ConfigurationError(
                "BEARWITHME_PLATFORM_ADMIN_TOKEN must contain at least 32 characters"
            )
        return cls(
            database_path=(
                os.environ.get("BEARWITHME_DATABASE")
                or os.environ.get("DATABASE_URL")
                or os.environ.get("POSTGRES_URL", "bearwithme-mvp.db")
            ),
            base_url=os.environ.get("BEARWITHME_BASE_URL", "http://localhost:8000").rstrip("/"),
            web_origin=os.environ.get("BEARWITHME_WEB_ORIGIN", "http://localhost:3000").rstrip("/"),
            master_key=key,
            platform_admin_token=admin_token,
            livekit_url=os.environ.get("LIVEKIT_URL", "").rstrip("/"),
            livekit_api_key=os.environ.get("LIVEKIT_API_KEY", ""),
            livekit_api_secret=os.environ.get("LIVEKIT_API_SECRET", ""),
        )

    @classmethod
    def for_testing(cls, database_path: str, master_key: bytes | None = None) -> "Settings":
        """Build explicit isolated settings for tests and local smoke scenarios."""
        return cls(
            database_path=database_path,
            base_url="http://testserver",
            web_origin="http://testserver",
            master_key=master_key or b"test-master-key-32-bytes-long!!!",
            platform_admin_token="test-platform-admin-token-32-bytes-long",
            push_url="",
        )
