"""The CA-ON artifact catalog: pilot artifacts named from Canada's own return (design.md §2, §7).

It lives with the pilot tests until the capability registry (#18) needs a production home.
Only artifacts the pilot tests use are listed.
"""

from __future__ import annotations

from app.domain.artifact import Amount


class TaxableIncome(Amount):
    """Taxable income, T1 line 26000: the base the federal and Ontario brackets apply to."""


class FederalBasicTax(Amount):
    """Federal tax on taxable income from the bracket schedule, before non-refundable credits."""
