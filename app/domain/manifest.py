"""Jurisdiction manifest: which capabilities run for a jurisdiction, and from which tax year.

A manifest is selection plus parameter-family references only (design.md §4).
Plain attributes for now; behavior comes later.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapabilitySelection:
    """One capability chosen by a manifest, with the parameter family it resolves against."""

    name: str
    params_family: str


@dataclass(frozen=True, slots=True)
class Manifest:
    """One structural version of a jurisdiction's composition.

    `capabilities` keeps the authored order, which is advisory only.
    """

    jurisdiction: str
    version: int
    valid_from_tax_year: int
    capabilities: tuple[CapabilitySelection, ...]
