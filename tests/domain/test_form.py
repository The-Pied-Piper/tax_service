"""Unit tests for FormComposition, FormSet and FormWorksheets, with made-up `ex/` names.

A form is a peer of the others, never a capability. `FormComposition` is one form wired: an inner
`Composition` whose inputs are the fields of its instances kind plus its imports and whose outputs
are its exports. An export `X` of the form `B` is read by every other form as the derived kind
`B.X`, a record list of one field with a record per instance. A form's imports are the dotted
kinds it consumes (or, for the return, declares as outputs) that nothing in the form produces.

`FormSet` holds the return form and the others. It orders the forms by their imports (a cycle or
an import nothing exports is an InvalidCompositionError), runs each form once per record of its
instances (the return form once), keeps every form's exports in one store and hands the imports to
each run as starting artifacts. `FormWorksheets` is what it returns: the worksheet of every
instance of every form, by form name and position from 1, and the return form's worksheet.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

import pytest

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.record_total import RecordTotal
from app.domain.capabilities.subtract import Subtract
from app.domain.capability import Capability, CapabilityResult
from app.domain.composition import Composition
from app.domain.errors import (
    CapabilityContractError,
    DomainError,
    InvalidCompositionError,
    MissingArtifactError,
    NotFoundError,
)
from app.domain.form import FormComposition, FormSet, FormWorksheets
from app.domain.record_list import RecordList, RecordListKind
from app.domain.trace import FormInstanceLine, RecordTotalLine, SubtractedLine
from app.domain.worksheet import Worksheet

D = Decimal

SALES = ArtifactKind("ex/sales", Decimal)
COSTS = ArtifactKind("ex/costs", Decimal)
PROFIT = ArtifactKind("ex/profit", Decimal, non_negative=True)
FEE = ArtifactKind("ex/fee", Decimal)
FEE_TOTAL = ArtifactKind("ex/fee_total", Decimal)
PROFIT_TOTAL = ArtifactKind("ex/profit_total", Decimal)
AUDITED = ArtifactKind("ex/audited", Decimal)
LEVY = ArtifactKind("ex/levy", Decimal)
GRAND = ArtifactKind("ex/grand", Decimal)
NOTE = ArtifactKind("ex/note", str)
BROKEN = ArtifactKind("ex/broken", Decimal)

SHOPS = RecordListKind("ex/shops", fields=(SALES, COSTS))
AUDITS = RecordListKind("ex/audits", fields=(FEE,))
SALES_ONLY = RecordListKind("ex/sales_only", fields=(SALES,))

# What the engine derives for the exports: one field, a record per instance.
SHOP_PROFIT = RecordListKind("ex/shop.profit", fields=(PROFIT,))
AUDIT_AUDITED = RecordListKind("ex/audit.audited", fields=(AUDITED,))
AUDIT_FEE = RecordListKind("ex/audit.fee", fields=(FEE,))

RETURN = "ex-on/return"


class Describe(Capability):
    """Produces `note`, a text: not a kind a form may export."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"note": str}

    def __init__(self, source: ArtifactKind[Decimal], note: ArtifactKind[str]) -> None:
        super().__init__(source=source, note=note)
        self._note = note

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        return CapabilityResult(outputs=(Artifact(self._note, "x"),), trace=())


class Reject(Capability):
    """Produces `target` as `source`, but raises a DomainError, not a contract error, on 666."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"source": Decimal}
    PRODUCES: ClassVar[Mapping[str, type]] = {"target": Decimal}

    def __init__(self, source: ArtifactKind[Decimal], target: ArtifactKind[Decimal]) -> None:
        super().__init__(source=source, target=target)
        self._source, self._target = source, target

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        value = self._input(inputs, self._source).value
        if value == 666:
            raise DomainError("666 is not accepted")
        return CapabilityResult(outputs=(Artifact(self._target, value),), trace=())


def shop(name: str = "ex/shop") -> FormComposition:
    """Profit of each shop: sales less costs; exports the profit."""
    return FormComposition(
        name,
        [Subtract(SALES, COSTS, PROFIT)],
        instances=SHOPS,
        exports=[PROFIT],
    )


def audit(name: str = "ex/audit") -> FormComposition:
    """Each audit: the fee less the total profit of all the shops; exports the result."""
    return FormComposition(
        name,
        [RecordTotal(SHOP_PROFIT, PROFIT_TOTAL), Subtract(PROFIT_TOTAL, FEE, AUDITED)],
        instances=AUDITS,
        exports=[AUDITED],
    )


def form_set(*forms: FormComposition) -> FormSet:
    return FormSet(
        RETURN,
        [RecordTotal(AUDIT_AUDITED, GRAND)],
        inputs=frozenset(form.instances for form in forms if form.instances is not None),
        outputs=frozenset({GRAND}),
        forms=forms,
    )


def shops(*pairs: tuple[str, str]) -> Artifact[Any]:
    return Artifact(SHOPS, RecordList(SHOPS.fields, [{SALES: D(s), COSTS: D(c)} for s, c in pairs]))


def audits(*fees: str) -> Artifact[Any]:
    return Artifact(AUDITS, RecordList(AUDITS.fields, [{FEE: D(f)} for f in fees]))


TWO_SHOPS = shops(("12000", "2000"), ("5000", "1000"))
TWO_AUDITS = audits("100", "30")


def values(worksheet: Worksheet, kind: RecordListKind) -> list[Decimal]:
    (field,) = kind.fields
    return [record[field] for record in worksheet.get(kind).value.records]


# --- a form wired: its derived kinds, instance fields and imports --------------------------------


def test_an_exports_derived_kind_is_a_record_list_of_that_one_field() -> None:
    assert shop().derived == (SHOP_PROFIT,)


def test_the_derived_kinds_can_be_built_before_any_selection_is() -> None:
    assert FormComposition.derive("ex/shop", [PROFIT]) == (SHOP_PROFIT,)
    assert FormComposition.derive("ex/audit", [AUDITED, FEE]) == (AUDIT_AUDITED, AUDIT_FEE)


def test_a_form_has_no_imports_when_it_reads_only_its_instance_fields() -> None:
    assert shop().imports == frozenset()


def test_the_imports_are_the_dotted_kinds_the_form_consumes_and_does_not_produce() -> None:
    assert audit().imports == frozenset({SHOP_PROFIT})


def test_the_form_remembers_its_name_instances_and_exports() -> None:
    found = audit()

    assert found.name == "ex/audit"
    assert found.instances is AUDITS
    assert found.exports == (AUDITED,)


def test_the_inner_composition_takes_the_instance_fields_and_the_imports() -> None:
    inner = audit().composition

    assert isinstance(inner, Composition)
    with pytest.raises(InvalidCompositionError, match="missing inputs 'fee', 'shop.profit'"):
        inner.compute()
    inner.compute(
        Artifact(FEE, D(1)),
        Artifact(SHOP_PROFIT, RecordList(SHOP_PROFIT.fields, [{PROFIT: D(5)}])),
    )


def test_an_instance_field_nothing_reads_is_refused_naming_the_form() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/shop.*'costs' is consumed by nothing"):
        FormComposition("ex/shop", [Reject(SALES, PROFIT)], instances=SHOPS, exports=[PROFIT])


def test_a_selection_without_a_producer_is_refused_naming_the_form() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/shop.*no producer for 'fee'"):
        FormComposition(
            "ex/shop",
            [Subtract(SALES, COSTS, PROFIT), Subtract(PROFIT, FEE, AUDITED)],
            instances=SHOPS,
            exports=[AUDITED],
        )


def test_an_export_nothing_in_the_form_produces_is_refused_naming_the_form() -> None:
    with pytest.raises(
        InvalidCompositionError, match="ex/shop.*output 'fee' is produced by nothing"
    ):
        FormComposition(
            "ex/shop", [Subtract(SALES, COSTS, PROFIT)], instances=SHOPS, exports=[PROFIT, FEE]
        )


def test_an_export_that_is_neither_an_amount_a_count_nor_a_record_list_is_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/labelled.*ex/note"):
        FormComposition(
            "ex/labelled", [Describe(SALES, NOTE)], instances=SALES_ONLY, exports=[NOTE]
        )


def test_a_form_must_export_something() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/shop.*exports"):
        FormComposition("ex/shop", [Subtract(SALES, COSTS, PROFIT)], instances=SHOPS, exports=[])


# --- the set: order by imports ------------------------------------------------------------------


def test_a_form_that_imports_runs_after_the_form_that_exports_it_even_if_listed_first() -> None:
    first_listed = form_set(audit(), shop())

    assert [found.name for found in first_listed.forms] == ["ex/shop", "ex/audit"]


def test_forms_that_do_not_import_each_other_run_in_name_order() -> None:
    forms = FormSet(
        RETURN,
        [Subtract(LEVY, FEE_TOTAL, GRAND)],
        inputs=frozenset({SHOPS, LEVY, FEE_TOTAL}),
        outputs=frozenset({GRAND}),
        forms=[shop("ex/zebra"), shop("ex/apple"), shop("ex/mango")],
    )

    assert [found.name for found in forms.forms] == ["ex/apple", "ex/mango", "ex/zebra"]


def test_the_order_does_not_depend_on_how_the_forms_were_listed() -> None:
    assert [f.name for f in form_set(shop(), audit()).forms] == [
        f.name for f in form_set(audit(), shop()).forms
    ]


def test_a_cycle_of_imports_is_refused_naming_the_forms_on_it() -> None:
    # shop imports audit.audited, audit imports shop.profit.
    shop_needs_audit = FormComposition(
        "ex/shop",
        [Subtract(SALES, COSTS, PROFIT), RecordTotal(AUDIT_AUDITED, FEE_TOTAL)],
        instances=SHOPS,
        exports=[PROFIT, FEE_TOTAL],
    )
    audit_exporting_total = audit()

    with pytest.raises(InvalidCompositionError, match="cycle") as caught:
        form_set(shop_needs_audit, audit_exporting_total)

    assert "ex/shop" in str(caught.value) and "ex/audit" in str(caught.value)


def test_a_form_importing_its_own_export_is_a_cycle_naming_it() -> None:
    greedy = FormComposition(
        "ex/shop",
        [Subtract(SALES, COSTS, PROFIT), RecordTotal(SHOP_PROFIT, PROFIT_TOTAL)],
        instances=SHOPS,
        exports=[PROFIT, PROFIT_TOTAL],
    )

    with pytest.raises(InvalidCompositionError, match=r"cycle.*ex/shop") as caught:
        form_set(greedy, audit())

    assert "ex/audit" not in str(caught.value)


def test_a_form_outside_the_cycle_is_not_named() -> None:
    shop_needs_audit = FormComposition(
        "ex/shop",
        [Subtract(SALES, COSTS, PROFIT), RecordTotal(AUDIT_AUDITED, FEE_TOTAL)],
        instances=SHOPS,
        exports=[PROFIT, FEE_TOTAL],
    )

    with pytest.raises(InvalidCompositionError, match="cycle") as caught:
        form_set(shop_needs_audit, audit(), shop("ex/bystander"))

    assert "ex/bystander" not in str(caught.value)


def test_an_import_no_form_exports_is_refused_naming_the_form_and_the_kind() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/audit.*no form exports 'shop.profit'"):
        form_set(audit())


def test_an_import_of_another_shape_than_the_export_is_refused() -> None:
    other = RecordListKind("ex/shop.profit", fields=(SALES,))
    needs_sales = FormComposition(
        "ex/audit",
        [RecordTotal(other, PROFIT_TOTAL), Subtract(PROFIT_TOTAL, FEE, AUDITED)],
        instances=AUDITS,
        exports=[AUDITED],
    )

    with pytest.raises(InvalidCompositionError, match="ex/audit.*'shop.profit'"):
        form_set(shop(), needs_sales)


def test_the_returns_import_no_form_exports_is_refused_naming_the_return() -> None:
    with pytest.raises(InvalidCompositionError, match=r"ex-on/return.*'audit.audited'"):
        form_set(shop())


def test_two_forms_of_one_name_are_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/shop.*more than once"):
        form_set(shop(), shop())


def test_a_form_named_like_the_return_is_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="ex-on/return.*more than once"):
        form_set(shop(RETURN), audit())


def test_a_forms_instances_kind_must_be_one_of_the_computations_inputs() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/shop.*'ex/shops'.*not.*input"):
        FormSet(
            RETURN,
            [Subtract(FEE, COSTS, LEVY)],
            inputs=frozenset({FEE, COSTS}),
            outputs=frozenset({LEVY}),
            forms=[shop()],
        )


def test_the_return_form_has_no_instances_and_no_derived_kinds() -> None:
    returns = form_set(shop(), audit()).return_form

    assert returns.name == RETURN
    assert returns.instances is None
    assert returns.derived == ()
    assert returns.imports == frozenset({AUDIT_AUDITED})


def test_the_return_forms_inputs_are_the_computations_inputs_less_the_instances_kinds() -> None:
    plain = FormSet(
        RETURN,
        [Subtract(SALES, COSTS, LEVY)],
        inputs=frozenset({SALES, COSTS, AUDITS}),
        outputs=frozenset({LEVY}),
        forms=[
            FormComposition("ex/audit", [Reject(FEE, AUDITED)], instances=AUDITS, exports=[AUDITED])
        ],
    )

    inner = plain.return_form.composition
    inner.compute(Artifact(SALES, D(3)), Artifact(COSTS, D(1)))
    with pytest.raises(InvalidCompositionError, match="'audits' is not an input"):
        inner.compute(Artifact(SALES, D(3)), Artifact(COSTS, D(1)), audits("1"))


# --- the run: peers reading each other's exports ------------------------------------------------


def test_a_form_reads_the_exports_of_another_form_on_each_of_its_instances() -> None:
    result = form_set(audit(), shop()).compute(TWO_SHOPS, TWO_AUDITS)

    # total profit 10000 + 4000, less each fee.
    first, second = result.worksheets("ex/audit")
    assert first.get(AUDITED).value == D("13900")
    assert second.get(AUDITED).value == D("13970")


def test_the_import_reaches_the_instance_as_a_starting_artifact() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    worksheet = result.worksheet("ex/audit", 2)

    assert worksheet.producer_of(SHOP_PROFIT) is None
    assert values(worksheet, SHOP_PROFIT) == [D(10000), D(4000)]


def test_an_export_is_a_record_list_of_one_field_with_a_record_per_instance_in_order() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert result.worksheet("ex/audit", 1).get(SHOP_PROFIT).value == RecordList(
        (PROFIT,), [{PROFIT: D(10000)}, {PROFIT: D(4000)}]
    )


def test_instance_order_is_the_order_of_the_records_given() -> None:
    swapped = shops(("5000", "1000"), ("12000", "2000"))

    result = form_set(shop(), audit()).compute(swapped, TWO_AUDITS)

    assert values(result.worksheet("ex/audit", 1), SHOP_PROFIT) == [D(4000), D(10000)]


def test_two_forms_importing_one_export_both_see_all_its_records() -> None:
    review = FormComposition(
        "ex/review",
        [RecordTotal(SHOP_PROFIT, PROFIT_TOTAL), Subtract(PROFIT_TOTAL, FEE, AUDITED)],
        instances=AUDITS,
        exports=[AUDITED],
    )
    forms = FormSet(
        RETURN,
        [RecordTotal(AUDIT_AUDITED, GRAND)],
        inputs=frozenset({SHOPS, AUDITS}),
        outputs=frozenset({GRAND}),
        forms=[shop(), audit(), review],
    )

    result = forms.compute(TWO_SHOPS, TWO_AUDITS)

    assert result.worksheet("ex/audit", 1).get(AUDITED).value == D("13900")
    assert result.worksheet("ex/review", 1).get(AUDITED).value == D("13900")
    assert values(result.worksheet("ex/review", 2), SHOP_PROFIT) == [D(10000), D(4000)]


def test_the_return_form_imports_and_keeps_the_import_with_its_intermediates() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    returns = result.return_worksheet

    assert returns.get(GRAND).value == D("13900") + D("13970")
    assert values(returns, AUDIT_AUDITED) == [D("13900"), D("13970")]
    assert returns.producer_of(AUDIT_AUDITED) is None


def test_the_return_form_runs_once_whatever_the_instances() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert result.worksheets(RETURN) == (result.return_worksheet,)
    assert result.worksheet(RETURN, 1) is result.return_worksheet


def test_a_declared_output_that_is_an_import_is_carried_onto_the_return() -> None:
    carried = FormSet(
        RETURN,
        [RecordTotal(SHOP_PROFIT, PROFIT_TOTAL)],
        inputs=frozenset({SHOPS}),
        outputs=frozenset({PROFIT_TOTAL, SHOP_PROFIT}),
        forms=[shop()],
    )

    result = carried.compute(TWO_SHOPS)

    assert values(result.return_worksheet, SHOP_PROFIT) == [D(10000), D(4000)]
    assert result.return_worksheet.get(PROFIT_TOTAL).value == D(14000)


def test_an_inner_artifact_that_is_not_an_export_is_not_on_the_other_forms_worksheets() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    for worksheet in (*result.worksheets("ex/audit"), result.return_worksheet):
        with pytest.raises(MissingArtifactError, match="no value"):
            worksheet.get(PROFIT)


# --- zero instances -----------------------------------------------------------------------------


def test_no_instances_still_produces_every_export_as_an_empty_record_list() -> None:
    result = form_set(shop(), audit()).compute(shops(), TWO_AUDITS)

    assert result.worksheet("ex/audit", 1).get(SHOP_PROFIT).value == RecordList((PROFIT,), [])


def test_an_importer_of_an_empty_export_computes_on_the_empty_list() -> None:
    result = form_set(shop(), audit()).compute(shops(), TWO_AUDITS)

    assert result.worksheet("ex/audit", 1).get(PROFIT_TOTAL).value == D(0)
    assert result.return_worksheet.get(GRAND).value == D("-130")


def test_a_form_of_no_instances_has_no_worksheets_and_no_trace_line() -> None:
    result = form_set(shop(), audit()).compute(shops(), audits())

    assert result.worksheets("ex/shop") == ()
    assert result.worksheets("ex/audit") == ()
    assert result.return_worksheet.get(GRAND).value == D(0)
    assert [type(line) for line in result.trace] == [RecordTotalLine]


# --- per-instance worksheets, reachable --------------------------------------------------------


def test_every_instance_keeps_its_own_worksheet_by_form_and_position_from_1() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert isinstance(result, FormWorksheets)
    first, second = result.worksheets("ex/shop")
    assert isinstance(first, Worksheet) and isinstance(second, Worksheet)
    assert result.worksheet("ex/shop", 1) is first
    assert result.worksheet("ex/shop", 2) is second
    assert first.get(PROFIT).value == D(10000)
    assert second.get(PROFIT).value == D(4000)
    assert first.get(SALES).value == D(12000)
    assert second.get(COSTS).value == D(1000)


def test_a_worksheet_holds_the_instances_starting_fields_and_intermediates_of_that_instance() -> (
    None
):
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    worksheet = result.worksheet("ex/audit", 2)

    assert worksheet.get(FEE).value == D(30)
    assert worksheet.get(PROFIT_TOTAL).value == D(14000)
    assert worksheet.get(AUDITED).value == D(13970)


def test_the_forms_are_named_in_the_order_they_ran_the_return_last() -> None:
    result = form_set(audit(), shop()).compute(TWO_SHOPS, TWO_AUDITS)

    assert result.forms == ("ex/shop", "ex/audit", RETURN)


@pytest.mark.parametrize("position", [0, 3, -1])
def test_an_instance_position_outside_the_instances_is_not_found(position: int) -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    with pytest.raises(NotFoundError, match=rf"ex/shop.*{position}"):
        result.worksheet("ex/shop", position)


def test_a_form_the_set_does_not_hold_is_not_found() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    with pytest.raises(NotFoundError, match="ex/nowhere"):
        result.worksheets("ex/nowhere")
    with pytest.raises(NotFoundError, match="ex/nowhere"):
        result.worksheet("ex/nowhere", 1)


# --- the trace: one line per instance, then the returns own lines ------------------------------


def test_the_trace_has_one_line_per_instance_in_run_order_then_the_returns_lines() -> None:
    result = form_set(audit(), shop()).compute(TWO_SHOPS, TWO_AUDITS)

    lines = result.trace
    instance_lines = [line for line in lines if isinstance(line, FormInstanceLine)]

    assert [(line.form, line.position) for line in instance_lines] == [
        ("ex/shop", 1),
        ("ex/shop", 2),
        ("ex/audit", 1),
        ("ex/audit", 2),
    ]
    assert lines[:4] == tuple(instance_lines)
    assert lines[4:] == result.return_worksheet.trace
    assert [type(line) for line in lines[4:]] == [RecordTotalLine]


def test_an_instances_line_holds_the_trace_of_that_instances_own_worksheet() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    first = result.trace[0]

    assert isinstance(first, FormInstanceLine)
    assert first.lines == result.worksheet("ex/shop", 1).trace
    assert [type(line) for line in first.lines] == [SubtractedLine]


# --- the starting artifacts ---------------------------------------------------------------------


def test_the_instances_of_every_form_are_required() -> None:
    with pytest.raises(InvalidCompositionError, match="missing input 'audits'"):
        form_set(shop(), audit()).compute(TWO_SHOPS)


def test_all_missing_instances_are_named() -> None:
    with pytest.raises(InvalidCompositionError, match="missing inputs 'audits', 'shops'"):
        form_set(shop(), audit()).compute()


def test_an_artifact_that_is_not_an_input_is_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="'fee' is not an input"):
        form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS, Artifact(FEE, D(1)))


def test_an_import_cannot_be_given_as_a_starting_artifact() -> None:
    given = Artifact(SHOP_PROFIT, RecordList(SHOP_PROFIT.fields, []))

    with pytest.raises(InvalidCompositionError, match="'shop.profit'"):
        form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS, given)


# --- errors name the form and the instance position --------------------------------------------


@pytest.mark.parametrize("position", [1, 2])
def test_a_failure_inside_an_instance_names_the_form_and_the_position(position: int) -> None:
    pairs = [("1000", "100"), ("1000", "100")]
    pairs[position - 1] = ("100", "500")  # a loss: PROFIT is non-negative

    with pytest.raises(CapabilityContractError, match=rf"ex/shop, instance {position}\b") as caught:
        form_set(shop(), audit()).compute(shops(*pairs), TWO_AUDITS)

    assert "profit" in str(caught.value)


def test_a_non_contract_domain_error_keeps_its_class_and_gains_the_names() -> None:
    guarded = FormComposition(
        "ex/shop",
        [Reject(SALES, BROKEN), Subtract(BROKEN, COSTS, PROFIT)],
        instances=SHOPS,
        exports=[PROFIT],
    )

    with pytest.raises(DomainError, match=r"ex/shop, instance 2: 666 is not accepted") as caught:
        form_set(guarded, audit()).compute(shops(("1000", "1"), ("666", "1")), TWO_AUDITS)

    assert type(caught.value) is DomainError


def test_a_failure_in_a_form_that_imports_names_that_form_and_the_instance() -> None:
    guarded = FormComposition(
        "ex/audit",
        [
            Reject(FEE, BROKEN),
            RecordTotal(SHOP_PROFIT, PROFIT_TOTAL),
            Subtract(PROFIT_TOTAL, BROKEN, AUDITED),
        ],
        instances=AUDITS,
        exports=[AUDITED],
    )

    with pytest.raises(DomainError, match=r"ex/audit, instance 2: 666 is not accepted"):
        form_set(shop(), guarded).compute(TWO_SHOPS, audits("100", "666"))


def test_the_returns_own_failure_is_not_prefixed_with_a_form_and_position() -> None:
    boom = FormSet(
        RETURN,
        [Subtract(SALES, COSTS, PROFIT)],
        inputs=frozenset({SALES, COSTS}),
        outputs=frozenset({PROFIT}),
    )

    with pytest.raises(CapabilityContractError) as caught:
        boom.compute(Artifact(SALES, D(1)), Artifact(COSTS, D(2)))

    assert "instance" not in str(caught.value)


# --- a set of no forms behaves as the bare composition -----------------------------------------


def lone_set() -> FormSet:
    return FormSet(
        RETURN,
        [Subtract(SALES, COSTS, LEVY)],
        inputs=frozenset({SALES, COSTS}),
        outputs=frozenset({LEVY}),
    )


def lone_composition() -> Composition:
    return Composition(
        [Subtract(SALES, COSTS, LEVY)],
        inputs=frozenset({SALES, COSTS}),
        outputs=frozenset({LEVY}),
    )


def test_a_set_of_only_the_return_form_computes_what_the_composition_does() -> None:
    given = (Artifact(SALES, D(10)), Artifact(COSTS, D(4)))

    result = lone_set().compute(*given)

    assert result.return_worksheet.get(LEVY) == lone_composition().compute(*given).get(LEVY)
    assert result.return_worksheet.trace == lone_composition().compute(*given).trace
    assert result.trace == result.return_worksheet.trace
    assert result.forms == (RETURN,)


def test_its_errors_are_those_of_the_composition_unprefixed() -> None:
    for arguments in ((), (Artifact(SALES, D(1)),), (Artifact(FEE, D(1)),)):
        with pytest.raises(InvalidCompositionError) as bare:
            lone_composition().compute(*arguments)
        with pytest.raises(InvalidCompositionError) as wrapped:
            lone_set().compute(*arguments)
        assert str(wrapped.value) == str(bare.value)


def test_its_wiring_errors_are_those_of_the_composition_unprefixed() -> None:
    with pytest.raises(InvalidCompositionError) as bare:
        Composition(
            [Subtract(SALES, COSTS, LEVY)], inputs=frozenset({SALES}), outputs=frozenset({LEVY})
        )
    with pytest.raises(InvalidCompositionError) as wrapped:
        FormSet(
            RETURN,
            [Subtract(SALES, COSTS, LEVY)],
            inputs=frozenset({SALES}),
            outputs=frozenset({LEVY}),
        )

    assert str(wrapped.value) == str(bare.value)


def test_the_return_composition_is_the_one_the_bare_wiring_would_give() -> None:
    assert [type(c) for c in lone_set().return_form.composition.order] == [Subtract]
