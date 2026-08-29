"""Security audit recording kept separate from business services."""

from __future__ import annotations

import json

from .crypto import Cipher
from .database import Database
from .util import new_public_ref, now


class AuditService:
    def __init__(self, database: Database, cipher: Cipher):
        self.database = database
        self.cipher = cipher

    def record(
        self,
        connection,
        actor_ref: str,
        actor_role: str,
        action: str,
        target_type: str,
        target_ref: str,
        metadata: dict | None = None,
    ) -> None:
        connection.execute(
            "INSERT INTO audit_events(audit_ref,actor_ref,actor_role,action,target_type,target_ref,metadata_ciphertext,created_at) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (
                new_public_ref("aud"),
                actor_ref,
                actor_role,
                action,
                target_type,
                target_ref,
                self.cipher.seal(json.dumps(metadata or {}, sort_keys=True)),
                now(),
            ),
        )

    def recent_for_target(self, target_type: str, target_ref: str) -> list[dict]:
        with self.database.read() as connection:
            rows = connection.execute(
                "SELECT actor_ref,actor_role,action,target_type,target_ref,metadata_ciphertext,created_at "
                "FROM audit_events WHERE target_type=? AND target_ref=? ORDER BY created_at DESC",
                (target_type, target_ref),
            ).fetchall()
        return [
            {
                "actor_ref": row["actor_ref"],
                "actor_role": row["actor_role"],
                "action": row["action"],
                "target_type": row["target_type"],
                "target_ref": row["target_ref"],
                "metadata": json.loads(self.cipher.open(row["metadata_ciphertext"])),
                "created_at": row["created_at"],
            }
            for row in rows
        ]
