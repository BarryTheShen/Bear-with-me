"""Owner item inventory and tag provisioning lifecycle."""

from __future__ import annotations

from .audit import AuditService
from .config import Settings
from .crypto import Cipher
from .database import Database
from .errors import AuthorizationError, ConflictError, NotFoundError
from .models import Item, ItemStatus, SafeTag, TagProvisioning
from .util import clean_text, generate_human_code, hash_token, normalize_human_code, new_public_ref, now


class ItemService:
    def __init__(self, database: Database, cipher: Cipher, settings: Settings, audit: AuditService):
        self.database = database
        self.cipher = cipher
        self.settings = settings
        self.audit = audit

    def create_item(self, owner_ref: str, label: str, description: str = "") -> Item:
        clean_label = clean_text(label, "label", 120)
        clean_description = clean_text(description, "description", 1000, required=False)
        item_ref = new_public_ref("itm")
        created = now()
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO items(item_ref,owner_ref,label_ciphertext,description_ciphertext,status,created_at) VALUES(?,?,?,?,?,?)",
                (
                    item_ref,
                    owner_ref,
                    self.cipher.seal(clean_label),
                    self.cipher.seal(clean_description),
                    ItemStatus.ACTIVE,
                    created,
                ),
            )
            self.audit.record(connection, owner_ref, "owner", "item.created", "item", item_ref)
        return Item(item_ref, owner_ref, clean_label, clean_description, ItemStatus.ACTIVE, created)

    def list_items(self, owner_ref: str) -> list[Item]:
        with self.database.read() as connection:
            rows = connection.execute(
                "SELECT * FROM items WHERE owner_ref=? ORDER BY created_at DESC", (owner_ref,)
            ).fetchall()
        return [self._item(row) for row in rows]

    def rename_item(self, owner_ref: str, item_ref: str, label: str, description: str | None = None) -> Item:
        clean_label = clean_text(label, "label", 120)
        with self.database.transaction() as connection:
            row = self._owned_row(connection, owner_ref, item_ref)
            clean_description = (
                row["description_ciphertext"]
                if description is None
                else self.cipher.seal(clean_text(description, "description", 1000, required=False))
            )
            connection.execute(
                "UPDATE items SET label_ciphertext=?,description_ciphertext=? WHERE item_ref=?",
                (self.cipher.seal(clean_label), clean_description, item_ref),
            )
            self.audit.record(connection, owner_ref, "owner", "item.updated", "item", item_ref)
            row = self._owned_row(connection, owner_ref, item_ref)
        return self._item(row)

    def set_status(self, owner_ref: str, item_ref: str, status: ItemStatus) -> Item:
        with self.database.transaction() as connection:
            self._owned_row(connection, owner_ref, item_ref)
            connection.execute("UPDATE items SET status=? WHERE item_ref=?", (status, item_ref))
            self.audit.record(connection, owner_ref, "owner", "item.status_changed", "item", item_ref, {"status": status})
            row = self._owned_row(connection, owner_ref, item_ref)
        return self._item(row)

    def provision_tag(self, owner_ref: str, item_ref: str) -> TagProvisioning:
        with self.database.transaction() as connection:
            self._owned_row(connection, owner_ref, item_ref)
            provisioning = self._insert_tag(connection, item_ref)
            self.audit.record(connection, owner_ref, "owner", "tag.provisioned", "tag", provisioning.tag_ref)
        return provisioning

    def revoke_tag(self, owner_ref: str, tag_ref: str) -> None:
        with self.database.transaction() as connection:
            row = self._tag_for_owner(connection, owner_ref, tag_ref)
            if row["status"] != "active":
                return
            connection.execute(
                "UPDATE tags SET status='revoked',revoked_at=? WHERE tag_ref=?", (now(), tag_ref)
            )
            self.audit.record(connection, owner_ref, "owner", "tag.revoked", "tag", tag_ref)

    def replace_tag(self, owner_ref: str, tag_ref: str) -> TagProvisioning:
        with self.database.transaction() as connection:
            row = self._tag_for_owner(connection, owner_ref, tag_ref)
            if row["status"] != "active":
                raise ConflictError("only an active tag can be replaced")
            replacement = self._insert_tag(connection, row["item_ref"])
            connection.execute(
                "UPDATE tags SET status='replaced',replaced_by=?,revoked_at=? WHERE tag_ref=?",
                (replacement.tag_ref, now(), tag_ref),
            )
            self.audit.record(
                connection, owner_ref, "owner", "tag.replaced", "tag", tag_ref,
                {"replacement": replacement.tag_ref},
            )
        return replacement

    def resolve_secret(self, secret: str) -> SafeTag:
        return self._resolve(hash_token(secret))

    def resolve_human_code(self, human_code: str) -> SafeTag:
        normalized = normalize_human_code(human_code)
        return self._resolve(None, hash_token(normalized))

    def _resolve(self, secret_hash: str | None, human_hash: str | None = None) -> SafeTag:
        column = "secret_hash" if secret_hash is not None else "human_code_hash"
        value = secret_hash if secret_hash is not None else human_hash
        with self.database.read() as connection:
            row = connection.execute(
                f"SELECT t.tag_ref,t.item_ref,t.status,i.label_ciphertext FROM tags t "
                f"JOIN items i ON i.item_ref=t.item_ref WHERE t.{column}=?", (value,)
            ).fetchone()
        if not row or row["status"] != "active":
            raise NotFoundError("tag is unknown or inactive")
        return SafeTag(row["tag_ref"], row["item_ref"], self.cipher.open(row["label_ciphertext"]))

    def _insert_tag(self, connection, item_ref: str) -> TagProvisioning:
        tag_ref = new_public_ref("tag")
        secret = self.cipher.random_secret()
        human_code = generate_human_code()
        try:
            connection.execute(
                "INSERT INTO tags(tag_ref,item_ref,secret_hash,human_code_hash,status,created_at) VALUES(?,?,?,?,?,?)",
                (tag_ref, item_ref, hash_token(secret), hash_token(human_code), "active", now()),
            )
        except Exception as exc:
            raise ConflictError("could not provision a unique tag") from exc
        return TagProvisioning(
            tag_ref,
            item_ref,
            secret,
            human_code,
            f"{self.settings.base_url}/f/{secret}",
        )

    def _owned_row(self, connection, owner_ref: str, item_ref: str):
        row = connection.execute(
            "SELECT * FROM items WHERE item_ref=? AND owner_ref=?", (item_ref, owner_ref)
        ).fetchone()
        if not row:
            raise NotFoundError("item not found")
        return row

    def _tag_for_owner(self, connection, owner_ref: str, tag_ref: str):
        row = connection.execute(
            "SELECT t.* FROM tags t JOIN items i ON i.item_ref=t.item_ref "
            "WHERE t.tag_ref=? AND i.owner_ref=?",
            (tag_ref, owner_ref),
        ).fetchone()
        if not row:
            raise NotFoundError("tag not found")
        return row

    def _item(self, row) -> Item:
        return Item(
            row["item_ref"],
            row["owner_ref"],
            self.cipher.open(row["label_ciphertext"]),
            self.cipher.open(row["description_ciphertext"]),
            ItemStatus(row["status"]),
            row["created_at"],
        )
