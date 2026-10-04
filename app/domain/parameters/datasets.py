"""Parameter datasets: a family's values for one tax year (design.md §4).

Every covered tax year needs its own dataset; an absent year is never carried
forward. `sources` records where the values came from.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.parameters.brackets import BracketSchedule
from app.domain.parameters.credit import Credit
from app.domain.parameters.rounding import RoundingRule


@dataclass(frozen=True)
class BracketParameters:
    family: str
    tax_year: int
    schedule: BracketSchedule
    rounding: RoundingRule
    sources: tuple[str, ...]


@dataclass(frozen=True)
class CreditParameters:
    family: str
    tax_year: int
    credit: Credit
    rounding: RoundingRule
    sources: tuple[str, ...]
