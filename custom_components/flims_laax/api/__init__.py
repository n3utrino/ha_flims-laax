"""
API package for flims_laax.

Exception hierarchy:
    FlimsLaaxApiClientError (base)
    ├── FlimsLaaxApiClientCommunicationError (network/timeout)
    └── FlimsLaaxApiClientAuthenticationError (401/403)

The coordinator maps them onto ConfigEntryAuthFailed and UpdateFailed; nothing else
in the integration imports this package.
"""

from .client import (
    FAN_SPEEDS,
    FlimsLaaxApiClient,
    FlimsLaaxApiClientAuthenticationError,
    FlimsLaaxApiClientCommunicationError,
    FlimsLaaxApiClientError,
)

__all__ = [
    "FAN_SPEEDS",
    "FlimsLaaxApiClient",
    "FlimsLaaxApiClientAuthenticationError",
    "FlimsLaaxApiClientCommunicationError",
    "FlimsLaaxApiClientError",
]
