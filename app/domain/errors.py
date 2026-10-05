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


class InvalidRoundingRuleError(DomainError):
    """A rounding rule's parameters are invalid (design.md §3, Rounding)."""


class InvalidJurisdictionCodeError(ValidationError):
    """A jurisdiction code is not in ISO 3166 form (e.g. `CA` or `CA-ON`)."""


class MissingArtifactError(DomainError):
    """A worksheet has no value for an artifact that was asked for."""


class DuplicateArtifactError(DomainError):
    """A worksheet was asked to record a value for an artifact that already has one."""


class CapabilityContractError(DomainError):
    """A capability's outputs do not match the artifacts its contract produces."""


class InvalidBracketScheduleError(DomainError):
    """A bracket schedule's thresholds or rates are invalid."""


class InvalidParameterDataError(DomainError):
    """A parameter dataset is malformed or does not match where it was found."""


class InvalidCreditError(DomainError):
    """A credit's amount or rate is invalid."""
