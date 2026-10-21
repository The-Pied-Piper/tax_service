"""The federal catalog: Form T657 Chart 2024, Period 1 and Period 2.

The starting amounts of each period (B for Period 1, F, G, H and J of each period) and the computed
amounts A to O of each period. Period 2's amount B is Period 1's amount N, so it is not declared.
"""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

T657_CHART_2024_PERIOD_1_AMOUNT_B = CATALOG.declare(
    "t657_chart_2024_period_1_amount_b", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount B, Form T657 Chart 2024 Period 1 "Enter the last amount that you
calculated for "Total amount of capital gains included in 2025 income eligible for the capital gains
deduction" from 2016 to 2023": a starting amount, 0 when no chart for 2016 to 2023 is completed."""

T657_CHART_2024_PERIOD_1_AMOUNT_F = CATALOG.declare("t657_chart_2024_period_1_amount_f", Decimal)
"""Chart 2024 Period 1 amount F, Form T657 Chart 2024 Period 1 "Add amounts F to H (if negative,
enter "0")": "Amount from line 6 of Form T2017 (do not include reserves from dispositions of QFFP in
any year or period other than Period 1 of 2024)", a starting amount, a loss in brackets."""

T657_CHART_2024_PERIOD_1_AMOUNT_G = CATALOG.declare("t657_chart_2024_period_1_amount_g", Decimal)
"""Chart 2024 Period 1 amount G, Form T657 Chart 2024 Period 1 "Add amounts F to H (if negative,
enter "0")": "Amount from line 12 of Form T2017 (do not include reserves from dispositions of QSBCS
in any year or period other than Period 1 of 2024)", a starting amount, a loss in brackets."""

T657_CHART_2024_PERIOD_1_AMOUNT_H = CATALOG.declare(
    "t657_chart_2024_period_1_amount_h", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount H, Form T657 Chart 2024 Period 1 "Add amounts F to H (if negative,
enter "0")": "Amount included in box 30 of a 2025 T3 slip and the footnote area indicates it is a
reserve from property disposed of in Period 1 of 2024", a starting amount."""

T657_CHART_2024_PERIOD_1_AMOUNT_J = CATALOG.declare(
    "t657_chart_2024_period_1_amount_j", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount J, Form T657 Chart 2024 Period 1 "Amount I minus amount J":
"Portion of the amount from line 17216 of Form T2048 in respect of a reserve for a property disposed
of in Period 1 of 2024", a starting amount."""

T657_CHART_2024_PERIOD_2_AMOUNT_F = CATALOG.declare("t657_chart_2024_period_2_amount_f", Decimal)
"""Chart 2024 Period 2 amount F, Form T657 Chart 2024 Period 2 "Add amounts F to H (if negative,
enter "0")": "Amount from line 6 of Form T2017 (do not include reserves from dispositions of QFFP in
any year or period other than Period 2 of 2024)", a starting amount, a loss in brackets."""

T657_CHART_2024_PERIOD_2_AMOUNT_G = CATALOG.declare("t657_chart_2024_period_2_amount_g", Decimal)
"""Chart 2024 Period 2 amount G, Form T657 Chart 2024 Period 2 "Add amounts F to H (if negative,
enter "0")": "Amount from line 12 of Form T2017 (do not include reserves from dispositions of QSBCS
in any year or period other than Period 2 of 2024)", a starting amount, a loss in brackets."""

T657_CHART_2024_PERIOD_2_AMOUNT_H = CATALOG.declare(
    "t657_chart_2024_period_2_amount_h", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount H, Form T657 Chart 2024 Period 2 "Add amounts F to H (if negative,
enter "0")": "Amount included in box 30 of a 2025 T3 slip and the footnote area indicates it is a
reserve from property disposed of in Period 2 of 2024", a starting amount."""

T657_CHART_2024_PERIOD_2_AMOUNT_J = CATALOG.declare(
    "t657_chart_2024_period_2_amount_j", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount J, Form T657 Chart 2024 Period 2 "Amount I minus amount J":
"Portion of the amount from line 17216 of Form T2048 in respect of a reserve for a property disposed
of in Period 2 of 2024", a starting amount."""

CHART_2024_PERIOD_1_AMOUNT_A = CATALOG.declare(
    "chart_2024_period_1_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS disposed of in 2024 for Period 1, Form T657
Chart 2024 Period 1 amount A: 508,418.00, a dataset."""

CHART_2024_PERIOD_1_AMOUNT_C = CATALOG.declare(
    "chart_2024_period_1_amount_c", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount C, Form T657 Chart 2024 Period 1 "Amount A minus amount B": amount A
minus amount B, floored at 0 (the form prints no floor)."""

CHART_2024_PERIOD_1_AMOUNT_E = CATALOG.declare(
    "chart_2024_period_1_amount_e", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount E, Form T657 Chart 2024 Period 1 "Capital gains deduction available
for dispositions of QFFP and/or QSBCS: amount C minus amount D (if negative, enter "0")": amount C
minus amount D, not below 0."""

CHART_2024_PERIOD_1_AMOUNTS_F_TO_H = CATALOG.declare(
    "chart_2024_period_1_amounts_f_to_h", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amounts F to H, Form T657 Chart 2024 Period 1 "Add amounts F to H (if
negative, enter "0")": the sum of amounts F to H, not below 0."""

CHART_2024_PERIOD_1_AMOUNT_I = CATALOG.declare(
    "chart_2024_period_1_amount_i", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount I, Form T657 Chart 2024 Period 1 "= × 1/2 = I": amounts F to H
multiplied by 1/2, rounded half-up to the cent."""

CHART_2024_PERIOD_1_AMOUNT_K = CATALOG.declare(
    "chart_2024_period_1_amount_k", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount K, Form T657 Chart 2024 Period 1 "Amount I minus amount J": amount I
minus amount J, floored at 0 (the form prints no floor)."""

CHART_2024_PERIOD_1_AMOUNT_L = CATALOG.declare(
    "chart_2024_period_1_amount_l", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount L, Form T657 Chart 2024 Period 1 "Enter whichever is less: amount E or
amount K.": the lesser of amount E and amount K."""

CHART_2024_PERIOD_1_AMOUNT_N = CATALOG.declare(
    "chart_2024_period_1_amount_n", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount N, Form T657 Chart 2024 Period 1 "Amount L plus amount M": amount L
plus amount B, where M is amount B. The total carried into Period 2 and into Chart 2025."""

CHART_2024_PERIOD_1_AMOUNT_O = CATALOG.declare(
    "chart_2024_period_1_amount_o", Decimal, non_negative=True
)
"""Chart 2024 Period 1 amount O, Form T657 Chart 2024 Period 1 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount N above.": the lesser of the annual gains limit, the cumulative
gains limit and amount N."""

CHART_2024_PERIOD_2_AMOUNT_A = CATALOG.declare(
    "chart_2024_period_2_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS disposed of in 2024 for Period 2, Form T657
Chart 2024 Period 2 amount A: 625,000.00, a dataset."""

CHART_2024_PERIOD_2_AMOUNT_C = CATALOG.declare(
    "chart_2024_period_2_amount_c", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount C, Form T657 Chart 2024 Period 2 "Amount A minus amount B": amount A
minus amount B, where B is Period 1's amount N, floored at 0 (the form prints no floor)."""

CHART_2024_PERIOD_2_AMOUNT_E = CATALOG.declare(
    "chart_2024_period_2_amount_e", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount E, Form T657 Chart 2024 Period 2 "Capital gains deduction available
for dispositions of QFFP and/or QSBCS: amount C minus amount D (if negative, enter "0")": amount C
minus amount D, not below 0."""

CHART_2024_PERIOD_2_AMOUNTS_F_TO_H = CATALOG.declare(
    "chart_2024_period_2_amounts_f_to_h", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amounts F to H, Form T657 Chart 2024 Period 2 "Add amounts F to H (if
negative, enter "0")": the sum of amounts F to H, not below 0."""

CHART_2024_PERIOD_2_AMOUNT_I = CATALOG.declare(
    "chart_2024_period_2_amount_i", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount I, Form T657 Chart 2024 Period 2 "= × 1/2 = I": amounts F to H
multiplied by 1/2, rounded half-up to the cent."""

CHART_2024_PERIOD_2_AMOUNT_K = CATALOG.declare(
    "chart_2024_period_2_amount_k", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount K, Form T657 Chart 2024 Period 2 "Amount I minus amount J": amount I
minus amount J, floored at 0 (the form prints no floor)."""

CHART_2024_PERIOD_2_AMOUNT_L = CATALOG.declare(
    "chart_2024_period_2_amount_l", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount L, Form T657 Chart 2024 Period 2 "Enter whichever is less: amount E or
amount K.": the lesser of amount E and amount K."""

CHART_2024_PERIOD_2_AMOUNT_N = CATALOG.declare(
    "chart_2024_period_2_amount_n", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount N, Form T657 Chart 2024 Period 2 "Amount L plus amount M": amount L
plus amount B, where M is Period 1's amount N. The total carried into Chart 2025 Part 1 amount B."""

CHART_2024_PERIOD_2_AMOUNT_O = CATALOG.declare(
    "chart_2024_period_2_amount_o", Decimal, non_negative=True
)
"""Chart 2024 Period 2 amount O, Form T657 Chart 2024 Period 2 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2, or amount N above.": the lesser of the annual gains limit, the cumulative
gains limit and amount N."""
