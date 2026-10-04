"""Outbound port: where parameter datasets come from."""

from __future__ import annotations

from typing import Protocol

from app.domain.parameters.datasets import BracketParameters, CreditParameters


class ParameterSource(Protocol):
    def get_brackets(self, family: str, tax_year: int) -> BracketParameters:
        """The bracket dataset for `family` in `tax_year`.

        Raise NotFoundError if that year has no dataset (no carry-forward), and
        InvalidParameterDataError if the dataset cannot be read.
        """
        ...

    def get_credit(self, family: str, tax_year: int) -> CreditParameters:
        """The credit dataset for `family` in `tax_year`; same errors as get_brackets."""
        ...
