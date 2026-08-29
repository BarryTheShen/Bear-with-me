"""Application-layer encryption and blind lookup primitives.

Keys are derived from a 32-byte master key and never persisted in SQLite. UUIDs,
contact details, push tokens, and authority details use ``seal``. Equality
lookups use ``blind_index`` rather than reversible deterministic encryption.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

from .errors import ConfigurationError, CryptoError


@dataclass(frozen=True)
class KeyRing:
    encryption_key: bytes
    lookup_key: bytes

    @classmethod
    def from_master(cls, master_key: bytes) -> "KeyRing":
        if len(master_key) != 32:
            raise ConfigurationError("encryption master key must be exactly 32 bytes")
        material = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=b"bear-with-me-mvp-key-v1",
            info=b"application-data-and-blind-index-keys",
        ).derive(master_key)
        return cls(material[:32], material[32:])


class Cipher:
    """Small authenticated-encryption facade with versioned ciphertexts."""

    def __init__(self, master_key: bytes):
        self._keys = KeyRing.from_master(master_key)

    def seal(self, value: str) -> str:
        nonce = secrets.token_bytes(12)
        ciphertext = AESGCM(self._keys.encryption_key).encrypt(
            nonce, value.encode("utf-8"), b"bear-with-me-v1"
        )
        encoded_nonce = base64.urlsafe_b64encode(nonce).decode("ascii").rstrip("=")
        encoded_value = base64.urlsafe_b64encode(ciphertext).decode("ascii").rstrip("=")
        return f"v1.{encoded_nonce}.{encoded_value}"

    def open(self, sealed: str) -> str:
        try:
            version, encoded_nonce, encoded_value = sealed.split(".", 2)
            if version != "v1":
                raise ValueError("unknown ciphertext version")
            nonce = base64.urlsafe_b64decode(encoded_nonce + "===")
            ciphertext = base64.urlsafe_b64decode(encoded_value + "===")
            plaintext = AESGCM(self._keys.encryption_key).decrypt(
                nonce, ciphertext, b"bear-with-me-v1"
            )
            return plaintext.decode("utf-8")
        except (InvalidTag, ValueError, TypeError, UnicodeDecodeError) as exc:
            raise CryptoError("ciphertext is invalid or authentication failed") from exc

    def blind_index(self, value: str) -> str:
        return hmac.new(
            self._keys.lookup_key, value.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    @staticmethod
    def random_secret() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def random_ref(prefix: str) -> str:
        return f"{prefix}_{secrets.token_urlsafe(18)}"

    @staticmethod
    def constant_time_equal(left: str, right: str) -> bool:
        return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))
