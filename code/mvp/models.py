"""Transport-neutral domain records returned by services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum


class TagStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
    REPLACED = "replaced"


class ItemStatus(StrEnum):
    ACTIVE = "active"
    LOST = "lost"
    RECOVERED = "recovered"


class ConversationStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


class AuthorityCaseStatus(StrEnum):
    REQUESTED = "requested"
    IN_CUSTODY = "in_custody"
    RELEASED = "released"
    CLOSED = "closed"


@dataclass(frozen=True)
class User:
    user_ref: str
    role: str
    created_at: str


@dataclass(frozen=True)
class Item:
    item_ref: str
    owner_ref: str
    label: str
    private_description: str
    status: ItemStatus
    created_at: str


@dataclass(frozen=True)
class TagProvisioning:
    tag_ref: str
    item_ref: str
    secret: str
    human_code: str
    finder_url: str


@dataclass(frozen=True)
class SafeTag:
    tag_ref: str
    item_ref: str
    label: str


@dataclass(frozen=True)
class FinderSession:
    session_token: str
    tag_ref: str
    label: str
    item_ref: str


@dataclass(frozen=True)
class FoundReport:
    found_ref: str
    conversation_ref: str
    item_ref: str
    owner_ref: str
    place: str
    note: str
    authority_case_ref: str | None
    created_at: str


@dataclass(frozen=True)
class Message:
    message_ref: str
    conversation_ref: str
    sender_role: str
    body: str
    created_at: str


@dataclass(frozen=True)
class AuthorityCase:
    case_ref: str
    found_ref: str
    organization: str
    status: AuthorityCaseStatus
    place: str
    case_number: str
    created_at: str
    updated_at: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
