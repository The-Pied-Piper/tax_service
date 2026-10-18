"""Surcharge tiers: a rate charged on the part of a base over each tier's threshold.

The tiers are parameter data, resolved per (family, tax_year); the code holds no jurisdiction's
thresholds or rates. A tier charges its rate on the part of a base over its threshold, unrounded;
rounding the part and summing the tiers are the capability's.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.errors import InvalidSurchargeTiersError
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import Rate


@dataclass(frozen=True)
class SurchargeTier:
    """`rate` charged on the part of a base over `threshold`; the threshold is exact."""

    threshold: Decimal
    rate: Rate

    def __post_init__(self) -> None:
        if not isinstance(self.threshold, Decimal):
            raise TypeError(
                f"tier threshold must be a Decimal, got {type(self.threshold).__name__}"
            )
        if not self.threshold.is_finite():
            raise InvalidSurchargeTiersError(f"tier threshold must be finite, got {self.threshold}")
        if self.threshold < 0:
            raise InvalidSurchargeTiersError(
                f"tier threshold must not be negative, got {self.threshold}"
            )
        if not isinstance(self.rate, Rate):
            raise TypeError(f"tier rate must be a Rate, got {type(self.rate).__name__}")

    def charge_on(self, base: Decimal) -> Decimal:
        """The unrounded charge on `base`: the rate on its part over the threshold, else zero."""
        over = base - self.threshold
        # At or below the threshold the charge is a plain zero: no scale, never a negative zero.
        return over * self.rate.value if over > 0 else Decimal(0)


@dataclass(frozen=True)
class SurchargeTiers:
    """At least one tier, thresholds strictly increasing; rates may rise or fall."""

    tiers: tuple[SurchargeTier, ...]

    def __post_init__(self) -> None:
        if not self.tiers:
            raise InvalidSurchargeTiersError("surcharge tiers need at least one tier")
        for index, (below, above) in enumerate(zip(self.tiers, self.tiers[1:], strict=False)):
            if above.threshold <= below.threshold:
                raise InvalidSurchargeTiersError(
                    f"tiers[{index + 1}] threshold {above.threshold} does not exceed "
                    f"tiers[{index}] threshold {below.threshold}; "
                    "thresholds must be strictly increasing"
                )

    def charges(self, base: Decimal) -> tuple[tuple[SurchargeTier, Decimal], ...]:
        """Each tier, in order, with its unrounded charge on `base`."""
        return tuple((tier, tier.charge_on(base)) for tier in self.tiers)


SURCHARGE_TIERS: ParameterKind[SurchargeTiers] = ParameterKind("surcharge_tiers", SurchargeTiers)
