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
    """No value was given for an artifact that was asked for."""


class DuplicateArtifactError(DomainError):
    """An artifact was given more than one value."""


class CapabilityContractError(DomainError):
    """A capability's outputs do not match the artifacts its contract produces."""


class InvalidBracketScheduleError(DomainError):
    """A bracket schedule's thresholds or rates are invalid."""


class InvalidParameterDataError(DomainError):
    """A parameter dataset is malformed or does not match where it was found."""


class InvalidCreditError(DomainError):
    """A credit amount is invalid."""


class InvalidRateError(DomainError):
    """A rate is not finite or is outside 0..1."""


class DuplicateRegistrationError(DomainError):
    """Something was registered under an identifier that is already taken."""


class UnknownRegistrationError(DomainError):
    """Nothing is registered under the identifier that was looked up."""


class InvalidRegistrationError(DomainError):
    """A registration's identifier or namespace is malformed, or no namespace is declared."""


class InvalidCompositionError(DomainError):
    """Capabilities are wired together badly, or a computation got the wrong starting values."""


class InvalidCapabilityError(DomainError):
    """A capability class declares slots its constructor cannot be built from (design.md §3)."""


class InvalidSelectionError(DomainError):
    """A manifest selection does not fill its capability's slots as declared (design.md §4)."""


class AmbiguousManifestError(DomainError):
    """More than one manifest applies to a tax year (design.md §4; §5 rule 6)."""
