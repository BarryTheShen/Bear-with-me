"""Dependency composition root; domain modules remain independently testable."""

from __future__ import annotations

from dataclasses import dataclass

from .audit import AuditService
from .authority import AuthorityService
from .calling import CallService
from .chat import ChatService
from .config import Settings
from .crypto import Cipher
from .database import Database
from .finder import FinderService
from .identity import IdentityService
from .items import ItemService
from .notifications import ExpoPushSender, NotificationService, PushSender


@dataclass(frozen=True)
class Services:
    settings: Settings
    database: Database
    cipher: Cipher
    audit: AuditService
    identity: IdentityService
    items: ItemService
    chat: ChatService
    notifications: NotificationService
    authorities: AuthorityService
    finder: FinderService
    calling: CallService


def create_services(settings: Settings, push_sender: PushSender | None = None) -> Services:
    database = Database(settings.database_path)
    database.initialize()
    cipher = Cipher(settings.master_key)
    audit = AuditService(database, cipher)
    identity = IdentityService(database, cipher, settings)
    chat = ChatService(database, cipher)
    notifications = NotificationService(
        database, cipher, push_sender or ExpoPushSender(settings)
    )
    authorities = AuthorityService(database, cipher, settings, identity, audit)
    items = ItemService(database, cipher, settings, audit)
    finder = FinderService(
        database, cipher, settings, chat, notifications=notifications, authorities=authorities
    )
    calling = CallService(database, settings, chat, authorities)
    return Services(
        settings,
        database,
        cipher,
        audit,
        identity,
        items,
        chat,
        notifications,
        authorities,
        finder,
        calling,
    )
