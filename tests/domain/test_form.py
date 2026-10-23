"""Unit tests for FormComposition and FormSet, with made-up `ex/` names.

A computation is a flat set of forms; a form is a peer of the others, never a capability, and none
is special. `FormComposition` is one form wired: an inner `Composition` whose outputs are its
exports and whose inputs are derived: the fields of its instances kind, or, for a form without
instances, the starting artifacts it reads, plus its imports. An export `X` of the form `B` is read
by every form as the derived kind `B.X`, a record list of one field with a record per instance (one
record for a form without an instances list: it has one instance). A form's imports are the
dotted kinds it consumes and nothing in the form produces.

`FormSet` holds the forms. It orders them by their imports (a cycle or an import nothing exports
is an InvalidCompositionError), runs each form once per record of its instances (a form without
instances has one), keeps every form's exports in one store and hands the imports to each run as
starting artifacts. It returns a plain mapping: form name to the worksheet of every instance, in
instance order.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
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
    DuplicateArtifactError,
    InvalidCompositionError,
    MissingArtifactError,
    NotFoundError,
)
from app.domain.form import FormComposition, FormSet
from app.domain.record_list import RecordList, RecordListKind
from app.domain.trace import FormInstanceLine, RecordTotalLine, SubtractedLine, TraceLine
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
RETURN_GRAND = RecordListKind("ex-on/return.grand", fields=(GRAND,))
FIRST_TOTAL = RecordListKind("ex/first.fee_total", fields=(FEE_TOTAL,))
SECOND_TOTAL = RecordListKind("ex/second.profit_total", fields=(PROFIT_TOTAL,))


class Describe(Capability):
    """Produces `note`, a text: not a kind a record can hold."""

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


def flat(
    capabilities: list[Capability],
    *,
    inputs: frozenset[ArtifactKind[Any]],
    outputs: frozenset[ArtifactKind[Any]],
    forms: Iterable[FormComposition] = (),
) -> FormSet:
    """The forms plus a form `ex-on/return` of `capabilities`, which has one instance."""
    default = FormComposition(
        RETURN,
        capabilities,
        exports=sorted(outputs, key=lambda kind: kind.identifier),
        starting=inputs,
    )
    return FormSet([*forms, default], inputs=inputs)


def form_set(*forms: FormComposition) -> FormSet:
    return flat(
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


def test_an_export_that_is_neither_an_amount_a_count_nor_a_record_list_is_not_importable() -> None:
    labelled = FormComposition(
        "ex/labelled", [Describe(SALES, NOTE)], instances=SALES_ONLY, exports=[NOTE]
    )

    assert labelled.exports == (NOTE,)
    assert labelled.derived == ()
    assert FormComposition.derive("ex/labelled", [NOTE, SALES]) == (
        RecordListKind("ex/labelled.sales", fields=(SALES,)),
    )


def test_an_export_that_is_another_forms_export_is_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/audit.*'ex/shop.profit'.*another form"):
        FormComposition(
            "ex/audit",
            [RecordTotal(SHOP_PROFIT, PROFIT_TOTAL)],
            instances=AUDITS,
            exports=[PROFIT_TOTAL, SHOP_PROFIT],
        )


def test_a_form_must_export_something() -> None:
    with pytest.raises(InvalidCompositionError, match="ex/shop.*exports"):
        FormComposition("ex/shop", [Subtract(SALES, COSTS, PROFIT)], instances=SHOPS, exports=[])


def test_instances_that_are_not_a_record_list_are_refused_naming_the_form() -> None:
    with pytest.raises(
        InvalidCompositionError, match="form 'ex/shop': instances 'ex/sales' is not a record list"
    ):
        FormComposition(
            "ex/shop", [Subtract(SALES, COSTS, PROFIT)], instances=SALES, exports=[PROFIT]
        )


# --- the set: order by imports ------------------------------------------------------------------


def test_a_form_that_imports_runs_after_the_form_that_exports_it_even_if_listed_first() -> None:
    first_listed = form_set(audit(), shop())

    assert [found.name for found in first_listed.forms] == ["ex/shop", "ex/audit", RETURN]


def test_forms_that_do_not_import_each_other_run_in_name_order() -> None:
    forms = flat(
        [Subtract(LEVY, FEE_TOTAL, GRAND)],
        inputs=frozenset({SHOPS, LEVY, FEE_TOTAL}),
        outputs=frozenset({GRAND}),
        forms=[shop("ex/zebra"), shop("ex/apple"), shop("ex/mango")],
    )

    assert [found.name for found in forms.forms] == [RETURN, "ex/apple", "ex/mango", "ex/zebra"]


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
        flat(
            [Subtract(FEE, COSTS, LEVY)],
            inputs=frozenset({FEE, COSTS}),
            outputs=frozenset({LEVY}),
            forms=[shop()],
        )


def test_the_default_form_is_an_ordinary_form_with_one_instance_that_exports_like_any() -> None:
    returns = form_set(shop(), audit()).form(RETURN)

    assert returns.name == RETURN
    assert returns.instances is None
    assert returns.exports == (GRAND,)
    assert returns.derived == (RETURN_GRAND,)
    assert returns.imports == frozenset({AUDIT_AUDITED})


def test_a_form_without_instances_takes_the_starting_artifacts_it_reads() -> None:
    once = FormComposition(
        "ex/once",
        [Subtract(SALES, COSTS, LEVY)],
        exports=[LEVY],
        starting=frozenset({SALES, COSTS, FEE}),
    )

    assert once.inputs == frozenset({SALES, COSTS})  # FEE is a starting artifact it does not read
    assert once.imports == frozenset()


def test_a_form_without_instances_reads_the_starting_artifacts_it_exports_unchanged() -> None:
    once = FormComposition(
        "ex/once",
        [Subtract(SALES, COSTS, LEVY)],
        exports=[LEVY, FEE],
        starting=frozenset({SALES, COSTS, FEE}),
    )

    assert once.inputs == frozenset({SALES, COSTS, FEE})


def test_a_form_without_instances_does_not_take_what_is_not_a_starting_artifact() -> None:
    with pytest.raises(InvalidCompositionError, match="no producer for 'costs'") as caught:
        FormComposition(
            "ex/once", [Subtract(SALES, COSTS, LEVY)], exports=[LEVY], starting=frozenset({SALES})
        )

    assert str(caught.value).startswith("form 'ex/once': ")  # wired before any instance exists
    assert "instance" not in str(caught.value)


def test_a_forms_inputs_are_only_the_starting_artifacts_it_reads() -> None:
    plain = flat(
        [Subtract(SALES, COSTS, LEVY)],
        inputs=frozenset({SALES, COSTS, AUDITS}),
        outputs=frozenset({LEVY}),
        forms=[
            FormComposition("ex/audit", [Reject(FEE, AUDITED)], instances=AUDITS, exports=[AUDITED])
        ],
    )

    inner = plain.form(RETURN).composition
    inner.compute(Artifact(SALES, D(3)), Artifact(COSTS, D(1)))
    with pytest.raises(InvalidCompositionError, match="'audits' is not an input"):
        inner.compute(Artifact(SALES, D(3)), Artifact(COSTS, D(1)), audits("1"))


def test_a_derived_kind_among_the_inputs_is_refused_when_the_set_is_built() -> None:
    with pytest.raises(
        InvalidCompositionError, match="'shop.profit' is exported by a form, not an input"
    ):
        flat(
            [RecordTotal(AUDIT_AUDITED, GRAND)],
            inputs=frozenset({SHOPS, AUDITS, SHOP_PROFIT}),
            outputs=frozenset({GRAND}),
            forms=[shop(), audit()],
        )


def test_a_cycle_between_forms_without_instances_is_refused_naming_them() -> None:
    first = FormComposition("ex/first", [RecordTotal(SECOND_TOTAL, FEE_TOTAL)], exports=[FEE_TOTAL])
    second = FormComposition(
        "ex/second", [RecordTotal(FIRST_TOTAL, PROFIT_TOTAL)], exports=[PROFIT_TOTAL]
    )

    with pytest.raises(InvalidCompositionError, match="cycle") as caught:
        FormSet([first, second], inputs=frozenset())

    assert "ex/first" in str(caught.value) and "ex/second" in str(caught.value)


def test_an_import_no_form_exports_is_refused_for_a_form_without_instances() -> None:
    lonely = FormComposition(
        "ex/lonely", [RecordTotal(SECOND_TOTAL, FEE_TOTAL)], exports=[FEE_TOTAL]
    )

    with pytest.raises(
        InvalidCompositionError, match="ex/lonely.*no form exports 'second.profit_total'"
    ):
        FormSet([lonely], inputs=frozenset())


def test_an_input_no_form_reads_is_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="input 'fee' is consumed by nothing"):
        flat(
            [Subtract(SALES, COSTS, LEVY)],
            inputs=frozenset({SALES, COSTS, FEE}),
            outputs=frozenset({LEVY}),
        )


def test_an_input_one_form_reads_and_another_form_does_not_is_fine() -> None:
    forms = flat(
        [Subtract(SALES, COSTS, LEVY)],
        inputs=frozenset({SALES, COSTS, FEE}),
        outputs=frozenset({LEVY}),
        forms=[
            FormComposition(
                "ex/fees",
                [Reject(FEE, FEE_TOTAL)],
                exports=[FEE_TOTAL],
                starting=frozenset({SALES, COSTS, FEE}),
            )
        ],
    )

    result = forms.compute(Artifact(SALES, D(5)), Artifact(COSTS, D(2)), Artifact(FEE, D(1)))

    assert result[RETURN][0].get(LEVY).value == D(3)
    assert result["ex/fees"][0].get(FEE_TOTAL).value == D(1)
    assert forms.form("ex/fees").inputs == frozenset({FEE})


def test_an_input_that_a_form_also_produces_is_refused() -> None:
    with pytest.raises(InvalidCompositionError, match="input 'levy' is also produced by Subtract"):
        flat(
            [Subtract(SALES, COSTS, LEVY)],
            inputs=frozenset({SALES, COSTS, LEVY}),
            outputs=frozenset({LEVY}),
        )


# --- the run: peers reading each other's exports ------------------------------------------------


def test_a_form_reads_the_exports_of_another_form_on_each_of_its_instances() -> None:
    result = form_set(audit(), shop()).compute(TWO_SHOPS, TWO_AUDITS)

    # total profit 10000 + 4000, less each fee.
    first, second = result["ex/audit"]
    assert first.get(AUDITED).value == D("13900")
    assert second.get(AUDITED).value == D("13970")


def test_the_import_reaches_the_instance_as_a_starting_artifact() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    worksheet = result["ex/audit"][1]

    assert worksheet.producer_of(SHOP_PROFIT) is None
    assert values(worksheet, SHOP_PROFIT) == [D(10000), D(4000)]


def test_an_export_is_a_record_list_of_one_field_with_a_record_per_instance_in_order() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert result["ex/audit"][0].get(SHOP_PROFIT).value == RecordList(
        (PROFIT,), [{PROFIT: D(10000)}, {PROFIT: D(4000)}]
    )


def test_instance_order_is_the_order_of_the_records_given() -> None:
    swapped = shops(("5000", "1000"), ("12000", "2000"))

    result = form_set(shop(), audit()).compute(swapped, TWO_AUDITS)

    assert values(result["ex/audit"][0], SHOP_PROFIT) == [D(4000), D(10000)]


def test_two_forms_importing_one_export_both_see_all_its_records() -> None:
    review = FormComposition(
        "ex/review",
        [RecordTotal(SHOP_PROFIT, PROFIT_TOTAL), Subtract(PROFIT_TOTAL, FEE, AUDITED)],
        instances=AUDITS,
        exports=[AUDITED],
    )
    forms = flat(
        [RecordTotal(AUDIT_AUDITED, GRAND)],
        inputs=frozenset({SHOPS, AUDITS}),
        outputs=frozenset({GRAND}),
        forms=[shop(), audit(), review],
    )

    result = forms.compute(TWO_SHOPS, TWO_AUDITS)

    assert result["ex/audit"][0].get(AUDITED).value == D("13900")
    assert result["ex/review"][0].get(AUDITED).value == D("13900")
    assert values(result["ex/review"][1], SHOP_PROFIT) == [D(10000), D(4000)]


def test_the_return_form_imports_and_keeps_the_import_with_its_intermediates() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    returns = result[RETURN][0]

    assert returns.get(GRAND).value == D("13900") + D("13970")
    assert values(returns, AUDIT_AUDITED) == [D("13900"), D("13970")]
    assert returns.producer_of(AUDIT_AUDITED) is None


def test_the_return_form_runs_once_whatever_the_instances() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert result[RETURN] == (result[RETURN][0],)
    assert result[RETURN][0] is result[RETURN][0]


def test_a_form_without_instances_exports_one_record_that_other_forms_read() -> None:
    summary = FormComposition(
        "ex/summary", [RecordTotal(RETURN_GRAND, PROFIT_TOTAL)], exports=[PROFIT_TOTAL]
    )
    # RETURN_GRAND is the default form's export: one record whatever the instances.
    forms = FormSet(
        [*form_set(shop(), audit()).forms, summary],
        inputs=frozenset({SHOPS, AUDITS}),
    )

    result = forms.compute(TWO_SHOPS, TWO_AUDITS)

    (only,) = result["ex/summary"]
    assert values(only, RETURN_GRAND) == [D("27870")]
    assert only.get(PROFIT_TOTAL).value == D("27870")


def test_an_inner_artifact_that_is_not_an_export_is_not_on_the_other_forms_worksheets() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    for worksheet in (*result["ex/audit"], result[RETURN][0]):
        with pytest.raises(MissingArtifactError, match="no value"):
            worksheet.get(PROFIT)


# --- zero instances -----------------------------------------------------------------------------


def test_no_instances_still_produces_every_export_as_an_empty_record_list() -> None:
    result = form_set(shop(), audit()).compute(shops(), TWO_AUDITS)

    assert result["ex/audit"][0].get(SHOP_PROFIT).value == RecordList((PROFIT,), [])


def test_an_importer_of_an_empty_export_computes_on_the_empty_list() -> None:
    result = form_set(shop(), audit()).compute(shops(), TWO_AUDITS)

    assert result["ex/audit"][0].get(PROFIT_TOTAL).value == D(0)
    assert result[RETURN][0].get(GRAND).value == D("-130")


def test_a_form_of_no_instances_has_no_worksheets_and_no_trace_line() -> None:
    forms = form_set(shop(), audit())
    result = forms.compute(shops(), audits())

    assert result["ex/shop"] == ()
    assert result["ex/audit"] == ()
    assert result[RETURN][0].get(GRAND).value == D(0)
    assert [(line.form, line.position) for line in instance_lines(forms.trace(result))] == [
        (RETURN, 1)
    ]


# --- per-instance worksheets, reachable --------------------------------------------------------


def test_every_instance_keeps_its_own_worksheet_by_form_and_position_from_1() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert isinstance(result, dict)
    first, second = result["ex/shop"]
    assert isinstance(first, Worksheet) and isinstance(second, Worksheet)
    assert result["ex/shop"][0] is first
    assert result["ex/shop"][1] is second
    assert first.get(PROFIT).value == D(10000)
    assert second.get(PROFIT).value == D(4000)
    assert first.get(SALES).value == D(12000)
    assert second.get(COSTS).value == D(1000)


def test_a_worksheet_holds_the_instances_starting_fields_and_intermediates_of_that_instance() -> (
    None
):
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    worksheet = result["ex/audit"][1]

    assert worksheet.get(FEE).value == D(30)
    assert worksheet.get(PROFIT_TOTAL).value == D(14000)
    assert worksheet.get(AUDITED).value == D(13970)


def test_the_forms_are_named_in_the_order_they_ran_the_default_form_among_them() -> None:
    result = form_set(audit(), shop()).compute(TWO_SHOPS, TWO_AUDITS)

    assert list(result) == ["ex/shop", "ex/audit", RETURN]


def test_the_result_is_a_plain_mapping_of_tuples_of_worksheets() -> None:
    result = form_set(shop(), audit()).compute(TWO_SHOPS, TWO_AUDITS)

    assert type(result) is dict
    assert all(type(found) is tuple for found in result.values())
    assert [len(found) for found in result.values()] == [2, 2, 1]


def test_a_form_the_set_does_not_hold_is_not_found() -> None:
    forms = form_set(shop(), audit())

    assert forms.form("ex/shop").name == "ex/shop"
    with pytest.raises(NotFoundError, match="ex/nowhere"):
        forms.form("ex/nowhere")


def instance_lines(lines: tuple[TraceLine, ...]) -> list[FormInstanceLine]:
    return [line for line in lines if isinstance(line, FormInstanceLine)]


# --- the trace: one line per worksheet, in run order ------------------------------------------


def test_the_trace_has_one_line_per_worksheet_in_run_order_the_default_form_among_them() -> None:
    forms = form_set(audit(), shop())
    result = forms.compute(TWO_SHOPS, TWO_AUDITS)

    lines = forms.trace(result)

    assert all(isinstance(line, FormInstanceLine) for line in lines)
    assert [(line.form, line.position) for line in instance_lines(lines)] == [
        ("ex/shop", 1),
        ("ex/shop", 2),
        ("ex/audit", 1),
        ("ex/audit", 2),
        (RETURN, 1),
    ]
    last = lines[-1]
    assert isinstance(last, FormInstanceLine)
    assert last.lines == result[RETURN][0].trace
    assert [type(line) for line in last.lines] == [RecordTotalLine]


def test_an_instances_line_holds_the_trace_of_that_instances_own_worksheet() -> None:
    forms = form_set(shop(), audit())
    result = forms.compute(TWO_SHOPS, TWO_AUDITS)

    first = forms.trace(result)[0]

    assert isinstance(first, FormInstanceLine)
    assert first.lines == result["ex/shop"][0].trace
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


def test_a_failure_of_a_form_without_instances_names_the_form_and_instance_1() -> None:
    boom = flat(
        [Subtract(SALES, COSTS, PROFIT)],
        inputs=frozenset({SALES, COSTS}),
        outputs=frozenset({PROFIT}),
    )

    with pytest.raises(CapabilityContractError) as caught:
        boom.compute(Artifact(SALES, D(1)), Artifact(COSTS, D(2)))

    assert str(caught.value).startswith(f"{RETURN}, instance 1: ")


def once_form() -> FormComposition:
    return FormComposition(
        "ex/once",
        [Subtract(SALES, COSTS, PROFIT)],
        exports=[PROFIT],
        starting=frozenset({SALES, COSTS}),
    )


def test_a_run_error_in_a_form_without_an_instances_list_names_it_and_instance_1() -> None:
    forms = FormSet([once_form()], inputs=frozenset({SALES, COSTS}))

    with pytest.raises(CapabilityContractError, match=r"^ex/once, instance 1: ") as caught:
        forms.compute(Artifact(SALES, D(1)), Artifact(COSTS, D(2)))  # a loss: PROFIT is >= 0

    assert "profit" in str(caught.value)


def test_a_wiring_error_in_a_form_without_an_instances_list_names_the_form_only() -> None:
    with pytest.raises(InvalidCompositionError, match=r"^form 'ex/once': ") as caught:
        FormComposition(
            "ex/once",
            [Subtract(SALES, COSTS, PROFIT)],
            exports=[PROFIT],
            starting=frozenset({SALES}),
        )

    assert "instance" not in str(caught.value)


def test_the_trace_of_a_form_without_an_instances_list_has_one_line_at_position_1() -> None:
    forms = FormSet([once_form()], inputs=frozenset({SALES, COSTS}))
    result = forms.compute(Artifact(SALES, D(5)), Artifact(COSTS, D(2)))

    (line,) = forms.trace(result)

    assert isinstance(line, FormInstanceLine)
    assert (line.form, line.position) == ("ex/once", 1)
    assert line.lines == result["ex/once"][0].trace


# --- a set of one form without instances behaves as the bare composition -----------------------


def lone_set() -> FormSet:
    return flat(
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


def test_a_set_of_one_form_without_instances_computes_what_the_composition_does() -> None:
    given = (Artifact(SALES, D(10)), Artifact(COSTS, D(4)))

    result = lone_set().compute(*given)

    assert result[RETURN][0].get(LEVY) == lone_composition().compute(*given).get(LEVY)
    assert result[RETURN][0].trace == lone_composition().compute(*given).trace
    assert list(result) == [RETURN]


def test_its_starting_kind_errors_are_the_compositions() -> None:
    for arguments in ((), (Artifact(SALES, D(1)),), (Artifact(FEE, D(1)),)):
        with pytest.raises(InvalidCompositionError) as bare:
            lone_composition().compute(*arguments)
        with pytest.raises(InvalidCompositionError) as wrapped:
            lone_set().compute(*arguments)
        assert str(wrapped.value) == str(bare.value)


def test_its_wiring_errors_are_those_of_the_composition_prefixed_with_the_form() -> None:
    with pytest.raises(InvalidCompositionError) as bare:
        Composition(
            [Subtract(SALES, COSTS, LEVY)], inputs=frozenset({SALES}), outputs=frozenset({LEVY})
        )
    with pytest.raises(InvalidCompositionError) as wrapped:
        flat(
            [Subtract(SALES, COSTS, LEVY)],
            inputs=frozenset({SALES}),
            outputs=frozenset({LEVY}),
        )

    assert str(wrapped.value) == f"form {RETURN!r}: {bare.value}"


def test_that_forms_composition_is_the_one_the_bare_wiring_would_give() -> None:
    assert [type(c) for c in lone_set().form(RETURN).composition.order] == [Subtract]


# --- two starting values of one kind -----------------------------------------------------------


def test_two_starting_values_for_a_return_input_are_refused_as_the_worksheet_does() -> None:
    twice = (Artifact(SALES, D(10)), Artifact(SALES, D(11)), Artifact(COSTS, D(4)))

    with pytest.raises(DuplicateArtifactError, match="two starting values for 'sales'") as bare:
        lone_composition().compute(*twice)
    with pytest.raises(DuplicateArtifactError) as wrapped:
        lone_set().compute(*twice)

    assert str(wrapped.value) == str(bare.value)


def test_two_starting_values_for_a_forms_instances_are_refused() -> None:
    with pytest.raises(DuplicateArtifactError, match="two starting values for 'shops'"):
        form_set(shop(), audit()).compute(TWO_SHOPS, shops(("1", "1")), TWO_AUDITS)


def test_two_starting_values_are_refused_even_when_the_kind_is_not_an_input() -> None:
    with pytest.raises(DuplicateArtifactError, match="two starting values for 'fee'"):
        form_set(shop(), audit()).compute(
            TWO_SHOPS, TWO_AUDITS, Artifact(FEE, D(1)), Artifact(FEE, D(2))
        )
