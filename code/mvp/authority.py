"""Manual authority invitations, least-privilege cases, and transitions."""

from __future__ import annotations

import hmac

from .audit import AuditService
from .config import Settings
from .crypto import Cipher
from .database import Database
from .errors import AuthenticationError, AuthorizationError, ConflictError, NotFoundError, ValidationError
from .identity import IdentityService
from .models import AuthorityCase, AuthorityCaseStatus
from .util import clean_text, expired, future_time, hash_token, new_public_ref, new_session_token, normalize_email, now


class AuthorityService:
    def __init__(
        self,
        database: Database,
        cipher: Cipher,
        settings: Settings,
        identity: IdentityService,
        audit: AuditService,
    ):
        self.database = database
        self.cipher = cipher
        self.settings = settings
        self.identity = identity
        self.audit = audit

    def invite(self, admin_token: str, organization: str, email: str) -> str:
        self._require_platform_admin(admin_token)
        organization = clean_text(organization, "organization", 160)
        email = normalize_email(email)
        token = new_session_token()
        invite_ref = new_public_ref("inv")
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO authority_invites(invite_ref,organization_ciphertext,organization_lookup,email_ciphertext,email_lookup,token_hash,expires_at,created_at) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (
                    invite_ref,
                    self.cipher.seal(organization),
                    self.cipher.blind_index(organization.lower()),
                    self.cipher.seal(email),
                    self.cipher.blind_index(email),
                    hash_token(token),
                    future_time(24 * 60 * 60),
                    now(),
                ),
            )
            self.audit.record(
                connection,
                "platform-admin",
                "platform_admin",
                "authority.invited",
                "authority_invite",
                invite_ref,
                {"organization": "encrypted"},
            )
        return token

    def accept_invite(self, token: str, name: str):
        token_hash = hash_token(token)
        with self.database.read() as connection:
            invite = connection.execute(
                "SELECT * FROM authority_invites WHERE token_hash=? AND consumed_at IS NULL",
                (token_hash,),
            ).fetchone()
        if not invite or expired(invite["expires_at"]):
            raise AuthenticationError("authority invite is invalid or expired")
        email = self.cipher.open(invite["email_ciphertext"])
        organization = self.cipher.open(invite["organization_ciphertext"])
        user, session = self.identity.register(email, name, role="authority")
        with self.database.transaction() as connection:
            connection.execute(
                "UPDATE authority_invites SET consumed_at=? WHERE token_hash=? AND consumed_at IS NULL",
                (now(), token_hash),
            )
            if connection.total_changes != 1:
                raise ConflictError("authority invite has already been consumed")
            authority_ref = new_public_ref("auth")
            connection.execute(
                "INSERT INTO authority_users(authority_ref,user_ref,organization_ciphertext,organization_lookup,status,created_at) VALUES(?,?,?,?,?,?)",
                (
                    authority_ref,
                    user.user_ref,
                    self.cipher.seal(organization),
                    self.cipher.blind_index(organization.lower()),
                    "active",
                    now(),
                ),
            )
            self.audit.record(
                connection,
                user.user_ref,
                "authority",
                "authority.accepted",
                "authority_user",
                authority_ref,
            )
        return user, session

    def create_case_for_found(self, connection, found_ref: str, organization: str, place: str, case_number: str) -> str:
        organization = clean_text(organization, "organization", 160)
        place = clean_text(place, "place", 120)
        case_number = clean_text(case_number, "case_number", 120, required=False)
        case_ref = new_public_ref("case")
        timestamp = now()
        connection.execute(
            "INSERT INTO authority_cases(case_ref,found_ref,organization_ciphertext,organization_lookup,status,custody_place_ciphertext,case_number_ciphertext,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (
                case_ref,
                found_ref,
                self.cipher.seal(organization),
                self.cipher.blind_index(organization.lower()),
                AuthorityCaseStatus.REQUESTED,
                self.cipher.seal(place),
                self.cipher.seal(case_number),
                timestamp,
                timestamp,
            ),
        )
        return case_ref

    def list_cases(self, authority_ref: str) -> list[AuthorityCase]:
        with self.database.read() as connection:
            authority = connection.execute(
                "SELECT organization_lookup FROM authority_users WHERE user_ref=? AND status='active'",
                (authority_ref,),
            ).fetchone()
            if not authority:
                raise AuthorizationError("authority account is inactive")
            rows = connection.execute(
                "SELECT * FROM authority_cases WHERE organization_lookup=? ORDER BY updated_at DESC",
                (authority["organization_lookup"],),
            ).fetchall()
        return [self._case(row) for row in rows]

    def update_case(
        self,
        authority_ref: str,
        case_ref: str,
        status: AuthorityCaseStatus,
        case_number: str | None = None,
    ) -> AuthorityCase:
        if status not in set(AuthorityCaseStatus):
            raise ValidationError("invalid authority case status")
        with self.database.transaction() as connection:
            authority = connection.execute(
                "SELECT organization_lookup FROM authority_users WHERE user_ref=? AND status='active'",
                (authority_ref,),
            ).fetchone()
            if not authority:
                raise AuthorizationError("authority account is inactive")
            row = connection.execute(
                "SELECT * FROM authority_cases WHERE case_ref=? AND organization_lookup=?",
                (case_ref, authority["organization_lookup"]),
            ).fetchone()
            if not row:
                raise NotFoundError("authority case not found")
            self._validate_transition(row["status"], status)
            number_ciphertext = row["case_number_ciphertext"]
            if case_number is not None:
                number_ciphertext = self.cipher.seal(clean_text(case_number, "case_number", 120))
            connection.execute(
                "UPDATE authority_cases SET status=?,case_number_ciphertext=?,updated_at=? WHERE case_ref=?",
                (status, number_ciphertext, now(), case_ref),
            )
            self.audit.record(connection, authority_ref, "authority", "authority.case_updated", "authority_case", case_ref, {"status": status})
            updated = connection.execute("SELECT * FROM authority_cases WHERE case_ref=?", (case_ref,)).fetchone()
        return self._case(updated)

    def organization_lookup_for_user(self, authority_ref: str) -> str:
        with self.database.read() as connection:
            row = connection.execute(
                "SELECT organization_lookup FROM authority_users WHERE user_ref=? AND status='active'",
                (authority_ref,),
            ).fetchone()
        if not row:
            raise AuthorizationError("authority account is inactive")
        return row["organization_lookup"]

    def _require_platform_admin(self, token: str) -> None:
        if not token or not hmac.compare_digest(token, self.settings.platform_admin_token):
            raise AuthorizationError("platform administrator authorization required")

    @staticmethod
    def _validate_transition(current: str, target: AuthorityCaseStatus) -> None:
        allowed = {
            "requested": {AuthorityCaseStatus.REQUESTED, AuthorityCaseStatus.IN_CUSTODY},
            "in_custody": {AuthorityCaseStatus.IN_CUSTODY, AuthorityCaseStatus.RELEASED},
            "released": {AuthorityCaseStatus.RELEASED, AuthorityCaseStatus.CLOSED},
            "closed": {AuthorityCaseStatus.CLOSED},
        }
        if target not in allowed[current]:
            raise ConflictError(f"cannot move authority case from {current} to {target}")

    def _case(self, row) -> AuthorityCase:
        return AuthorityCase(
            row["case_ref"],
            row["found_ref"],
            self.cipher.open(row["organization_ciphertext"]),
            AuthorityCaseStatus(row["status"]),
            self.cipher.open(row["custody_place_ciphertext"]),
            self.cipher.open(row["case_number_ciphertext"]),
            row["created_at"],
            row["updated_at"],
        )
