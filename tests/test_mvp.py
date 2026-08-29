from __future__ import annotations

import sqlite3

import pytest
from fastapi.testclient import TestClient

from code.mvp.api import create_app
from code.mvp.config import Settings
from code.mvp.container import create_services
from code.mvp.crypto import Cipher
from code.mvp.errors import AuthenticationError, AuthorizationError, CryptoError, NotFoundError
from code.mvp.notifications import MemoryPushSender
from code.mvp.util import valid_human_code


@pytest.fixture
def services(tmp_path):
    settings = Settings.for_testing(str(tmp_path / "mvp.db"))
    sender = MemoryPushSender()
    return create_services(settings, push_sender=sender), sender


def test_application_encryption_is_authenticated_and_uuid_is_not_plaintext(services):
    service, _ = services
    value = "owner-uuid-value"
    sealed = service.cipher.seal(value)
    assert service.cipher.open(sealed) == value
    parts = sealed.split(".")
    tampered_value = list(parts[2])
    tampered_value[0] = "A" if tampered_value[0] != "A" else "B"
    with pytest.raises(CryptoError):
        service.cipher.open(f"{parts[0]}.{parts[1]}.{''.join(tampered_value)}")
    with pytest.raises(CryptoError):
        Cipher(b"different-master-key-32-bytes!!!").open(sealed)

    owner, _ = service.identity.register("owner@example.com", "Owner")
    with service.database.read() as connection:
        row = connection.execute("SELECT * FROM users WHERE user_ref=?", (owner.user_ref,)).fetchone()
    assert value not in " ".join(str(item) for item in row)
    assert "uuid_ciphertext" in row.keys()


def test_tag_replacement_and_anonymous_chat_notify_owner(services):
    service, sender = services
    owner, owner_session = service.identity.register("owner@example.com", "Owner")
    item = service.items.create_item(owner.user_ref, "Blue bottle", "Private scratch")
    tag = service.items.provision_tag(owner.user_ref, item.item_ref)
    assert len(tag.human_code) == 8
    assert valid_human_code(tag.human_code)

    device_ref = service.notifications.register_device(owner.user_ref, "ExponentPushToken[test]", "ios")
    finder = service.finder.open_secret(tag.secret)
    assert finder.label == "Blue bottle"
    report = service.finder.report_found(finder.session_token, "Main library", "At the desk")
    assert report.conversation_ref
    assert sender.sent[0][1]["body"] == "Someone reported your item found."
    assert "Main library" not in sender.sent[0][1]["body"]

    service.chat.send_finder(finder.session_token, report.conversation_ref, "I left it at the desk")
    service.chat.send_owner(owner.user_ref, report.conversation_ref, "Thank you")
    messages = service.chat.list_for_owner(owner.user_ref, report.conversation_ref)
    assert [message.sender_role for message in messages] == ["finder", "owner"]
    assert messages[0].body == "I left it at the desk"

    replacement = service.items.replace_tag(owner.user_ref, tag.tag_ref)
    with pytest.raises(NotFoundError):
        service.finder.open_secret(tag.secret)
    assert service.finder.open_secret(replacement.secret).item_ref == item.item_ref
    assert device_ref
    assert owner_session


def test_authority_is_invited_and_cannot_escalate(services):
    service, _ = services
    owner, _ = service.identity.register("owner@example.com", "Owner")
    item = service.items.create_item(owner.user_ref, "Backpack")
    tag = service.items.provision_tag(owner.user_ref, item.item_ref)
    finder = service.finder.open_human_code(tag.human_code)
    report = service.finder.report_found(
        finder.session_token,
        "Campus security",
        "Handed to desk",
        "WashU Campus Security",
    )
    assert report.authority_case_ref

    invite = service.authorities.invite(
        service.settings.platform_admin_token, "WashU Campus Security", "police@example.com"
    )
    authority, authority_session = service.authorities.accept_invite(invite, "Officer")
    cases = service.authorities.list_cases(authority.user_ref)
    assert cases[0].case_ref == report.authority_case_ref
    service.authorities.update_case(authority.user_ref, cases[0].case_ref, "in_custody", "CASE-1")
    with pytest.raises(AuthorizationError):
        service.authorities.invite(authority_session, "Another", "another@example.com")


def test_http_contract_carries_core_return_loop(services):
    service, _ = services
    client = TestClient(create_app(service))
    registered = client.post("/api/auth/register", json={"email": "owner@example.com", "name": "Owner"})
    assert registered.status_code == 200
    body = registered.json()
    assert "uuid" not in registered.text.lower()
    auth = {"Authorization": f"Bearer {body['session_token']}"}

    item = client.post("/api/items", headers=auth, json={"label": "Bottle", "description": "Blue cap"})
    assert item.status_code == 200
    item_ref = item.json()["item_ref"]
    provisioned = client.post(f"/api/items/{item_ref}/tags", headers=auth)
    assert provisioned.status_code == 200
    tag = provisioned.json()

    opened = client.get(f"/api/f/{tag['secret']}")
    assert opened.status_code == 200
    assert set(opened.json()) == {"session_token", "label"}
    finder_headers = {"X-Finder-Session": opened.json()["session_token"]}
    report = client.post(
        f"/api/f/sessions/{opened.json()['session_token']}/found",
        headers=finder_headers,
        json={"place": "Student union", "note": "On the front desk"},
    )
    assert report.status_code == 200
    assert "owner_ref" not in report.json()
    assert "item_ref" not in report.json()
    conversation = report.json()["conversation_ref"]
    sent = client.post(
        f"/api/finder/conversations/{conversation}/messages",
        headers=finder_headers,
        json={"body": "It is safe at the desk."},
    )
    assert sent.status_code == 200
    inbox = client.get("/api/owner/inbox", headers=auth)
    assert inbox.status_code == 200
    assert inbox.json()["events"][0]["conversation_ref"] == conversation
    messages = client.get(f"/api/owner/conversations/{conversation}/messages", headers=auth)
    assert messages.status_code == 200
    assert messages.json()["messages"][0]["body"] == "It is safe at the desk."


def test_short_code_requires_check_symbol_and_is_rate_limited(services):
    service, _ = services
    client = TestClient(create_app(service))
    for _ in range(10):
        response = client.get("/api/f/code/00000001")
        assert response.status_code == 422
    limited = client.get("/api/f/code/00000001")
    assert limited.status_code == 429
    assert "retry-after" in limited.headers
