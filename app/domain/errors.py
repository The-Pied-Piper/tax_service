"""Errors raised by the domain and application layers.

They carry no HTTP knowledge; `main.py` maps them onto problem+json responses.
"""


class DomainError(Exception):
    """Base class for all business-rule violations."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class ValidationError(DomainError):
    pass


class InvalidManifestError(DomainError):
    """A jurisdiction manifest is malformed or breaks a manifest rule (design.md §4)."""


class InvalidJurisdictionCodeError(ValidationError):
    """A jurisdiction code is not in ISO 3166 form (e.g. `CA` or `CA-ON`)."""
