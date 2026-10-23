"""Unit tests for ProvincialForeignTaxCredit, lines 1 to 5 of Form T2036 (ON428 line 82).

Form T2036, "Provincial or Territorial Foreign Tax Credit": "Enter the amount from line 1 of Form
T2209." (line 1); "Enter the amount from line 3 of Form T2209, unless you have to pay minimum
tax.(1)" (line 2); "Line 1 minus line 2" (line 3); "Net foreign non-business income (2)" "×
Provincial or territorial tax otherwise payable (4)" over "Net income (3)" (line 4); "Enter
whichever amount is less: line 3 or line 4." "Provincial or territorial foreign tax credit" (line
5); "Enter the total from line 5 (for each country if applicable) on the line for the provincial or
territorial foreign tax credit of Form 428." Note (2): "Enter the amount reported as net foreign
non-business income from line 2 of Form T2209." Note (3): "Enter the amount reported as net income
from line 2 of Form T2209." And "If you paid tax to more than one foreign country, and the total
of the non-business income taxes that you paid to all foreign countries was more than $200, do the
calculation on a separate form for each country in Canadian dollars."

Its slots: one parameter slot, `rounding` (a `rounding_only` dataset: the rule for line 4); three
consumed slots, `sheets` (the `ca/foreign_tax_credit_sheets` record list of the T2209 sheets, each
record holding line 1 (tax paid), the income used on line 2 and line 3), `net_income` (note 3) and
`provincial_tax` (note 4, the tax otherwise payable), both Decimal; and one produced slot, `total`
(Decimal), the total of line 5 before the form's limit.

Per sheet: line 1 is the sheet's tax paid, line 2 is the sheet's T2209 line 3, line 3 is line 1
minus line 2, line 4 is the sheet's income times the provincial tax over the net income through
`ApplyRatio.ratio_of` (the same object as `core/apply_ratio`), rounded once with the `rounding`
dataset's rule, line 5 is the lesser of line 3 and line 4, and the total is the sum of line 5. No
sheets give 0, and net income is not consulted. A zero net income with at least one sheet is a
ValidationError naming `net_income`. It records one `ProvincialForeignTaxCreditLine` per sheet, by
position from 1, then an `ItemsTotalLine`; no sheets record the `ItemsTotalLine` alone.

The kinds and dataset families are made up, apart from the sheets, which are the registered record
list.
"""

from __future__ import annotations

import decimal
from collections.abc import Mapping
from decimal import Decimal
from types import MappingProxyType
from typing import Any, assert_type, cast

import pytest

import app.jurisdictions.ca_on.capabilities as ca_on_capabilities
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.capability import CapabilityRegistry, CapabilityResult
from app.domain.errors import (
    InvalidCapabilityError,
    MissingArtifactError,
    NotFoundError,
    ValidationError,
)
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Form, Manifest
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.catalog import (
    FOREIGN_BUSINESS_TAX_PAID,
    FOREIGN_BUSINESS_UNUSED_TAX_CREDITS,
    FOREIGN_NON_BUSINESS_TAX_PAID,
    FOREIGN_SURTAX_OUTSIDE_CANADA,
    FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    FOREIGN_TAX_CREDIT_SHEETS,
    NET_FOREIGN_BUSINESS_INCOME,
    NET_FOREIGN_NON_BUSINESS_INCOME,
)
from app.jurisdictions.ca_on.capabilities.provincial_foreign_tax_credit import (
    ProvincialForeignTaxCredit,
)
from app.jurisdictions.ca_on.trace import ProvincialForeignTaxCreditLine

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)

# The return-wide figures and the output come with the wiring; the tests use made-up kinds.
NET_INCOME = ArtifactKind("ex/net_income", Decimal)
PROVINCIAL_TAX = ArtifactKind("ex/provincial_tax", Decimal, non_negative=True)
CREDIT = ArtifactKind("ex/provincial_credit", Decimal, non_negative=True)
SHEETS = FOREIGN_TAX_CREDIT_SHEETS

# A sheet is (line 1 tax paid, income used on line 2, T2209 line 3).
Sheet = tuple[str, str, str]

# Net income 100,000 and provincial tax otherwise payable 5,000: line 4 is 5% of the income.
# US: 1,500 paid, the federal credit 1,400, so line 3 is 100; line 4 is 10,000 x 5% = 500.00.
US: Sheet = ("1500", "10000", "1400")
# UK: 100 paid, all of it credited federally, so line 3 is 0.
UK: Sheet = ("100", "5000", "100")


def rounding(rule: RoundingRule = CENT) -> ParameterDataset[RoundingOnly]:
    """By default half up to the cent."""
    return ParameterDataset(
        "ex/provincial_credit_rounding",
        2025,
        ROUNDING_ONLY,
        RoundingOnly(),
        rule,
        ("https://example.org/rounding",),
    )


def capability(dataset: ParameterDataset[RoundingOnly] | None = None) -> ProvincialForeignTaxCredit:
    return ProvincialForeignTaxCredit(
        dataset or rounding(), SHEETS, NET_INCOME, PROVINCIAL_TAX, CREDIT
    )


def sheet_list(*rows: Sheet) -> Artifact[Any]:
    """A `ca/foreign_tax_credit_sheets` artifact of one record per sheet, in order."""
    records = [
        {
            FOREIGN_NON_BUSINESS_TAX_PAID: D(tax),
            NET_FOREIGN_NON_BUSINESS_INCOME: D(income),
            FOREIGN_TAX_CREDIT_SHEET_LINE_3: D(line_3),
            FOREIGN_BUSINESS_TAX_PAID: D(0),
            FOREIGN_BUSINESS_UNUSED_TAX_CREDITS: D(0),
            NET_FOREIGN_BUSINESS_INCOME: D(0),
            FOREIGN_SURTAX_OUTSIDE_CANADA: D(0),
        }
        for tax, income, line_3 in rows
    ]
    return Artifact(SHEETS, RecordList(SHEETS.fields, records))


def given(
    *rows: Sheet, net_income: str = "100000", provincial_tax: str = "5000"
) -> tuple[Artifact[Any], ...]:
    return (
        sheet_list(*rows),
        Artifact(NET_INCOME, D(net_income)),
        Artifact(PROVINCIAL_TAX, D(provincial_tax)),
    )


def totals(result: CapabilityResult) -> Decimal:
    """The `total` output of a computation."""
    (output,) = result.outputs
    assert output.kind == CREDIT
    assert isinstance(output.value, Decimal)
    return output.value


def total(
    *rows: Sheet,
    net_income: str = "100000",
    provincial_tax: str = "5000",
    dataset: ParameterDataset[RoundingOnly] | None = None,
) -> Decimal:
    wired = capability(dataset)
    return totals(wired.compute(given(*rows, net_income=net_income, provincial_tax=provincial_tax)))


# --- contract and wiring ------------------------------------------------------------------------


def test_is_registered_as_ca_on_provincial_foreign_tax_credit() -> None:
    assert (
        CapabilityRegistry.shared().get("ca-on/provincial_foreign_tax_credit")
        is ProvincialForeignTaxCredit
    )


def test_is_exported_from_the_ca_on_capabilities_package() -> None:
    assert ca_on_capabilities.NAMESPACE == "ca-on"
    assert "provincial_foreign_tax_credit" in ca_on_capabilities.__all__
    assert (
        ca_on_capabilities.provincial_foreign_tax_credit.ProvincialForeignTaxCredit
        is ProvincialForeignTaxCredit
    )


def test_declares_its_contract() -> None:
    assert capability().consumes == frozenset({SHEETS, NET_INCOME, PROVINCIAL_TAX})
    assert capability().produces == frozenset({CREDIT})


def test_leaves_its_contract_to_the_base() -> None:
    assert "consumes" not in vars(ProvincialForeignTaxCredit)
    assert "produces" not in vars(ProvincialForeignTaxCredit)


def test_declares_its_slots() -> None:
    assert ProvincialForeignTaxCredit.PARAMETERS == {"rounding": ROUNDING_ONLY}
    assert ProvincialForeignTaxCredit.CONSUMES == {
        "sheets": RecordList,
        "net_income": Decimal,
        "provincial_tax": Decimal,
    }
    assert ProvincialForeignTaxCredit.PRODUCES == {"total": Decimal}
    assert not ProvincialForeignTaxCredit.is_list_slot("sheets")


def test_its_slots_are_read_only() -> None:
    slots = (
        ProvincialForeignTaxCredit.PARAMETERS,
        ProvincialForeignTaxCredit.CONSUMES,
        ProvincialForeignTaxCredit.PRODUCES,
    )
    for each in slots:
        assert isinstance(each, MappingProxyType)
        with pytest.raises(TypeError):
            cast(Any, each)["extra"] = Decimal


def test_its_slots_are_typed_as_read_only_mappings() -> None:
    assert_type(ProvincialForeignTaxCredit.CONSUMES, Mapping[str, type])
    assert_type(ProvincialForeignTaxCredit.PRODUCES, Mapping[str, type])


def test_is_built_from_its_slot_names_as_keywords() -> None:
    wired = ProvincialForeignTaxCredit(
        rounding=rounding(),
        sheets=SHEETS,
        net_income=NET_INCOME,
        provincial_tax=PROVINCIAL_TAX,
        total=CREDIT,
    )

    assert totals(wired.compute(given(US))) == D("100")


def test_takes_no_separate_rounding_argument() -> None:
    with pytest.raises(TypeError):
        ProvincialForeignTaxCredit(  # type: ignore[call-arg]
            rounding(), SHEETS, NET_INCOME, PROVINCIAL_TAX, CREDIT, CENT
        )


def test_rejects_a_money_kind_for_its_sheets() -> None:
    with pytest.raises(InvalidCapabilityError, match="ProvincialForeignTaxCredit.*'sheets'"):
        ProvincialForeignTaxCredit(
            rounding(),
            CREDIT,  # type: ignore[arg-type]
            NET_INCOME,
            PROVINCIAL_TAX,
            CREDIT,
        )


def test_mypy_rejects_a_dataset_of_another_parameter_kind() -> None:
    def wire() -> None:  # type-checked, never run
        amount = ParameterDataset(
            "ex/some_amount", 2025, AMOUNT, Amount(D("5")), NO_ROUNDING, ("https://example.org/a",)
        )
        ProvincialForeignTaxCredit(
            amount,  # type: ignore[arg-type]
            SHEETS,
            NET_INCOME,
            PROVINCIAL_TAX,
            CREDIT,
        )

    assert callable(wire)


def test_is_not_generic_over_artifacts() -> None:
    assert not getattr(ProvincialForeignTaxCredit, "__type_params__", ())
    assert not getattr(ProvincialForeignTaxCredit, "__parameters__", ())


# --- computing: lines 1 to 5 --------------------------------------------------------------------


def test_one_sheet_gives_the_lesser_of_line_3_and_line_4() -> None:
    # Line 3 = 1,500 - 1,400 = 100; line 4 = 10,000 x 5,000 / 100,000 = 500.00; line 5 = 100.
    assert total(US) == D("100")


def test_a_sheet_whose_line_4_is_below_line_3_gives_line_4() -> None:
    # Line 3 = 1,500 - 0 = 1,500; line 4 = 500.00.
    assert total(("1500", "10000", "0")) == D("500.00")


def test_a_sheet_credited_in_full_federally_adds_nothing() -> None:
    # Line 3 = 100 - 100 = 0; line 4 = 5,000 x 5% = 250.00.
    assert total(UK) == D("0")


def test_the_total_is_the_sum_of_line_5_of_each_sheet() -> None:
    # US 100 + a second sheet of line 3 = 300 - 100 = 200 and line 4 = 5,000 x 5% = 250.00: 200.
    assert total(US, ("300", "5000", "100")) == D("300")


def test_each_sheets_line_5_is_the_lesser_of_its_own_lines_3_and_4() -> None:
    # 800 - 0 = 800 against 500.00 gives 500.00; 100 - 0 = 100 against 250.00 gives 100.
    assert total(("800", "10000", "0"), ("100", "5000", "0")) == D("600.00")


def test_the_total_does_not_depend_on_the_order_of_the_sheets() -> None:
    assert total(UK, US) == total(US, UK)


def test_line_3_is_line_1_minus_line_2() -> None:
    # Line 3 = 1,500 - 1,400 = 100, not the sheet's own line 3 of 1,400.
    assert total(("1500", "100000", "1400")) == D("100")


def test_a_sheet_with_no_income_adds_nothing() -> None:
    assert total(("500", "0", "0")) == D("0.00")


def test_a_zero_provincial_tax_gives_zero() -> None:
    assert total(("1500", "10000", "0"), provincial_tax="0") == D("0.00")


def test_cents_in_the_tax_paid_are_kept() -> None:
    # Line 3 = 1,234.56 - 1,000 = 234.56, below line 4 = 100,000 x 5% = 5,000.00.
    assert total(("1234.56", "100000", "1000")) == D("234.56")


def test_line_3_depends_on_both_the_tax_paid_and_the_t2209_line_3() -> None:
    # 1,500 - 1,400 and 1,400 - 1,300 are both 100, while 1,500 - 1,300 is 200 (line 4 is 500.00).
    assert total(("1500", "10000", "1400")) == D("100")
    assert total(("1400", "10000", "1300")) == D("100")
    assert total(("1500", "10000", "1300")) == D("200")


# --- computing: no sheets ------------------------------------------------------------------------


def test_no_sheets_give_zero() -> None:
    output = Artifact(CREDIT, totals(capability().compute(given())))

    assert output == Artifact(CREDIT, D("0"))
    assert type(output.value) is Decimal
    assert not output.value.is_signed()


def test_no_sheets_do_not_consult_net_income() -> None:
    assert total(net_income="0") == D("0")


def test_no_sheets_need_neither_net_income_nor_provincial_tax_to_be_given() -> None:
    result = capability().compute((sheet_list(),))

    assert totals(result) == D("0")


# --- computing: net income zero ------------------------------------------------------------------


def test_a_zero_net_income_is_refused() -> None:
    with pytest.raises(ValidationError, match="net_income"):
        total(US, net_income="0")


def test_a_zero_net_income_is_refused_with_several_sheets() -> None:
    with pytest.raises(ValidationError, match="net_income"):
        total(US, UK, net_income="0")


def test_a_refusal_is_raised_when_computing_not_when_wiring() -> None:
    wired = capability()

    with pytest.raises(ValidationError):
        wired.compute(given(US, net_income="0"))

    assert totals(wired.compute(given(US))) == D("100")


# --- computing: rounding -------------------------------------------------------------------------


def test_line_4_is_rounded_half_up_to_the_cent() -> None:
    # 10 x 100 / 300 = 3.333...; 20 x 100 / 300 = 6.666...
    assert total(("50", "10", "0"), net_income="300", provincial_tax="100") == D("3.33")
    assert total(("50", "20", "0"), net_income="300", provincial_tax="100") == D("6.67")


def test_a_tie_rounds_half_up_by_the_dataset_rule() -> None:
    # 0.015 x 1 / 3 is exactly 0.005: half up gives 0.01, half even 0.00. Dividing first would
    # give 0.00499... and round down.
    assert total(("5", "0.015", "0"), net_income="3", provincial_tax="1") == D("0.01")
    half_even = RoundTo(D("0.01"), RoundingMode.HALF_EVEN)
    assert total(
        ("5", "0.015", "0"), net_income="3", provincial_tax="1", dataset=rounding(half_even)
    ) == D("0.00")


def test_each_sheet_is_rounded_before_the_sheets_are_summed() -> None:
    # Three sheets of 100 income, x 100 / 300: 33.33 x 3 = 99.99, not the rounded exact 100.00.
    rows = (("300", "100", "0"), ("300", "100", "0"), ("300", "100", "0"))

    assert total(*rows, net_income="300", provincial_tax="100") == D("99.99")


def test_a_whole_dollar_rule_rounds_each_sheet_to_the_dollar() -> None:
    whole = RoundTo(D("1"), RoundingMode.FLOOR)

    # 10 / 3 = 3.33 floors to 3; 20 / 3 = 6.67 floors to 6.
    assert total(
        ("300", "10", "0"),
        ("300", "20", "0"),
        net_income="300",
        provincial_tax="100",
        dataset=rounding(whole),
    ) == D("9")


def test_no_rounding_keeps_an_exact_finite_quotient() -> None:
    # 0.015 x 1 / 2 = 0.0075.
    assert total(
        ("5", "0.015", "0"), net_income="2", provincial_tax="1", dataset=rounding(NO_ROUNDING)
    ) == D("0.0075")


def test_no_rounding_refuses_a_quotient_with_no_finite_expansion() -> None:
    with pytest.raises(decimal.Inexact):
        total(
            ("5", "10", "0"), net_income="300", provincial_tax="100", dataset=rounding(NO_ROUNDING)
        )


def test_a_rounded_line_4_carries_the_increments_scale() -> None:
    assert str(total(("1500", "10000", "0"))) == "500.00"


# --- computing: the shared ratio object ---------------------------------------------------------


def test_line_4_is_worked_by_the_shared_ratio_method_of_apply_ratio(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = ApplyRatio.ratio_of
    calls: list[tuple[Decimal, Decimal, Decimal, RoundingRule]] = []

    def spy(
        amount: Decimal, numerator: Decimal, denominator: Decimal, rule: RoundingRule
    ) -> Decimal:
        calls.append((amount, numerator, denominator, rule))
        return original(amount, numerator, denominator, rule)

    monkeypatch.setattr(ApplyRatio, "ratio_of", staticmethod(spy))

    assert total(US, UK) == D("100")
    # amount = the sheet's income, numerator = the provincial tax, denominator = net income.
    assert calls == [
        (D("10000"), D("5000"), D("100000"), CENT),
        (D("5000"), D("5000"), D("100000"), CENT),
    ]


# --- computing: inputs --------------------------------------------------------------------------


def test_ignores_artifacts_it_does_not_consume() -> None:
    other = Artifact(CREDIT, D("9"))

    result = capability().compute((other, *given(US)))

    assert totals(result) == D("100")


@pytest.mark.parametrize("missing", ["foreign_tax_credit_sheets", "net_income", "provincial_tax"])
def test_a_missing_input_is_a_missing_artifact(missing: str) -> None:
    inputs = [a for a in given(US) if not a.kind.identifier.endswith(missing)]

    with pytest.raises(MissingArtifactError, match=missing):
        capability().compute(tuple(inputs))


def test_has_one_output_the_total() -> None:
    result = capability().compute(given(US, UK))

    assert [a.kind for a in result.outputs] == [CREDIT]


# --- trace ---------------------------------------------------------------------------------------


def sheet_line(
    position: int,
    tax: str,
    federal: str,
    line_3: str,
    income: str,
    line_4: str,
    result: str,
    rule: RoundingRule = CENT,
) -> Any:
    return ProvincialForeignTaxCreditLine(
        output=CREDIT,
        position=position,
        tax_paid=D(tax),
        federal_credit=D(federal),
        line_3=D(line_3),
        income=D(income),
        net_income=D("100000"),
        provincial_tax=D("5000"),
        rounding=rule,
        line_4=D(line_4),
        result=D(result),
    )


def test_traces_one_line_per_sheet_then_the_total() -> None:
    trace = capability().compute(given(US, UK)).trace

    assert trace == (
        sheet_line(1, "1500", "1400", "100", "10000", "500.00", "100"),
        sheet_line(2, "100", "100", "0", "5000", "250.00", "0"),
        ItemsTotalLine(CREDIT, ((1, D("100")), (2, D("0"))), D("100")),
    )


def test_traces_the_callers_order_with_positions_from_one() -> None:
    trace = capability().compute(given(UK, US)).trace

    assert trace == (
        sheet_line(1, "100", "100", "0", "5000", "250.00", "0"),
        sheet_line(2, "1500", "1400", "100", "10000", "500.00", "100"),
        ItemsTotalLine(CREDIT, ((1, D("0")), (2, D("100"))), D("100")),
    )


def test_traces_a_single_sheet_as_one_line_and_a_total() -> None:
    trace = capability().compute(given(("1500", "10000", "0"))).trace

    assert trace == (
        sheet_line(1, "1500", "0", "1500", "10000", "500.00", "500.00"),
        ItemsTotalLine(CREDIT, ((1, D("500.00")),), D("500.00")),
    )


def test_traces_no_sheets_as_only_an_empty_total() -> None:
    assert capability().compute(given()).trace == (ItemsTotalLine(CREDIT, (), D("0")),)


def test_traces_the_rounding_rule_of_the_dataset() -> None:
    wired = capability(rounding(NO_ROUNDING))

    line, _total = wired.compute(
        given(("5", "0.015", "0"), net_income="2", provincial_tax="1")
    ).trace

    assert isinstance(line, ProvincialForeignTaxCreditLine)
    assert line.rounding == NO_ROUNDING
    assert line.line_4 == D("0.0075")


def test_the_last_trace_line_amount_is_the_output() -> None:
    for rows in ((US, UK), (US,), ()):
        result = capability().compute(given(*rows))

        assert result.trace[-1].amount == totals(result)


def test_the_total_is_the_sum_of_its_items() -> None:
    *_, total_line = capability().compute(given(US, UK, ("1500", "10000", "0"))).trace

    assert isinstance(total_line, ItemsTotalLine)
    assert total_line.total == sum((amount for _, amount in total_line.items), D("0"))


def test_compute_is_repeatable() -> None:
    wired = capability()

    assert wired.compute(given(US, UK)) == wired.compute(given(US, UK))


# --- through TaxComputationService --------------------------------------------------------------


class _Jurisdictions:
    def __init__(self, jurisdiction: Jurisdiction) -> None:
        self._jurisdiction = jurisdiction

    def get_jurisdiction(self, code: JurisdictionCode) -> Jurisdiction:
        return self._jurisdiction


class _Parameters:
    def __init__(self, *datasets: ParameterDataset[Any]) -> None:
        self._datasets = {(d.family, d.kind): d for d in datasets}

    def get[T](self, family: str, tax_year: int, kind: ParameterKind[T]) -> ParameterDataset[T]:
        if tax_year != 2025 or (family, kind) not in self._datasets:
            raise NotFoundError(f"no {family} dataset for tax year {tax_year}")
        return cast(ParameterDataset[T], self._datasets[(family, kind)])


def service(dataset: ParameterDataset[RoundingOnly] | None = None) -> TaxComputationService:
    dataset = dataset or rounding()
    code = JurisdictionCode("CA-ON")
    selection = CapabilitySelection(
        name="ca-on/provincial_foreign_tax_credit",
        params={"rounding": dataset.family},
        consumes={
            "sheets": "ca/foreign_tax_credit_sheets",
            "net_income": "ex/net_income",
            "provincial_tax": "ex/provincial_tax",
        },
        produces={"total": "ex/provincial_credit"},
    )
    manifest = Manifest(
        jurisdiction=code,
        version=1,
        valid_from_tax_year=2025,
        inputs=frozenset({"ca/foreign_tax_credit_sheets", "ex/net_income", "ex/provincial_tax"}),
        forms=(
            Form(
                name=code.namespace.identifier("return"),
                instances=None,
                exports=("ex/provincial_credit",),
                capabilities=(selection,),
            ),
        ),
    )
    artifacts = ArtifactRegistry()
    for kind in (SHEETS, NET_INCOME, PROVINCIAL_TAX, CREDIT):
        artifacts.register(kind.identifier, kind)
    return TaxComputationService(
        _Jurisdictions(Jurisdiction(code=code, manifests=(manifest,))),
        _Parameters(dataset),
        CapabilityRegistry.shared(),
        artifacts,
    )


def test_a_computation_builds_the_capability_from_the_registry_and_its_dataset() -> None:
    composition = (
        service().compose(JurisdictionCode("CA-ON"), 2025).form("ca-on/return").composition
    )

    (built,) = composition.order
    assert isinstance(built, ProvincialForeignTaxCredit)
    assert built.consumes == frozenset({SHEETS, NET_INCOME, PROVINCIAL_TAX})
    assert built.produces == frozenset({CREDIT})


def test_a_computation_gives_the_total_of_line_5() -> None:
    worksheet = service().compute(JurisdictionCode("CA-ON"), 2025, *given(US, UK))["ca-on/return"][
        0
    ]

    assert worksheet.get(CREDIT).value == D("100")
    assert isinstance(worksheet.producer_of(CREDIT), ProvincialForeignTaxCredit)
    assert worksheet.trace == (
        sheet_line(1, "1500", "1400", "100", "10000", "500.00", "100"),
        sheet_line(2, "100", "100", "0", "5000", "250.00", "0"),
        ItemsTotalLine(CREDIT, ((1, D("100")), (2, D("0"))), D("100")),
    )


def test_a_computation_with_no_sheets_gives_zero() -> None:
    worksheet = service().compute(JurisdictionCode("CA-ON"), 2025, *given())["ca-on/return"][0]

    assert worksheet.get(CREDIT).value == D("0")


def test_a_computation_refuses_a_zero_net_income() -> None:
    with pytest.raises(ValidationError, match="net_income"):
        service().compute(JurisdictionCode("CA-ON"), 2025, *given(US, net_income="0"))


def test_a_computation_applies_the_datasets_rounding() -> None:
    whole = RoundTo(D("1"), RoundingMode.FLOOR)

    worksheet = service(rounding(whole)).compute(
        JurisdictionCode("CA-ON"),
        2025,
        *given(("50", "10", "0"), net_income="300", provincial_tax="100"),
    )["ca-on/return"][0]

    assert worksheet.get(CREDIT).value == D("3")
