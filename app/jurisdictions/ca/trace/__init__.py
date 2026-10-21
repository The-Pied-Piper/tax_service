"""The federal Canada trace lines: facts in the vocabulary of Canada's own forms.

Capital cost allowance, gains, dependants and rentals; each line's English text is in
`app.jurisdictions.ca.trace_english`. The generic lines are in `app.domain.trace`.
"""

from __future__ import annotations

# Each feature module's `__all__` is re-exported, so a class added to an existing module needs no
# edit here; a new feature module adds its name to each of the three lists below.
from app.jurisdictions.ca.trace import capital_cost, dependants, gains, percentages, rentals
from app.jurisdictions.ca.trace.capital_cost import *  # noqa: F403
from app.jurisdictions.ca.trace.dependants import *  # noqa: F403
from app.jurisdictions.ca.trace.gains import *  # noqa: F403
from app.jurisdictions.ca.trace.percentages import *  # noqa: F403
from app.jurisdictions.ca.trace.rentals import *  # noqa: F403

__all__ = (
    capital_cost.__all__
    + dependants.__all__
    + gains.__all__
    + percentages.__all__
    + rentals.__all__
)
