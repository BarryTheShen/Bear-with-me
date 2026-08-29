"""Small shared helpers with no domain side effects."""

from __future__ import annotations

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone

from .errors import ValidationError


CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
PLACES = (
    "Main library",
    "Science library",
    "Student union",
    "Sports centre",
    "Lecture hall block",
    "Cafeteria",
    "Campus security",
    "Still with me",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def future_time(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat(
        timespec="seconds"
    )


def expired(timestamp: str) -> bool:
    return parse_time(timestamp) <= datetime.now(timezone.utc)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def clean_text(value: str, field: str, max_length: int, required: bool = True) -> str:
    text = (value or "").strip()
    if required and not text:
        raise ValidationError(f"{field} is required")
    if len(text) > max_length:
        raise ValidationError(f"{field} exceeds {max_length} characters")
    return text


def normalize_email(email: str) -> str:
    value = clean_text(email, "email", 320).lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        raise ValidationError("email is invalid")
    return value


def generate_human_code() -> str:
    data = "".join(secrets.choice(CROCKFORD) for _ in range(7))
    check = CROCKFORD[sum(CROCKFORD.index(char) for char in data) % len(CROCKFORD)]
    return data + check


def valid_human_code(code: str) -> bool:
    normalized = re.sub(r"[-\s]", "", (code or "")).upper()
    if len(normalized) != 8 or any(char not in CROCKFORD for char in normalized):
        return False
    expected = CROCKFORD[
        sum(CROCKFORD.index(char) for char in normalized[:7]) % len(CROCKFORD)
    ]
    return normalized[-1] == expected


def normalize_human_code(code: str) -> str:
    normalized = re.sub(r"[-\s]", "", (code or "")).upper()
    if not valid_human_code(normalized):
        raise ValidationError("human code is invalid")
    return normalized


def new_public_ref(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(18)}"


def new_session_token() -> str:
    return secrets.token_urlsafe(32)
