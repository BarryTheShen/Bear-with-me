"""Unauthenticated finder entry, anonymous sessions, and found reports."""

from __future__ import annotations

from .chat import ChatService
from .config import Settings
from .crypto import Cipher
from .database import Database
from .errors import AuthenticationError, NotFoundError, ValidationError
from .models import FinderSession, FoundReport, SafeTag
from .util import (
    PLACES,
    clean_text,
    expired,
    future_time,
    hash_token,
    new_public_ref,
    new_session_token,
    normalize_human_code,
    now,
)


class FinderService:
    def __init__(
        self,
        database: Database,
        cipher: Cipher,
        settings: Settings,
        chat: ChatService,
        notifications=None,
        authorities=None,
    ):
        self.database = database
        self.cipher = cipher
        self.settings = settings
        self.chat = chat
        self.notifications = notifications
        self.authorities = authorities

    def open_secret(self, secret: str) -> FinderSession:
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT t.tag_ref,t.item_ref,t.status,i.label_ciphertext FROM tags t "
                "JOIN items i ON i.item_ref=t.item_ref WHERE t.secret_hash=?",
                (hash_token(secret),),
            ).fetchone()
        return self._open_row(row)

    def open_human_code(self, human_code: str) -> FinderSession:
        normalized = normalize_human_code(human_code)
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT t.tag_ref,t.item_ref,t.status,i.label_ciphertext FROM tags t "
                "JOIN items i ON i.item_ref=t.item_ref WHERE t.human_code_hash=?",
                (hash_token(normalized),),
            ).fetchone()
        return self._open_row(row)

    def report_found(
        self,
        session_token: str,
        place: str,
        note: str = "",
        authority_organization: str = "",
    ) -> FoundReport:
        place = clean_text(place, "place", 120)
        if place not in PLACES:
            raise ValidationError("place must be selected from the supported places")
        note = clean_text(note, "note", 1000, required=False)
        organization = clean_text(authority_organization, "authority_organization", 160, required=False)
        session_hash = hash_token(session_token)
        with self.database.transaction() as connection:
            session = connection.execute(
                "SELECT fs.*,t.item_ref,t.status,i.owner_ref FROM finder_sessions fs "
                "JOIN tags t ON t.tag_ref=fs.tag_ref JOIN items i ON i.item_ref=t.item_ref "
                "WHERE fs.session_hash=?",
                (session_hash,),
            ).fetchone()
            if not session or expired(session["expires_at"]):
                raise AuthenticationError("finder session is invalid or expired")
            if session["status"] != "active":
                raise NotFoundError("tag is no longer active")
            found_ref = new_public_ref("fnd")
            created = now()
            authority_requested = bool(organization)
            connection.execute(
                "INSERT INTO found_events(found_ref,tag_ref,item_ref,owner_ref,finder_session_hash,place,note_ciphertext,authority_requested,organization_ciphertext,organization_lookup,created_at) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (
                    found_ref,
                    session["tag_ref"],
                    session["item_ref"],
                    session["owner_ref"],
                    session_hash,
                    place,
                    self.cipher.seal(note),
                    int(authority_requested),
                    self.cipher.seal(organization) if authority_requested else None,
                    self.cipher.blind_index(organization) if authority_requested else None,
                    created,
                ),
            )
            connection.execute(
                "UPDATE items SET status='lost' WHERE item_ref=? AND status='active'",
                (session["item_ref"],),
            )
            conversation_ref = self.chat.create_for_found(
                connection, found_ref, session["owner_ref"], session_hash
            )
            authority_case_ref = None
            if authority_requested and self.authorities:
                authority_case_ref = self.authorities.create_case_for_found(
                    connection, found_ref, organization, place, ""
                )
        report = FoundReport(
            found_ref,
            conversation_ref,
            session["item_ref"],
            session["owner_ref"],
            place,
            note,
            authority_case_ref,
            created,
        )
        if self.notifications:
            self.notifications.notify_found(report)
        return report

    def owner_inbox(self, owner_ref: str) -> list[dict]:
        with self.database.read() as connection:
            rows = connection.execute(
                "SELECT f.found_ref,f.place,f.note_ciphertext,f.created_at,c.conversation_ref,c.status,i.item_ref,i.label_ciphertext "
                "FROM found_events f JOIN conversations c ON c.found_ref=f.found_ref "
                "JOIN items i ON i.item_ref=f.item_ref WHERE f.owner_ref=? ORDER BY f.created_at DESC",
                (owner_ref,),
            ).fetchall()
        return [
            {
                "found_ref": row["found_ref"],
                "conversation_ref": row["conversation_ref"],
                "item_ref": row["item_ref"],
                "label": self.cipher.open(row["label_ciphertext"]),
                "place": row["place"],
                "note": self.cipher.open(row["note_ciphertext"]),
                "conversation_status": row["status"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def _open_row(self, row) -> FinderSession:
        if not row or row["status"] != "active":
            raise NotFoundError("tag is unknown or inactive")
        token = new_session_token()
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO finder_sessions(session_hash,tag_ref,expires_at,created_at) VALUES(?,?,?,?)",
                (hash_token(token), row["tag_ref"], future_time(self.settings.finder_session_ttl_seconds), now()),
            )
        return FinderSession(token, row["tag_ref"], self.cipher.open(row["label_ciphertext"]), row["item_ref"])
