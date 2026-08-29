"""Anonymous finder/owner conversation service."""

from __future__ import annotations

from .crypto import Cipher
from .database import Database
from .errors import AuthorizationError, ConflictError, NotFoundError
from .models import ConversationStatus, Message
from .util import clean_text, hash_token, new_public_ref, now


class ChatService:
    def __init__(self, database: Database, cipher: Cipher):
        self.database = database
        self.cipher = cipher

    def create_for_found(self, connection, found_ref: str, owner_ref: str, finder_session_hash: str) -> str:
        conversation_ref = new_public_ref("cnv")
        connection.execute(
            "INSERT INTO conversations(conversation_ref,found_ref,owner_ref,finder_session_hash,status,created_at) "
            "VALUES(?,?,?,?,?,?)",
            (conversation_ref, found_ref, owner_ref, finder_session_hash, ConversationStatus.OPEN, now()),
        )
        return conversation_ref

    def send_owner(self, owner_ref: str, conversation_ref: str, body: str) -> Message:
        body = clean_text(body, "message", 2000)
        with self.database.transaction() as connection:
            self._conversation_for_owner(connection, owner_ref, conversation_ref)
            return self._insert(connection, conversation_ref, "owner", body)

    def send_finder(self, session_token: str, conversation_ref: str, body: str) -> Message:
        body = clean_text(body, "message", 2000)
        with self.database.transaction() as connection:
            self._conversation_for_finder(connection, session_token, conversation_ref)
            return self._insert(connection, conversation_ref, "finder", body)

    def send_authority(
        self, authority_ref: str, organization_lookup: str, conversation_ref: str, body: str
    ) -> Message:
        body = clean_text(body, "message", 2000)
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT c.conversation_ref FROM conversations c "
                "JOIN found_events f ON f.found_ref=c.found_ref "
                "JOIN authority_cases ac ON ac.found_ref=f.found_ref "
                "WHERE c.conversation_ref=? AND ac.organization_lookup=? AND ac.status IN ('requested','in_custody')",
                (conversation_ref, organization_lookup),
            ).fetchone()
            if not row:
                raise AuthorizationError("authority cannot access this conversation")
            return self._insert(connection, conversation_ref, "authority", body)

    def list_for_owner(self, owner_ref: str, conversation_ref: str, after: str = "") -> list[Message]:
        with self.database.read() as connection:
            self._conversation_for_owner(connection, owner_ref, conversation_ref)
            return self._messages(connection, conversation_ref, after)

    def list_for_finder(self, session_token: str, conversation_ref: str, after: str = "") -> list[Message]:
        with self.database.read() as connection:
            self._conversation_for_finder(connection, session_token, conversation_ref)
            return self._messages(connection, conversation_ref, after)

    def list_for_authority(
        self, organization_lookup: str, conversation_ref: str, after: str = ""
    ) -> list[Message]:
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT c.conversation_ref FROM conversations c "
                "JOIN authority_cases ac ON ac.found_ref=c.found_ref "
                "WHERE c.conversation_ref=? AND ac.organization_lookup=?",
                (conversation_ref, organization_lookup),
            ).fetchone()
            if not row:
                raise AuthorizationError("authority cannot access this conversation")
            return self._messages(connection, conversation_ref, after)

    def close_for_owner(self, owner_ref: str, conversation_ref: str) -> None:
        with self.database.transaction() as connection:
            self._conversation_for_owner(connection, owner_ref, conversation_ref)
            connection.execute(
                "UPDATE conversations SET status=?,closed_at=? WHERE conversation_ref=?",
                (ConversationStatus.CLOSED, now(), conversation_ref),
            )

    def _insert(self, connection, conversation_ref: str, role: str, body: str) -> Message:
        message = Message(new_public_ref("msg"), conversation_ref, role, body, now())
        connection.execute(
            "INSERT INTO messages(message_ref,conversation_ref,sender_role,body_ciphertext,created_at) VALUES(?,?,?,?,?)",
            (message.message_ref, conversation_ref, role, self.cipher.seal(body), message.created_at),
        )
        return message

    def _messages(self, connection, conversation_ref: str, after: str) -> list[Message]:
        if after:
            rows = connection.execute(
                "SELECT * FROM messages WHERE conversation_ref=? AND created_at>? ORDER BY created_at ASC, message_ref ASC",
                (conversation_ref, after),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM messages WHERE conversation_ref=? ORDER BY created_at ASC, message_ref ASC",
                (conversation_ref,),
            ).fetchall()
        return [
            Message(
                row["message_ref"],
                row["conversation_ref"],
                row["sender_role"],
                self.cipher.open(row["body_ciphertext"]),
                row["created_at"],
            )
            for row in rows
        ]

    def _conversation_for_owner(self, connection, owner_ref: str, conversation_ref: str):
        row = connection.execute(
            "SELECT * FROM conversations WHERE conversation_ref=? AND owner_ref=?",
            (conversation_ref, owner_ref),
        ).fetchone()
        if not row:
            raise NotFoundError("conversation not found")
        return row

    def _conversation_for_finder(self, connection, session_token: str, conversation_ref: str):
        row = connection.execute(
            "SELECT * FROM conversations WHERE conversation_ref=? AND finder_session_hash=?",
            (conversation_ref, hash_token(session_token)),
        ).fetchone()
        if not row:
            raise NotFoundError("conversation not found")
        return row
