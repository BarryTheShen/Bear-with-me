"""Optional anonymous voice-call token issuance.

The service only mints short-lived room tokens after conversation authorization.
The LiveKit dependency is optional so chat and notifications remain deployable
without voice credentials; an unconfigured call is an explicit provider error.
"""

from __future__ import annotations

from datetime import timedelta
import hashlib

from .chat import ChatService
from .config import Settings
from .database import Database
from .errors import ProviderUnavailable
from .util import new_public_ref


class CallService:
    def __init__(self, database: Database, settings: Settings, chat: ChatService, authorities):
        self.database = database
        self.settings = settings
        self.chat = chat
        self.authorities = authorities

    def owner_token(self, owner_ref: str, conversation_ref: str) -> dict[str, str]:
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT conversation_ref FROM conversations WHERE conversation_ref=? AND owner_ref=? AND status='open'",
                (conversation_ref, owner_ref),
            ).fetchone()
        if not row:
            from .errors import NotFoundError

            raise NotFoundError("conversation not found")
        return self._issue(conversation_ref, "owner")

    def finder_token(self, finder_session_token: str, conversation_ref: str) -> dict[str, str]:
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT conversation_ref FROM conversations WHERE conversation_ref=? AND finder_session_hash=? AND status='open'",
                (conversation_ref, self._hash(finder_session_token)),
            ).fetchone()
        if not row:
            from .errors import NotFoundError

            raise NotFoundError("conversation not found")
        return self._issue(conversation_ref, "finder")

    def authority_token(self, authority_ref: str, conversation_ref: str) -> dict[str, str]:
        organization_lookup = self.authorities.organization_lookup_for_user(authority_ref)
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT c.conversation_ref FROM conversations c JOIN authority_cases ac ON ac.found_ref=c.found_ref "
                "WHERE c.conversation_ref=? AND ac.organization_lookup=? AND c.status='open'",
                (conversation_ref, organization_lookup),
            ).fetchone()
        if not row:
            from .errors import NotFoundError

            raise NotFoundError("conversation not found")
        return self._issue(conversation_ref, "authority")

    def _issue(self, conversation_ref: str, role: str) -> dict[str, str]:
        if not all((self.settings.livekit_url, self.settings.livekit_api_key, self.settings.livekit_api_secret)):
            raise ProviderUnavailable("calling provider is not configured")
        try:
            from livekit import api
        except ImportError as exc:
            raise ProviderUnavailable("calling provider package is not installed") from exc

        room = "bwm_" + hashlib.sha256(conversation_ref.encode()).hexdigest()[:24]
        participant = new_public_ref(role[:3])
        token = (
            api.AccessToken(self.settings.livekit_api_key, self.settings.livekit_api_secret)
            .with_ttl(timedelta(minutes=10))
            .with_identity(participant)
            .with_name(role)
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room,
                    can_publish=True,
                    can_subscribe=True,
                )
            )
            .to_jwt()
        )
        return {"server_url": self.settings.livekit_url, "room": room, "token": token}

    @staticmethod
    def _hash(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
