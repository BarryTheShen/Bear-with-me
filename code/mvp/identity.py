"""Owner and authority identity lifecycle.

The application database stores encrypted UUIDs and contact fields. Sessions are
bearer tokens whose plaintext exists only at the transport boundary.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict

from .config import Settings
from .crypto import Cipher
from .database import Database
from .errors import AuthenticationError, ConflictError, NotFoundError
from .models import User
from .util import expired, future_time, hash_token, new_public_ref, new_session_token, normalize_email, now, clean_text


class IdentityService:
    def __init__(self, database: Database, cipher: Cipher, settings: Settings):
        self.database = database
        self.cipher = cipher
        self.settings = settings

    def register(self, email: str, name: str, role: str = "owner") -> tuple[User, str]:
        normalized_email = normalize_email(email)
        clean_name = clean_text(name, "name", 120)
        if role not in {"owner", "authority"}:
            raise ConflictError("unsupported user role")
        user_ref = new_public_ref("usr")
        user_uuid = str(uuid.uuid4())
        created = now()
        with self.database.transaction() as connection:
            try:
                connection.execute(
                    "INSERT INTO users(user_ref,uuid_ciphertext,uuid_lookup,role,name_ciphertext,email_ciphertext,email_lookup,created_at) "
                    "VALUES(?,?,?,?,?,?,?,?)",
                    (
                        user_ref,
                        self.cipher.seal(user_uuid),
                        self.cipher.blind_index(user_uuid),
                        role,
                        self.cipher.seal(clean_name),
                        self.cipher.seal(normalized_email),
                        self.cipher.blind_index(normalized_email),
                        created,
                    ),
                )
            except Exception as exc:
                if "UNIQUE constraint failed: users.email_lookup" in str(exc):
                    raise ConflictError("email already registered") from exc
                raise
        user = User(user_ref=user_ref, role=role, created_at=created)
        return user, self.issue_session(user_ref)

    def request_magic_link(self, email: str) -> str:
        normalized_email = normalize_email(email)
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT user_ref FROM users WHERE email_lookup=?",
                (self.cipher.blind_index(normalized_email),),
            ).fetchone()
        if not row:
            raise NotFoundError("account not found")
        token = new_session_token()
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO magic_links(token_hash,user_ref,expires_at) VALUES(?,?,?)",
                (hash_token(token), row["user_ref"], future_time(15 * 60)),
            )
        return token

    def consume_magic_link(self, token: str) -> tuple[User, str]:
        token_hash = hash_token(token)
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM magic_links WHERE token_hash=? AND consumed_at IS NULL",
                (token_hash,),
            ).fetchone()
            if not row or expired(row["expires_at"]):
                raise AuthenticationError("magic link is invalid or expired")
            connection.execute(
                "UPDATE magic_links SET consumed_at=? WHERE token_hash=?",
                (now(), token_hash),
            )
            user = self._user_from_connection(connection, row["user_ref"])
        return user, self.issue_session(user.user_ref)

    def issue_session(self, user_ref: str) -> str:
        token = new_session_token()
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO sessions(session_hash,user_ref,expires_at,created_at) VALUES(?,?,?,?)",
                (hash_token(token), user_ref, future_time(self.settings.session_ttl_seconds), now()),
            )
        return token

    def authenticate(self, token: str) -> User:
        if not token:
            raise AuthenticationError("authentication required")
        token_hash = hash_token(token)
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT user_ref,expires_at FROM sessions WHERE session_hash=?",
                (token_hash,),
            ).fetchone()
            if not row or expired(row["expires_at"]):
                if row:
                    connection.execute("DELETE FROM sessions WHERE session_hash=?", (token_hash,))
                raise AuthenticationError("session is invalid or expired")
            return self._user_from_connection(connection, row["user_ref"])

    def require_owner(self, token: str) -> User:
        user = self.authenticate(token)
        if user.role != "owner":
            raise AuthenticationError("owner session required")
        return user

    def require_authority(self, token: str) -> User:
        user = self.authenticate(token)
        if user.role != "authority":
            raise AuthenticationError("authority session required")
        return user

    def _user_from_connection(self, connection, user_ref: str) -> User:
        row = connection.execute(
            "SELECT user_ref,role,created_at FROM users WHERE user_ref=?",
            (user_ref,),
        ).fetchone()
        if not row:
            raise AuthenticationError("account no longer exists")
        return User(user_ref=row["user_ref"], role=row["role"], created_at=row["created_at"])
