"""The composition root's explicit list of jurisdiction packages and the data roots it yields.

Checked generically, so a package added under `app/jurisdictions/` but not registered fails here.
Catalogs register only when `JURISDICTIONS.register()` is called; importing registers no kind.
"""

from __future__ import annotations

import importlib
import inspect
import subprocess
import sys
from pathlib import Path

import pytest

import app
import app.adapters.inbound.trace_english
import app.adapters.outbound.parameter_parsers
import app.domain.capabilities
import app.jurisdictions
import app.registrations
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages
from app.domain.artifact import ArtifactCatalog, ArtifactRegistry
from app.domain.capability import CapabilityRegistry
from app.domain.errors import UnknownRegistrationError

JURISDICTIONS_DIRECTORY = Path(app.jurisdictions.__file__).parent


def test_lists_the_jurisdiction_packages() -> None:
    assert isinstance(app.registrations.JURISDICTIONS, JurisdictionPackages)


def test_every_jurisdiction_package_is_registered() -> None:
    packages = {init.parent for init in JURISDICTIONS_DIRECTORY.glob("*/__init__.py")}

    assert packages
    assert packages <= set(app.registrations.JURISDICTIONS.roots().values())


def test_each_root_is_the_directory_of_the_package_declaring_its_namespace() -> None:
    for namespace, directory in app.registrations.JURISDICTIONS.roots().items():
        package = importlib.import_module(f"app.jurisdictions.{directory.name}")

        assert Path(package.__file__ or "").parent == directory
        assert package.NAMESPACE == namespace.name


def test_lists_the_core_packages() -> None:
    assert app.registrations.CORE_PACKAGES == (
        app.domain.capabilities,
        app.adapters.outbound.parameter_parsers,
        app.adapters.inbound.trace_english,
    )


def test_importing_a_jurisdiction_package_registers_its_capabilities() -> None:
    registry = CapabilityRegistry.shared()

    for name in (
        "caregiver_amount",
        "choose_by_range",
        "disability_transfer_amount",
        "flow_through_share_expenses",
        "provincial_foreign_tax_credit",
    ):
        registered = registry.get(f"ca-on/{name}")
        assert registered.__module__ == f"app.jurisdictions.ca_on.capabilities.{name}"


def test_importing_the_federal_package_registers_its_capabilities() -> None:
    registered = CapabilityRegistry.shared().get("ca/caregiver_amount")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.caregiver_amount"


def test_importing_the_federal_package_registers_the_other_dependants_medical_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/other_dependants_medical")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.other_dependants_medical"


def test_importing_the_federal_package_registers_the_apprenticeship_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/apprenticeship_wages_total")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.apprenticeship_wages_total"


def test_importing_the_federal_package_registers_the_threshold_gate_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/threshold_gate")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.threshold_gate"


def test_importing_the_federal_package_registers_the_principal_residence_gain() -> None:
    registered = CapabilityRegistry.shared().get("ca/principal_residence_gain")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.principal_residence_gain"


@pytest.mark.parametrize("line", [27, 29, 30, 32, 33, 38, 39, 42, 44, 45, 48, 51, 53])
def test_importing_the_federal_package_registers_the_principal_residence_part_2_lines(
    line: int,
) -> None:
    registered = CapabilityRegistry.shared().get(f"ca/principal_residence_line_{line}")

    assert registered.__module__ == (
        f"app.jurisdictions.ca.capabilities.principal_residence_line_{line}"
    )


def test_the_principal_residence_rows_base_is_not_registered() -> None:
    # The base is a class of its own, imported here, and is never registered under any name.
    from app.jurisdictions.ca.capabilities.principal_residence_rows import PrincipalResidenceRows

    assert PrincipalResidenceRows.__name__ == "PrincipalResidenceRows"
    with pytest.raises(UnknownRegistrationError):
        CapabilityRegistry.shared().get("ca/principal_residence_rows")


@pytest.mark.parametrize(
    "line",
    [3, 6, 16, 17, 18, 19, 21, 23, 24, 26, 27, 30, 32, 33, 35, 36, 40, 41, 44, 46, 47]
    + [50, 53, 55, 58, 59, 61, 63, 64, 66],
)
def test_importing_the_federal_package_registers_the_worksheet_lines(line: int) -> None:
    registered = CapabilityRegistry.shared().get(f"ca/principal_residence_worksheet_line_{line}")

    assert registered.__module__ == (
        f"app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_{line}"
    )


@pytest.mark.parametrize("line", [56, 57])
def test_importing_the_federal_package_registers_the_part_4_lines(line: int) -> None:
    registered = CapabilityRegistry.shared().get(f"ca/principal_residence_line_{line}")

    assert registered.__module__ == (
        f"app.jurisdictions.ca.capabilities.principal_residence_line_{line}"
    )


def test_the_worksheet_base_is_not_registered() -> None:
    # The base is a class of its own, imported here, and is never registered under any name.
    from app.jurisdictions.ca.capabilities.principal_residence_worksheet_rows import (
        PrincipalResidenceWorksheetRows,
    )

    assert PrincipalResidenceWorksheetRows.__name__ == "PrincipalResidenceWorksheetRows"
    with pytest.raises(UnknownRegistrationError):
        CapabilityRegistry.shared().get("ca/principal_residence_worksheet_rows")


def test_importing_the_federal_package_registers_the_disposition_gains_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/disposition_gains")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.disposition_gains"


def test_importing_the_federal_package_registers_the_disposition_gains_only_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/disposition_gains_only")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.disposition_gains_only"


def test_importing_the_federal_package_registers_the_disposition_proceeds_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/disposition_proceeds")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.disposition_proceeds"


def test_importing_the_federal_package_registers_the_ei_excluded_slips_net_income_capability() -> (
    None
):
    registered = CapabilityRegistry.shared().get("ca/ei_excluded_slips_net_income")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.ei_excluded_slips_net_income"


def test_importing_the_federal_package_registers_the_cca_claim_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/cca_claim")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.cca_claim"


def test_importing_the_federal_package_registers_the_cca_claim_after_column_22_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/cca_claim_after_column_22")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.cca_claim_after_column_22"


def test_importing_the_federal_package_registers_the_cca_claim_prorated_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/cca_claim_prorated")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.cca_claim_prorated"


def test_importing_the_federal_package_registers_the_cca_claim_after_22_prorated_capability() -> (
    None
):
    registered = CapabilityRegistry.shared().get("ca/cca_claim_after_column_22_prorated")

    assert (
        registered.__module__
        == "app.jurisdictions.ca.capabilities.cca_claim_after_column_22_prorated"
    )


def test_importing_the_federal_package_registers_the_recaptured_cca_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/recaptured_cca")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.recaptured_cca"


def test_importing_the_federal_package_registers_the_immediate_expensing_claim_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/immediate_expensing_claim")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.immediate_expensing_claim"


def test_importing_the_federal_package_registers_the_business_vehicle_expenses_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/business_vehicle_expenses")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.business_vehicle_expenses"


def test_importing_the_federal_package_registers_the_terminal_loss_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/terminal_loss")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.terminal_loss"


def test_importing_the_federal_package_registers_the_closing_ucc_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/closing_ucc")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.closing_ucc"


def test_importing_the_federal_package_registers_the_closing_ucc_after_column_22_capability() -> (
    None
):
    registered = CapabilityRegistry.shared().get("ca/closing_ucc_after_column_22")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.closing_ucc_after_column_22"


def test_importing_the_federal_package_registers_the_closing_ucc_prorated_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/closing_ucc_prorated")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.closing_ucc_prorated"


def test_importing_the_federal_package_registers_the_closing_ucc_after_22_prorated_capability() -> (
    None
):
    registered = CapabilityRegistry.shared().get("ca/closing_ucc_after_column_22_prorated")

    assert (
        registered.__module__
        == "app.jurisdictions.ca.capabilities.closing_ucc_after_column_22_prorated"
    )


def test_importing_the_federal_package_registers_the_fiscal_period_days_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/fiscal_period_days")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.fiscal_period_days"


def test_importing_the_federal_package_registers_the_short_term_rental_expenses_capability() -> (
    None
):
    registered = CapabilityRegistry.shared().get("ca/short_term_rental_non_compliant_expenses")

    assert registered.__module__ == (
        "app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_expenses"
    )


def test_importing_the_federal_package_registers_the_short_term_rental_cca_capabilities() -> None:
    total = CapabilityRegistry.shared().get("ca/short_term_rental_non_compliant_cca")
    by_class = CapabilityRegistry.shared().get("ca/short_term_rental_non_compliant_cca_by_class")

    assert total.__module__ == (
        "app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca"
    )
    assert by_class.__module__ == (
        "app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca_by_class"
    )


def test_importing_the_federal_package_registers_the_short_term_rental_gross_rents() -> None:
    registered = CapabilityRegistry.shared().get("ca/short_term_rental_gross_rents")

    assert registered.__module__ == (
        "app.jurisdictions.ca.capabilities.short_term_rental_gross_rents"
    )


def test_importing_the_federal_package_registers_the_rental_gross_rents() -> None:
    registered = CapabilityRegistry.shared().get("ca/rental_gross_rents")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.rental_gross_rents"


def test_importing_the_federal_package_registers_the_amount_or_divided_by_rate_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/amount_or_divided_by_rate")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.amount_or_divided_by_rate"


def test_importing_the_federal_package_registers_the_divided_by_rate_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/divided_by_rate")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.divided_by_rate"


def test_importing_the_federal_package_registers_the_sign_chosen_difference_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/sign_chosen_difference")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.sign_chosen_difference"


def test_importing_the_federal_package_registers_the_lesser_of_with_maximum_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/lesser_of_with_maximum")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.lesser_of_with_maximum"


def test_importing_the_federal_package_registers_the_chart_a_row_c_total_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/chart_a_row_c_total")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.chart_a_row_c_total"


def test_importing_the_federal_package_registers_the_chart_b_zone_a_total_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/chart_b_zone_a_total")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.chart_b_zone_a_total"


def test_importing_the_federal_package_registers_the_chart_b_zone_b_total_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/chart_b_zone_b_total")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.chart_b_zone_b_total"


def test_importing_the_federal_package_registers_the_foreign_non_business_tax_credit() -> None:
    registered = CapabilityRegistry.shared().get("ca/foreign_non_business_tax_credit")

    assert registered.__module__ == (
        "app.jurisdictions.ca.capabilities.foreign_non_business_tax_credit"
    )


@pytest.mark.parametrize("line", [4, 5, 7, 8, 10, 11])
def test_importing_the_federal_package_registers_the_foreign_business_tax_credit_lines(
    line: int,
) -> None:
    registered = CapabilityRegistry.shared().get(f"ca/foreign_business_tax_credit_line_{line}")

    assert registered.__module__ == (
        f"app.jurisdictions.ca.capabilities.foreign_business_tax_credit_line_{line}"
    )


def test_the_foreign_business_tax_credit_base_is_not_registered() -> None:
    with pytest.raises(UnknownRegistrationError):
        CapabilityRegistry.shared().get("ca/foreign_business_tax_credit_rows")


def test_importing_the_federal_package_registers_the_disability_transfer_amount() -> None:
    registered = CapabilityRegistry.shared().get("ca/disability_transfer_amount")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.disability_transfer_amount"


def test_each_core_package_imports_every_module_in_its_directory() -> None:
    for package in app.registrations.CORE_PACKAGES:
        directory = Path(package.__file__ or "").parent
        modules = {path.stem for path in directory.glob("*.py")} - {"__init__"}

        assert modules, package.__name__
        assert modules <= set(package.__all__), package.__name__
        for name in modules:
            assert getattr(package, name) is sys.modules[f"{package.__name__}.{name}"], name


def test_has_no_side_effect_only_imports() -> None:
    source = inspect.getsource(app.registrations)

    assert "noqa" not in source


def test_every_listed_package_exposes_its_catalog() -> None:
    for directory in app.registrations.JURISDICTIONS.roots().values():
        catalog = importlib.import_module(f"app.jurisdictions.{directory.name}.catalog")

        assert isinstance(getattr(catalog, "CATALOG", None), ArtifactCatalog), catalog.__name__


def test_register_fills_a_fresh_registry_with_every_listed_catalog() -> None:
    registry = ArtifactRegistry()

    app.registrations.JURISDICTIONS.register(registry)

    expected = set()
    for directory in app.registrations.JURISDICTIONS.roots().values():
        catalog = importlib.import_module(f"app.jurisdictions.{directory.name}.catalog").CATALOG
        expected |= {kind.identifier for kind in catalog.kinds}
        for kind in catalog.kinds:
            assert registry.get(kind.identifier) is kind
    assert expected
    assert registry.identifiers() == expected


def test_registering_twice_is_idempotent() -> None:
    registry = ArtifactRegistry()
    app.registrations.JURISDICTIONS.register(registry)
    first = registry.identifiers()

    app.registrations.JURISDICTIONS.register(registry)

    assert registry.identifiers() == first


_IMPORT_EVERYTHING = """
import pkgutil, importlib
import app
import app.adapters.outbound.parameter_parsers
import app.domain.capabilities
import app.jurisdictions
import app.registrations
from app.domain.artifact import ArtifactRegistry
for info in pkgutil.walk_packages(app.jurisdictions.__path__, "app.jurisdictions."):
    importlib.import_module(info.name)
print(sorted(ArtifactRegistry.shared().identifiers()))
"""


def test_importing_the_packages_and_registrations_registers_no_artifact_kind() -> None:
    # A fresh interpreter, so modules this test session already imported are imported again.
    result = subprocess.run(
        [sys.executable, "-c", _IMPORT_EVERYTHING],
        cwd=Path(app.__file__).parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"


def test_importing_the_federal_package_registers_the_count_at_least_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/count_at_least")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.count_at_least"


def test_importing_the_federal_package_registers_the_qbt_before_qcc_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/qbt_before_qcc")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.qbt_before_qcc"


def test_importing_the_federal_package_registers_the_yes_or_no_count_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/yes_or_no_count")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.yes_or_no_count"


def test_importing_the_federal_package_registers_the_ratio_truncated_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/ratio_truncated")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.ratio_truncated"


def test_importing_the_federal_package_registers_the_ratio_truncated_at_most_one_capability() -> (
    None
):
    registered = CapabilityRegistry.shared().get("ca/ratio_truncated_at_most_one")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.ratio_truncated"


def test_importing_the_federal_package_registers_the_apply_chosen_rate_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/apply_chosen_rate")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.apply_chosen_rate"


def test_importing_the_federal_package_registers_the_choose_by_sign_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/choose_by_sign")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.choose_by_sign"


def test_importing_the_federal_package_registers_the_positive_part_of_negation_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/positive_part_of_negation")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.positive_part_of_negation"


def test_importing_the_federal_package_registers_the_lesser_of_when_positive_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/lesser_of_when_positive")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.lesser_of_when_positive"


def test_importing_the_federal_package_registers_the_in_brackets_lesser_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/lesser_of_when_positive_in_brackets")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.lesser_of_when_positive"


def test_importing_the_federal_package_registers_the_amount_when_more_capability() -> None:
    registered = CapabilityRegistry.shared().get("ca/amount_when_more")

    assert registered.__module__ == "app.jurisdictions.ca.capabilities.amount_when_more"
