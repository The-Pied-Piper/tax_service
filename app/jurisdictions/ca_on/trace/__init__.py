"""The Ontario trace lines: facts in the vocabulary of Ontario's own forms.

Dependants, the provincial foreign tax credit and the placement credit; each line's English text
is in `app.jurisdictions.ca_on.trace_english`. The generic lines are in `app.domain.trace`, the
federal ones in `app.jurisdictions.ca.trace`.
"""

from __future__ import annotations

# Each feature module's `__all__` is re-exported, so a class added to an existing module needs no
# edit here; a new feature module adds its name to each of the three lists below.
from app.jurisdictions.ca_on.trace import dependants, foreign_tax, placement_credit
from app.jurisdictions.ca_on.trace.dependants import *  # noqa: F403
from app.jurisdictions.ca_on.trace.foreign_tax import *  # noqa: F403
from app.jurisdictions.ca_on.trace.placement_credit import *  # noqa: F403

__all__ = dependants.__all__ + foreign_tax.__all__ + placement_credit.__all__
