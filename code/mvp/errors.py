"""Stable service errors mapped to transport-level responses."""


class MvpError(Exception):
    """Base class for expected application errors."""


class ConfigurationError(MvpError):
    """Required production configuration is missing or invalid."""


class AuthenticationError(MvpError):
    """A session or one-time credential is invalid."""


class AuthorizationError(MvpError):
    """The actor cannot perform the requested operation."""


class NotFoundError(MvpError):
    """The requested resource does not exist or is not visible."""


class ConflictError(MvpError):
    """The operation conflicts with current resource state."""


class ValidationError(MvpError):
    """Input failed domain validation."""


class RateLimitError(MvpError):
    """A public endpoint has exceeded its request budget."""

    def __init__(self, retry_after: int):
        super().__init__("too many requests; retry later")
        self.retry_after = retry_after

class CryptoError(MvpError):
    """Authenticated encryption or integrity verification failed."""


class ProviderUnavailable(MvpError):
    """An optional external provider is not configured or unavailable."""
