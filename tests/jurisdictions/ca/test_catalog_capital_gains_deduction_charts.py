"""Registered and money kinds of the federal catalog family `capital_gains_deduction_charts`.

Form T657 Chart 2024, Period 1 and Period 2 (confirmed 2026-10-19 from the PDF; the form lines are
in `tests/jurisdictions/ca_on/test_t657_2025.py`).
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    CHART_2024_PERIOD_1_AMOUNT_A,
    CHART_2024_PERIOD_1_AMOUNT_C,
    CHART_2024_PERIOD_1_AMOUNT_E,
    CHART_2024_PERIOD_1_AMOUNT_I,
    CHART_2024_PERIOD_1_AMOUNT_K,
    CHART_2024_PERIOD_1_AMOUNT_L,
    CHART_2024_PERIOD_1_AMOUNT_N,
    CHART_2024_PERIOD_1_AMOUNT_O,
    CHART_2024_PERIOD_1_AMOUNTS_F_TO_H,
    CHART_2024_PERIOD_2_AMOUNT_A,
    CHART_2024_PERIOD_2_AMOUNT_C,
    CHART_2024_PERIOD_2_AMOUNT_E,
    CHART_2024_PERIOD_2_AMOUNT_I,
    CHART_2024_PERIOD_2_AMOUNT_K,
    CHART_2024_PERIOD_2_AMOUNT_L,
    CHART_2024_PERIOD_2_AMOUNT_N,
    CHART_2024_PERIOD_2_AMOUNT_O,
    CHART_2024_PERIOD_2_AMOUNTS_F_TO_H,
    T657_CHART_2024_PERIOD_1_AMOUNT_B,
    T657_CHART_2024_PERIOD_1_AMOUNT_F,
    T657_CHART_2024_PERIOD_1_AMOUNT_G,
    T657_CHART_2024_PERIOD_1_AMOUNT_H,
    T657_CHART_2024_PERIOD_1_AMOUNT_J,
    T657_CHART_2024_PERIOD_2_AMOUNT_F,
    T657_CHART_2024_PERIOD_2_AMOUNT_G,
    T657_CHART_2024_PERIOD_2_AMOUNT_H,
    T657_CHART_2024_PERIOD_2_AMOUNT_J,
)


def test_the_form_t657_chart_2024_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    # Form T657 Chart 2024, Period 1 and Period 2: the starting amounts (B for Period 1, F, G, H and
    # J of each period) and the computed amounts A to O of each period.
    for identifier, kind in (
        ("ca/t657_chart_2024_period_1_amount_b", T657_CHART_2024_PERIOD_1_AMOUNT_B),
        ("ca/t657_chart_2024_period_1_amount_f", T657_CHART_2024_PERIOD_1_AMOUNT_F),
        ("ca/t657_chart_2024_period_1_amount_g", T657_CHART_2024_PERIOD_1_AMOUNT_G),
        ("ca/t657_chart_2024_period_1_amount_h", T657_CHART_2024_PERIOD_1_AMOUNT_H),
        ("ca/t657_chart_2024_period_1_amount_j", T657_CHART_2024_PERIOD_1_AMOUNT_J),
        ("ca/t657_chart_2024_period_2_amount_f", T657_CHART_2024_PERIOD_2_AMOUNT_F),
        ("ca/t657_chart_2024_period_2_amount_g", T657_CHART_2024_PERIOD_2_AMOUNT_G),
        ("ca/t657_chart_2024_period_2_amount_h", T657_CHART_2024_PERIOD_2_AMOUNT_H),
        ("ca/t657_chart_2024_period_2_amount_j", T657_CHART_2024_PERIOD_2_AMOUNT_J),
        ("ca/chart_2024_period_1_amount_a", CHART_2024_PERIOD_1_AMOUNT_A),
        ("ca/chart_2024_period_1_amount_c", CHART_2024_PERIOD_1_AMOUNT_C),
        ("ca/chart_2024_period_1_amount_e", CHART_2024_PERIOD_1_AMOUNT_E),
        ("ca/chart_2024_period_1_amounts_f_to_h", CHART_2024_PERIOD_1_AMOUNTS_F_TO_H),
        ("ca/chart_2024_period_1_amount_i", CHART_2024_PERIOD_1_AMOUNT_I),
        ("ca/chart_2024_period_1_amount_k", CHART_2024_PERIOD_1_AMOUNT_K),
        ("ca/chart_2024_period_1_amount_l", CHART_2024_PERIOD_1_AMOUNT_L),
        ("ca/chart_2024_period_1_amount_n", CHART_2024_PERIOD_1_AMOUNT_N),
        ("ca/chart_2024_period_1_amount_o", CHART_2024_PERIOD_1_AMOUNT_O),
        ("ca/chart_2024_period_2_amount_a", CHART_2024_PERIOD_2_AMOUNT_A),
        ("ca/chart_2024_period_2_amount_c", CHART_2024_PERIOD_2_AMOUNT_C),
        ("ca/chart_2024_period_2_amount_e", CHART_2024_PERIOD_2_AMOUNT_E),
        ("ca/chart_2024_period_2_amounts_f_to_h", CHART_2024_PERIOD_2_AMOUNTS_F_TO_H),
        ("ca/chart_2024_period_2_amount_i", CHART_2024_PERIOD_2_AMOUNT_I),
        ("ca/chart_2024_period_2_amount_k", CHART_2024_PERIOD_2_AMOUNT_K),
        ("ca/chart_2024_period_2_amount_l", CHART_2024_PERIOD_2_AMOUNT_L),
        ("ca/chart_2024_period_2_amount_n", CHART_2024_PERIOD_2_AMOUNT_N),
        ("ca/chart_2024_period_2_amount_o", CHART_2024_PERIOD_2_AMOUNT_O),
    ):
        assert registry.get(identifier) is kind, identifier


def test_the_form_t657_chart_2024_amounts_are_money_non_negative_except_the_signed_lines() -> None:
    # Amounts F and G (T2017 lines 6 and 12) are signed, as the ticket's design sets; every other
    # starting amount and every computed amount is non-negative.
    signed = (
        T657_CHART_2024_PERIOD_1_AMOUNT_F,
        T657_CHART_2024_PERIOD_1_AMOUNT_G,
        T657_CHART_2024_PERIOD_2_AMOUNT_F,
        T657_CHART_2024_PERIOD_2_AMOUNT_G,
    )
    for kind in signed:
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is False, kind.identifier
    for kind in (
        T657_CHART_2024_PERIOD_1_AMOUNT_B,
        T657_CHART_2024_PERIOD_1_AMOUNT_H,
        T657_CHART_2024_PERIOD_1_AMOUNT_J,
        T657_CHART_2024_PERIOD_2_AMOUNT_H,
        T657_CHART_2024_PERIOD_2_AMOUNT_J,
        CHART_2024_PERIOD_1_AMOUNT_A,
        CHART_2024_PERIOD_1_AMOUNT_C,
        CHART_2024_PERIOD_1_AMOUNT_E,
        CHART_2024_PERIOD_1_AMOUNTS_F_TO_H,
        CHART_2024_PERIOD_1_AMOUNT_I,
        CHART_2024_PERIOD_1_AMOUNT_K,
        CHART_2024_PERIOD_1_AMOUNT_L,
        CHART_2024_PERIOD_1_AMOUNT_N,
        CHART_2024_PERIOD_1_AMOUNT_O,
        CHART_2024_PERIOD_2_AMOUNT_A,
        CHART_2024_PERIOD_2_AMOUNT_C,
        CHART_2024_PERIOD_2_AMOUNT_E,
        CHART_2024_PERIOD_2_AMOUNTS_F_TO_H,
        CHART_2024_PERIOD_2_AMOUNT_I,
        CHART_2024_PERIOD_2_AMOUNT_K,
        CHART_2024_PERIOD_2_AMOUNT_L,
        CHART_2024_PERIOD_2_AMOUNT_N,
        CHART_2024_PERIOD_2_AMOUNT_O,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
