"""The structured trace: what each capability did, recorded as facts.

A trace line holds the domain objects and amounts involved (`ArtifactKind`, `Rate`, `Credit`,
`Amount`, `ContributionTier`, `Taper`, `Factor`, `Fraction`, `RateTableRow`, `ClassRate`,
`RoundingRule`), never text; its `amount` is the figure the line is about. A count is an `int`
artifact kind and its `int` value; a chosen rate is a `Rate` artifact kind and its `Rate` value.
Rendering lines as human-readable text lives outside the domain, in the adapters.
"""

from __future__ import annotations

# Each feature module's `__all__` is re-exported, so a class added to an existing module needs no
# edit here; a new feature module adds its name to each of the three lists below.
from app.domain.trace import (
    arithmetic,
    base,
    capital_cost,
    choices,
    dependants,
    gains,
    placement_credit,
    rate_tables,
    record_lists,
    rentals,
)
from app.domain.trace.arithmetic import *  # noqa: F403
from app.domain.trace.base import *  # noqa: F403
from app.domain.trace.capital_cost import *  # noqa: F403
from app.domain.trace.choices import *  # noqa: F403
from app.domain.trace.dependants import *  # noqa: F403
from app.domain.trace.gains import *  # noqa: F403
from app.domain.trace.placement_credit import *  # noqa: F403
from app.domain.trace.rate_tables import *  # noqa: F403
from app.domain.trace.record_lists import *  # noqa: F403
from app.domain.trace.rentals import *  # noqa: F403

__all__ = (
    arithmetic.__all__
    + base.__all__
    + capital_cost.__all__
    + choices.__all__
    + dependants.__all__
    + gains.__all__
    + placement_credit.__all__
    + rate_tables.__all__
    + record_lists.__all__
    + rentals.__all__
)
