"""The CA-ON manifest: what it selects, and that production code builds it into a composition.

Building it through `TaxComputationService.compose` resolves every slot: each capability name to a
registered class, each parameter slot's family to a dataset of the slot's kind for the tax year,
and each artifact identifier to a registered kind of the slot's value type.

The entries it selects are listed by family, one module each in `manifest_families/`: each
family test checks that its own entries are in the manifest, and the full-manifest tests check
that the families together are the whole manifest, so an entry outside every family still
fails.
"""

from __future__ import annotations

from types import ModuleType

import pytest

import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.application.services.tax_computation import TaxComputationService
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.main import build_tax_computation
from tests.jurisdictions.ca_on.manifest_families import (
    canada_workers_benefit,
    capital_gains_deduction_qbt,
    credits_against_federal_tax,
    deductions,
    income,
    net_tax,
    non_refundable_credits,
    ontario_benefit_inputs,
    ontario_credits,
    ontario_lift,
    ontario_other_credits,
    ontario_personal_amounts,
    ontario_tax_reduction,
    other_inputs,
    personal_amounts,
    refund,
    refundable_credits,
    resp_aips,
    rrsp_fhsa,
    taxable_income,
)

FAMILIES: tuple[ModuleType, ...] = (
    income,
    rrsp_fhsa,
    deductions,
    taxable_income,
    capital_gains_deduction_qbt,
    personal_amounts,
    non_refundable_credits,
    credits_against_federal_tax,
    resp_aips,
    other_inputs,
    net_tax,
    canada_workers_benefit,
    refundable_credits,
    refund,
    ontario_personal_amounts,
    ontario_credits,
    ontario_tax_reduction,
    ontario_lift,
    ontario_other_credits,
    ontario_benefit_inputs,
)

ROOTS = app.registrations.JURISDICTIONS.roots()
CA_ON = JurisdictionCode("CA-ON")
INPUTS = frozenset[str]().union(*(family.INPUTS for family in FAMILIES))
OUTPUTS = frozenset[str]().union(*(family.OUTPUTS for family in FAMILIES))
STEPS = set[CapabilitySelection]().union(*(family.STEPS for family in FAMILIES))
WIRING = set[object]().union(*(family.WIRING for family in FAMILIES))


def manifest() -> Manifest:
    (only,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests
    return only


def service() -> TaxComputationService:
    return build_tax_computation()


@pytest.mark.parametrize("family", FAMILIES, ids=[f.__name__.rpartition(".")[2] for f in FAMILIES])
def test_the_manifest_has_the_inputs_outputs_and_selections_of_the_family(
    family: ModuleType,
) -> None:
    found = manifest()

    assert family.INPUTS <= found.inputs
    assert family.OUTPUTS <= found.outputs
    assert family.STEPS <= set(found.capabilities)


@pytest.mark.parametrize("family", FAMILIES, ids=[f.__name__.rpartition(".")[2] for f in FAMILIES])
def test_the_composition_has_the_wiring_of_the_family(family: ModuleType) -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert family.WIRING <= wiring


def test_ca_on_has_one_manifest_from_2025() -> None:
    found = manifest()

    assert found.jurisdiction == CA_ON
    assert found.version == 1
    assert found.valid_from_tax_year == 2025
    assert found.inputs == INPUTS
    # T1 line 167, the refund or balance owing, Schedule 7 line 23, what the return produces for
    # the next year's line 1, line 12010, the amount of dividends other than eligible, which
    # nothing else on the return reads; the Federal Worksheet's "Line 25000 - Other payments
    # deduction" line 9 "Line 5 plus line 8 =", which nothing consumes while the count of line 9
    # over $93,454 is a starting count; and ON428 line 58, the Ontario tax less the dividend tax
    # credit, which nothing else on the return reads (the surtax and line 69 read line 53; line
    # 60, the minimum tax carryover, is not modelled); Schedule 15 line 58, what the return produces
    # for the next year's line 52; the Ontario opportunities fund's line 3 (line 46600) "Net
    # refund (line 1 minus line 2)", which nothing reads (line 48400, the refund, is read by that
    # page's line 1, so it is not a line the computation returns); and ON479 line 63260, the
    # number of eligible work placements, which nothing else reads; Schedule 8 Part 2 line C
    # "Maximum amount subject to second additional contributions" of the "Monthly proration for
    # 2025" table, which nothing consumes, as Part 4 line 12 reads the maximum of 9,900 (and the
    # 8% rate) from its own dataset; T776 line 8140 "Total of
    # your gross rents for short-term rentals", which nothing else reads; T776 line 9365 "Total
    # for short-term rental portion", which nothing else reads (Chart A's column 3 is a
    # starting amount); Schedule 11 line 25 "Unused federal tuition amount available to carry
    # forward to a future year", which nothing else reads; T776 Area A column 24 "UCC at the end
    # of the year", a record list of each class's closing UCC for next year, which nothing else
    # reads; Form T2222 Chart A's row C
    # "Enter the total of all amounts in row B. This total cannot be more than $1,200.", totalled
    # over the individuals, which no line of the form reads; and Form ON-BEN's ten lines
    # (tick boxes 61020, 61040, 61060, 61070,
    # 61080 and 61140, Part A lines 61100, 61120, 61210 and 61230), which the return carries as
    # entered, each also an input with nothing computing from it; and ON479 line 63265 (the
    # answer on a partnership claim) and line 63270 (the business number), likewise carried as
    # entered: the lines the computation returns.
    # Schedule ON(S11) line 8, "Unused provincial tuition and education amounts available to carry
    # forward to a future year", the carryforward, which nothing else on the return reads.
    # Form T2048 Part 4 line 32 "Line 30 plus line 31", which nothing reads, and Part 5's totals A
    # 17211, B 17212, D 17215, E 17216 and (as lines 16, 41 and 42) C 17213, F 17217 and G 17218,
    # which the return carries for Form T657 and the T1 slips.
    assert found.outputs == OUTPUTS
    # List order carries no meaning: the composition derives the run order from the contracts.
    assert set(found.capabilities) == STEPS
    assert len(found.capabilities) == 628


def test_its_first_tax_year_composes_every_selection() -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert len(composition.order) == 628
    assert wiring == WIRING
