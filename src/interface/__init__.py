"""Utilities for integrating Blackbird with alternative interfaces."""

from .service import (
    SearchOutcome,
    AccountResult,
    MetadataItem,
    SearchServiceError,
    search_email,
    search_username,
)

__all__ = [
    "SearchOutcome",
    "AccountResult",
    "MetadataItem",
    "SearchServiceError",
    "search_email",
    "search_username",
]
