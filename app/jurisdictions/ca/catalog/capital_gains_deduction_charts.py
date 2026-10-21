"""The federal catalog: Form T657 Charts 2021 to 2023 (Part 1 and Part 2) and Chart 2024,
Period 1 and Period 2.

The starting amounts of each chart (the signed Part 1 F and G, the box 30 amounts, the counts and
the 2021 amount B) and the computed amounts of each chart, with each chart's total carried forward.
The charts are chained in the form's year order: each chart's amount B is the total carried by the
chart before it, and Period 2's amount B is Period 1's amount N, so those are not declared."""

from __future__ import annotations

from decimal import Decimal

from app.jurisdictions.ca.catalog.base import CATALOG

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

T657_CHART_2021_AMOUNT_B = CATALOG.declare("t657_chart_2021_amount_b", Decimal, non_negative=True)
"""Chart 2021 amount B, Form T657 Chart 2021 Part 1 "Enter the last amount that you calculated for
"Total amount of capital gains included in 2025 income eligible for the capital gains deduction"
from 2016 to 2020. If you did not complete charts for 2016 to 2020, enter "0"": a starting
amount, 0 when no chart for 2016 to 2020 is completed."""

T657_CHART_2021_USES_D_INSTEAD = CATALOG.declare(
    "t657_chart_2021_uses_d_instead", int, non_negative=True
)
"""Chart 2021 uses the (2021-1) calculation, Form T657 Chart 2021 Part 1 "If you claimed a capital
gains deduction for other eligible capital gains from 2021 to 2024, complete the following
calculation instead:": 1 when the filer completes that calculation for amount D, 0 when amount D
is line 19 of Chart 2; a starting count."""

T657_CHART_2021_AMOUNT_D_INSTEAD = CATALOG.declare(
    "t657_chart_2021_amount_d_instead", Decimal, non_negative=True
)
"""Chart 2021 amount D from the (2021-1) calculation, Form T657 Chart 2021 Part 1 "Enter the result
at amount D above.": the result of that calculation, which the caller enters when uses_d_instead
is 1; a starting amount."""

T657_CHART_2021_AMOUNT_F = CATALOG.declare("t657_chart_2021_amount_f", Decimal)
"""Chart 2021 Part 1 amount F, Form T657 Chart 2021 Part 1 "Amount from line 6 of Form T2017 (do
not include reserves from dispositions of QFFP in any year other than 2021)": a starting amount,
a loss in brackets."""

T657_CHART_2021_AMOUNT_G = CATALOG.declare("t657_chart_2021_amount_g", Decimal)
"""Chart 2021 Part 1 amount G, Form T657 Chart 2021 Part 1 "Amount from line 12 of Form T2017 (do
not include reserves from dispositions of QSBCS in any year other than 2021)": a starting
amount, a loss in brackets."""

T657_CHART_2021_AMOUNT_I = CATALOG.declare("t657_chart_2021_amount_i", Decimal, non_negative=True)
"""Chart 2021 Part 1 amount I, Form T657 Chart 2021 Part 1 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the property was disposed of in 2021": a starting amount."""

T657_CHART_2021_PART_2_AMOUNT_G = CATALOG.declare("t657_chart_2021_part_2_amount_g", Decimal)
"""Chart 2021 Part 2 amount G, Form T657 Chart 2021 Part 2 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the QFFP was disposed of in 2021": a starting amount."""

T657_CHART_2021_CLAIMS_ADDITIONAL_DEDUCTION = CATALOG.declare(
    "t657_chart_2021_claims_additional_deduction", int, non_negative=True
)
"""Chart 2021 Part 2 gate, Form T657 Chart 2021 Part 1 "you want to claim the additional deduction,
complete Part 2": 1 when the filer wants the additional deduction, 0 when not; a starting count."""

CHART_2021_PART_1_AMOUNT_A = CATALOG.declare(
    "chart_2021_part_1_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS disposed of in 2021, Form T657 Chart 2021
Part 1 amount A: 446,109.00, a dataset."""

CHART_2021_PART_1_AMOUNT_C = CATALOG.declare(
    "chart_2021_part_1_amount_c", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount C, Form T657 Chart 2021 Part 1 "Amount A minus amount B": amount A
minus amount B, floored at 0 (the form prints no floor)."""

CHART_2021_AMOUNT_D = CATALOG.declare("chart_2021_amount_d", Decimal, non_negative=True)
"""Chart 2021 amount D, Form T657 Chart 2021 Part 1 "Capital gains deductions from previous years
from line 19 of Chart 2 (2021-1)": line 19 of Chart 2, or the (2021-1) calculation's result when
uses_d_instead is 1."""

CHART_2021_PART_1_AMOUNT_E = CATALOG.declare(
    "chart_2021_part_1_amount_e", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount E, Form T657 Chart 2021 Part 1 "Capital gains deduction available for
QFFP and/or QSBCS disposed of in 2021 and included in your 2025 income: amount C minus amount D
(if negative, enter "0")": amount C minus amount D, not below 0."""

CHART_2021_PART_1_AMOUNTS_F_AND_G = CATALOG.declare(
    "chart_2021_part_1_amounts_f_and_g", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amounts F and G, Form T657 Chart 2021 Part 1 "Taxable capital gains from a
reserve on QFFP and/or QSBCS disposed of in 2021 included in your 2025 income: amount F plus
amount G (if negative, enter "0")": the sum of amounts F and G, not below 0."""

CHART_2021_PART_1_AMOUNT_H = CATALOG.declare(
    "chart_2021_part_1_amount_h", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount H, Form T657 Chart 2021 Part 1 "amount F plus amount G (if negative,
enter "0") × 1/2 = H": amounts F and G times 1/2, rounded half-up to the cent."""

CHART_2021_PART_1_AMOUNT_I = CATALOG.declare(
    "chart_2021_part_1_amount_i", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount I, Form T657 Chart 2021 Part 1 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the property was disposed of in 2021 × 1/2 = +": the box 30
amount times 1/2, rounded half-up to the cent."""

CHART_2021_PART_1_AMOUNT_J = CATALOG.declare(
    "chart_2021_part_1_amount_j", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount J, Form T657 Chart 2021 Part 1 "Amount H plus amount I": amounts H and
I added."""

CHART_2021_PART_1_AMOUNT_K = CATALOG.declare(
    "chart_2021_part_1_amount_k", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount K, Form T657 Chart 2021 Part 1 "Enter whichever is less: amount E or
amount J.": the lesser of amount E and amount J."""

CHART_2021_PART_1_AMOUNT_M = CATALOG.declare(
    "chart_2021_part_1_amount_m", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount M, Form T657 Chart 2021 Part 1 "Amount K plus amount L" M (L "Enter
amount B from above."): amount K plus amount B. B is the starting amount from 2016 to 2020, 0
when no chart is completed."""

CHART_2021_PART_1_AMOUNT_N = CATALOG.declare(
    "chart_2021_part_1_amount_n", Decimal, non_negative=True
)
"""Chart 2021 Part 1 amount N, Form T657 Chart 2021 Part 1 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount M above.": the lesser of the annual gains limit, the
cumulative gains limit and amount M, the maximum for line 25400 if no later reserve is reported."""

CHART_2021_PART_2_AMOUNT_A = CATALOG.declare(
    "chart_2021_part_2_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP disposed of in 2021, Form T657 Chart 2021 Part 2 amount
A: 500,000.00, a dataset."""

CHART_2021_PART_2_AMOUNT_C = CATALOG.declare(
    "chart_2021_part_2_amount_c", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount C, Form T657 Chart 2021 Part 2 "Amount A minus amount B" (B "Enter
amount M from Part 1 of Chart 2021."): amount A minus Part 1's amount M, floored at 0 (the form
prints no floor)."""

CHART_2021_PART_2_AMOUNT_E = CATALOG.declare(
    "chart_2021_part_2_amount_e", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount E, Form T657 Chart 2021 Part 2 "Capital gains deduction available for
QFFP disposed of in ... amount C minus amount D (if negative, enter "0")": amount C minus amount
D, not below 0."""

CHART_2021_PART_2_AMOUNT_F = CATALOG.declare(
    "chart_2021_part_2_amount_f", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount F, Form T657 Chart 2021 Part 2 "Amount from line 6 of Form T2017 ... ×
1/2 = F": the Part 1 amount F from line 6 of Form T2017 times 1/2, rounded half-up to the cent;
signed as its input is, the form prints no floor."""

CHART_2021_PART_2_AMOUNT_G = CATALOG.declare(
    "chart_2021_part_2_amount_g", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount G, Form T657 Chart 2021 Part 2 "Amount included in box 30 of a 2025 T3
slip ... × 1/2 = G": the box 30 amount times 1/2, rounded half-up to the cent; signed as its
input is, the form prints no floor."""

CHART_2021_PART_2_AMOUNT_H = CATALOG.declare(
    "chart_2021_part_2_amount_h", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount H, Form T657 Chart 2021 Part 2 "Amount F plus amount G" H: amounts F
and G added, with no floor (the form prints none)."""

CHART_2021_PART_2_AMOUNT_I = CATALOG.declare(
    "chart_2021_part_2_amount_i", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount I, Form T657 Chart 2021 Part 2 "Enter whichever is less: amount E or
amount H." I: the lesser of amount E and amount H."""

CHART_2021_PART_2_AMOUNT_K = CATALOG.declare(
    "chart_2021_part_2_amount_k", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount K, Form T657 Chart 2021 Part 2 "Amount I plus amount J" K (J "Enter
amount B from above.", Part 1 amount M): amount I plus Part 1's amount M."""

CHART_2021_PART_2_AMOUNT_L = CATALOG.declare(
    "chart_2021_part_2_amount_l", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount L, Form T657 Chart 2021 Part 2 "Enter whichever is less: amount H or
amount K." L: the lesser of amount H and amount K."""

CHART_2021_PART_2_AMOUNT_M = CATALOG.declare(
    "chart_2021_part_2_amount_m", Decimal, non_negative=True
)
"""Chart 2021 Part 2 amount M, Form T657 Chart 2021 Part 2 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount L above." M: the lesser of the annual gains limit, the
cumulative gains limit and amount L, the maximum for line 25400 if no other disposition is
reported."""

CHART_2021_PART_2_APPLIES = CATALOG.declare("chart_2021_part_2_applies", int, non_negative=True)
"""Chart 2021 Part 2 gate, Form T657 Chart 2021 Part 2 conditions (a QFFP reserve, you want to
claim the additional deduction, and amount E of Part 1 is no more than the three amounts the
form names): 1 when Part 2 is completed, 0 when it is not."""

CHART_2021_TOTAL_CARRIED = CATALOG.declare("chart_2021_total_carried", Decimal, non_negative=True)
"""Chart 2021 total carried, Form T657 Chart 2021 "Enter the last amount that you calculated for
"Total amount of capital gains included in 2025 income eligible for the capital gains
deduction"" for the charts after it: Part 2's amount L when Part 2 is completed, else Part 1's
amount M."""

T657_CHART_2022_USES_D_INSTEAD = CATALOG.declare(
    "t657_chart_2022_uses_d_instead", int, non_negative=True
)
"""Chart 2022 uses the (2022-1) calculation, Form T657 Chart 2022 Part 1 "If you claimed a capital
gains deduction for other eligible capital gains from 2022 to 2024, complete the following
calculation instead:": 1 when the filer completes that calculation for amount D, 0 when amount D
is line 19 of Chart 2; a starting count."""

T657_CHART_2022_AMOUNT_D_INSTEAD = CATALOG.declare(
    "t657_chart_2022_amount_d_instead", Decimal, non_negative=True
)
"""Chart 2022 amount D from the (2022-1) calculation, Form T657 Chart 2022 Part 1 "Enter the result
at amount D above.": the result of that calculation, which the caller enters when uses_d_instead
is 1; a starting amount."""

T657_CHART_2022_AMOUNT_F = CATALOG.declare("t657_chart_2022_amount_f", Decimal)
"""Chart 2022 Part 1 amount F, Form T657 Chart 2022 Part 1 "Amount from line 6 of Form T2017 (do
not include reserves from dispositions of QFFP in any year other than 2022)": a starting amount,
a loss in brackets."""

T657_CHART_2022_AMOUNT_G = CATALOG.declare("t657_chart_2022_amount_g", Decimal)
"""Chart 2022 Part 1 amount G, Form T657 Chart 2022 Part 1 "Amount from line 12 of Form T2017 (do
not include reserves from dispositions of QSBCS in any year other than 2022)": a starting
amount, a loss in brackets."""

T657_CHART_2022_AMOUNT_I = CATALOG.declare("t657_chart_2022_amount_i", Decimal, non_negative=True)
"""Chart 2022 Part 1 amount I, Form T657 Chart 2022 Part 1 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the property was disposed of in 2022": a starting amount."""

T657_CHART_2022_PART_2_AMOUNT_G = CATALOG.declare("t657_chart_2022_part_2_amount_g", Decimal)
"""Chart 2022 Part 2 amount G, Form T657 Chart 2022 Part 2 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the QFFP was disposed of in 2022": a starting amount."""

T657_CHART_2022_CLAIMS_ADDITIONAL_DEDUCTION = CATALOG.declare(
    "t657_chart_2022_claims_additional_deduction", int, non_negative=True
)
"""Chart 2022 Part 2 gate, Form T657 Chart 2022 Part 1 "you want to claim the additional deduction,
complete Part 2": 1 when the filer wants the additional deduction, 0 when not; a starting count."""

CHART_2022_PART_1_AMOUNT_A = CATALOG.declare(
    "chart_2022_part_1_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS disposed of in 2022, Form T657 Chart 2022
Part 1 amount A: 456,815.00, a dataset."""

CHART_2022_PART_1_AMOUNT_C = CATALOG.declare(
    "chart_2022_part_1_amount_c", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount C, Form T657 Chart 2022 Part 1 "Amount A minus amount B": amount A
minus amount B, floored at 0 (the form prints no floor)."""

CHART_2022_AMOUNT_D = CATALOG.declare("chart_2022_amount_d", Decimal, non_negative=True)
"""Chart 2022 amount D, Form T657 Chart 2022 Part 1 "Capital gains deductions from previous years
from line 19 of Chart 2 (2022-1)": line 19 of Chart 2, or the (2022-1) calculation's result when
uses_d_instead is 1."""

CHART_2022_PART_1_AMOUNT_E = CATALOG.declare(
    "chart_2022_part_1_amount_e", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount E, Form T657 Chart 2022 Part 1 "Capital gains deduction available for
QFFP and/or QSBCS disposed of in 2022 and included in your 2025 income: amount C minus amount D
(if negative, enter "0")": amount C minus amount D, not below 0."""

CHART_2022_PART_1_AMOUNTS_F_AND_G = CATALOG.declare(
    "chart_2022_part_1_amounts_f_and_g", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amounts F and G, Form T657 Chart 2022 Part 1 "Taxable capital gains from a
reserve on QFFP and/or QSBCS disposed of in 2022 included in your 2025 income: amount F plus
amount G (if negative, enter "0")": the sum of amounts F and G, not below 0."""

CHART_2022_PART_1_AMOUNT_H = CATALOG.declare(
    "chart_2022_part_1_amount_h", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount H, Form T657 Chart 2022 Part 1 "amount F plus amount G (if negative,
enter "0") × 1/2 = H": amounts F and G times 1/2, rounded half-up to the cent."""

CHART_2022_PART_1_AMOUNT_I = CATALOG.declare(
    "chart_2022_part_1_amount_i", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount I, Form T657 Chart 2022 Part 1 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the property was disposed of in 2022 × 1/2 = +": the box 30
amount times 1/2, rounded half-up to the cent."""

CHART_2022_PART_1_AMOUNT_J = CATALOG.declare(
    "chart_2022_part_1_amount_j", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount J, Form T657 Chart 2022 Part 1 "Amount H plus amount I": amounts H and
I added."""

CHART_2022_PART_1_AMOUNT_K = CATALOG.declare(
    "chart_2022_part_1_amount_k", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount K, Form T657 Chart 2022 Part 1 "Enter whichever is less: amount E or
amount J.": the lesser of amount E and amount J."""

CHART_2022_PART_1_AMOUNT_M = CATALOG.declare(
    "chart_2022_part_1_amount_m", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount M, Form T657 Chart 2022 Part 1 "Amount K plus amount L" M (L "Enter
amount B from above."): amount K plus amount B. B is Chart 2021's total carried."""

CHART_2022_PART_1_AMOUNT_N = CATALOG.declare(
    "chart_2022_part_1_amount_n", Decimal, non_negative=True
)
"""Chart 2022 Part 1 amount N, Form T657 Chart 2022 Part 1 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount M above.": the lesser of the annual gains limit, the
cumulative gains limit and amount M, the maximum for line 25400 if no later reserve is reported."""

CHART_2022_PART_2_AMOUNT_A = CATALOG.declare(
    "chart_2022_part_2_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP disposed of in 2022, Form T657 Chart 2022 Part 2 amount
A: 500,000.00, a dataset."""

CHART_2022_PART_2_AMOUNT_C = CATALOG.declare(
    "chart_2022_part_2_amount_c", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount C, Form T657 Chart 2022 Part 2 "Amount A minus amount B" (B "Enter
amount M from Part 1 of Chart 2022."): amount A minus Part 1's amount M, floored at 0 (the form
prints no floor)."""

CHART_2022_PART_2_AMOUNT_E = CATALOG.declare(
    "chart_2022_part_2_amount_e", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount E, Form T657 Chart 2022 Part 2 "Capital gains deduction available for
QFFP disposed of in ... amount C minus amount D (if negative, enter "0")": amount C minus amount
D, not below 0."""

CHART_2022_PART_2_AMOUNT_F = CATALOG.declare(
    "chart_2022_part_2_amount_f", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount F, Form T657 Chart 2022 Part 2 "Amount from line 6 of Form T2017 ... ×
1/2 = F": the Part 1 amount F from line 6 of Form T2017 times 1/2, rounded half-up to the cent;
signed as its input is, the form prints no floor."""

CHART_2022_PART_2_AMOUNT_G = CATALOG.declare(
    "chart_2022_part_2_amount_g", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount G, Form T657 Chart 2022 Part 2 "Amount included in box 30 of a 2025 T3
slip ... × 1/2 = G": the box 30 amount times 1/2, rounded half-up to the cent; signed as its
input is, the form prints no floor."""

CHART_2022_PART_2_AMOUNT_H = CATALOG.declare(
    "chart_2022_part_2_amount_h", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount H, Form T657 Chart 2022 Part 2 "Amount F plus amount G" H: amounts F
and G added, with no floor (the form prints none)."""

CHART_2022_PART_2_AMOUNT_I = CATALOG.declare(
    "chart_2022_part_2_amount_i", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount I, Form T657 Chart 2022 Part 2 "Enter whichever is less: amount E or
amount H." I: the lesser of amount E and amount H."""

CHART_2022_PART_2_AMOUNT_K = CATALOG.declare(
    "chart_2022_part_2_amount_k", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount K, Form T657 Chart 2022 Part 2 "Amount I plus amount J" K (J "Enter
amount B from above.", Part 1 amount M): amount I plus Part 1's amount M."""

CHART_2022_PART_2_AMOUNT_L = CATALOG.declare(
    "chart_2022_part_2_amount_l", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount L, Form T657 Chart 2022 Part 2 "Enter whichever is less: amount H or
amount K." L: the lesser of amount H and amount K."""

CHART_2022_PART_2_AMOUNT_M = CATALOG.declare(
    "chart_2022_part_2_amount_m", Decimal, non_negative=True
)
"""Chart 2022 Part 2 amount M, Form T657 Chart 2022 Part 2 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount L above." M: the lesser of the annual gains limit, the
cumulative gains limit and amount L, the maximum for line 25400 if no other disposition is
reported."""

CHART_2022_PART_2_APPLIES = CATALOG.declare("chart_2022_part_2_applies", int, non_negative=True)
"""Chart 2022 Part 2 gate, Form T657 Chart 2022 Part 2 conditions (a QFFP reserve, you want to
claim the additional deduction, and amount E of Part 1 is no more than the three amounts the
form names): 1 when Part 2 is completed, 0 when it is not."""

CHART_2022_TOTAL_CARRIED = CATALOG.declare("chart_2022_total_carried", Decimal, non_negative=True)
"""Chart 2022 total carried, Form T657 Chart 2022 "Enter the last amount that you calculated for
"Total amount of capital gains included in 2025 income eligible for the capital gains
deduction"" for the charts after it: Part 2's amount L when Part 2 is completed, else Part 1's
amount M."""

T657_CHART_2023_USES_D_INSTEAD = CATALOG.declare(
    "t657_chart_2023_uses_d_instead", int, non_negative=True
)
"""Chart 2023 uses the (2023-1) calculation, Form T657 Chart 2023 Part 1 "If you claimed a capital
gains deduction for other eligible capital gains from 2023 to 2024, complete the following
calculation instead:": 1 when the filer completes that calculation for amount D, 0 when amount D
is line 19 of Chart 2; a starting count."""

T657_CHART_2023_AMOUNT_D_INSTEAD = CATALOG.declare(
    "t657_chart_2023_amount_d_instead", Decimal, non_negative=True
)
"""Chart 2023 amount D from the (2023-1) calculation, Form T657 Chart 2023 Part 1 "Enter the result
at amount D above.": the result of that calculation, which the caller enters when uses_d_instead
is 1; a starting amount."""

T657_CHART_2023_AMOUNT_F = CATALOG.declare("t657_chart_2023_amount_f", Decimal)
"""Chart 2023 Part 1 amount F, Form T657 Chart 2023 Part 1 "Amount from line 6 of Form T2017 (do
not include reserves from dispositions of QFFP in any year other than 2023)": a starting amount,
a loss in brackets."""

T657_CHART_2023_AMOUNT_G = CATALOG.declare("t657_chart_2023_amount_g", Decimal)
"""Chart 2023 Part 1 amount G, Form T657 Chart 2023 Part 1 "Amount from line 12 of Form T2017 (do
not include reserves from dispositions of QSBCS in any year other than 2023)": a starting
amount, a loss in brackets."""

T657_CHART_2023_AMOUNT_I = CATALOG.declare("t657_chart_2023_amount_i", Decimal, non_negative=True)
"""Chart 2023 Part 1 amount I, Form T657 Chart 2023 Part 1 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the property was disposed of in 2023": a starting amount."""

T657_CHART_2023_PART_2_AMOUNT_G = CATALOG.declare("t657_chart_2023_part_2_amount_g", Decimal)
"""Chart 2023 Part 2 amount G, Form T657 Chart 2023 Part 2 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the QFFP was disposed of in 2023": a starting amount."""

T657_CHART_2023_CLAIMS_ADDITIONAL_DEDUCTION = CATALOG.declare(
    "t657_chart_2023_claims_additional_deduction", int, non_negative=True
)
"""Chart 2023 Part 2 gate, Form T657 Chart 2023 Part 1 "you want to claim the additional deduction,
complete Part 2": 1 when the filer wants the additional deduction, 0 when not; a starting count."""

CHART_2023_PART_1_AMOUNT_A = CATALOG.declare(
    "chart_2023_part_1_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP and/or QSBCS disposed of in 2023, Form T657 Chart 2023
Part 1 amount A: 485,595.00, a dataset."""

CHART_2023_PART_1_AMOUNT_C = CATALOG.declare(
    "chart_2023_part_1_amount_c", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount C, Form T657 Chart 2023 Part 1 "Amount A minus amount B": amount A
minus amount B, floored at 0 (the form prints no floor)."""

CHART_2023_AMOUNT_D = CATALOG.declare("chart_2023_amount_d", Decimal, non_negative=True)
"""Chart 2023 amount D, Form T657 Chart 2023 Part 1 "Capital gains deductions from previous years
from line 19 of Chart 2 (2023-1)": line 19 of Chart 2, or the (2023-1) calculation's result when
uses_d_instead is 1."""

CHART_2023_PART_1_AMOUNT_E = CATALOG.declare(
    "chart_2023_part_1_amount_e", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount E, Form T657 Chart 2023 Part 1 "Capital gains deduction available for
QFFP and/or QSBCS disposed of in 2023 and included in your 2025 income: amount C minus amount D
(if negative, enter "0")": amount C minus amount D, not below 0."""

CHART_2023_PART_1_AMOUNTS_F_AND_G = CATALOG.declare(
    "chart_2023_part_1_amounts_f_and_g", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amounts F and G, Form T657 Chart 2023 Part 1 "Taxable capital gains from a
reserve on QFFP and/or QSBCS disposed of in 2023 included in your 2025 income: amount F plus
amount G (if negative, enter "0")": the sum of amounts F and G, not below 0."""

CHART_2023_PART_1_AMOUNT_H = CATALOG.declare(
    "chart_2023_part_1_amount_h", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount H, Form T657 Chart 2023 Part 1 "amount F plus amount G (if negative,
enter "0") × 1/2 = H": amounts F and G times 1/2, rounded half-up to the cent."""

CHART_2023_PART_1_AMOUNT_I = CATALOG.declare(
    "chart_2023_part_1_amount_i", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount I, Form T657 Chart 2023 Part 1 "Amount included in box 30 of a 2025 T3
slip and the footnote area indicates the property was disposed of in 2023 × 1/2 = +": the box 30
amount times 1/2, rounded half-up to the cent."""

CHART_2023_PART_1_AMOUNT_J = CATALOG.declare(
    "chart_2023_part_1_amount_j", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount J, Form T657 Chart 2023 Part 1 "Amount H plus amount I": amounts H and
I added."""

CHART_2023_PART_1_AMOUNT_K = CATALOG.declare(
    "chart_2023_part_1_amount_k", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount K, Form T657 Chart 2023 Part 1 "Enter whichever is less: amount E or
amount J.": the lesser of amount E and amount J."""

CHART_2023_PART_1_AMOUNT_M = CATALOG.declare(
    "chart_2023_part_1_amount_m", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount M, Form T657 Chart 2023 Part 1 "Amount K plus amount L" M (L "Enter
amount B from above."): amount K plus amount B. B is Chart 2022's total carried."""

CHART_2023_PART_1_AMOUNT_N = CATALOG.declare(
    "chart_2023_part_1_amount_n", Decimal, non_negative=True
)
"""Chart 2023 Part 1 amount N, Form T657 Chart 2023 Part 1 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount M above.": the lesser of the annual gains limit, the
cumulative gains limit and amount M, the maximum for line 25400 if no later reserve is reported."""

CHART_2023_PART_2_AMOUNT_A = CATALOG.declare(
    "chart_2023_part_2_amount_a", Decimal, non_negative=True
)
"""Maximum capital gains deduction for QFFP disposed of in 2023, Form T657 Chart 2023 Part 2 amount
A: 500,000.00, a dataset."""

CHART_2023_PART_2_AMOUNT_C = CATALOG.declare(
    "chart_2023_part_2_amount_c", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount C, Form T657 Chart 2023 Part 2 "Amount A minus amount B" (B "Enter
amount M from Part 1 of Chart 2023."): amount A minus Part 1's amount M, floored at 0 (the form
prints no floor)."""

CHART_2023_PART_2_AMOUNT_E = CATALOG.declare(
    "chart_2023_part_2_amount_e", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount E, Form T657 Chart 2023 Part 2 "Capital gains deduction available for
QFFP disposed of in ... amount C minus amount D (if negative, enter "0")": amount C minus amount
D, not below 0."""

CHART_2023_PART_2_AMOUNT_F = CATALOG.declare(
    "chart_2023_part_2_amount_f", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount F, Form T657 Chart 2023 Part 2 "Amount from line 6 of Form T2017 ... ×
1/2 = F": the Part 1 amount F from line 6 of Form T2017 times 1/2, rounded half-up to the cent;
signed as its input is, the form prints no floor."""

CHART_2023_PART_2_AMOUNT_G = CATALOG.declare(
    "chart_2023_part_2_amount_g", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount G, Form T657 Chart 2023 Part 2 "Amount included in box 30 of a 2025 T3
slip ... × 1/2 = G": the box 30 amount times 1/2, rounded half-up to the cent; signed as its
input is, the form prints no floor."""

CHART_2023_PART_2_AMOUNT_H = CATALOG.declare(
    "chart_2023_part_2_amount_h", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount H, Form T657 Chart 2023 Part 2 "Amount F plus amount G" H: amounts F
and G added, with no floor (the form prints none)."""

CHART_2023_PART_2_AMOUNT_I = CATALOG.declare(
    "chart_2023_part_2_amount_i", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount I, Form T657 Chart 2023 Part 2 "Enter whichever is less: amount E or
amount H." I: the lesser of amount E and amount H."""

CHART_2023_PART_2_AMOUNT_K = CATALOG.declare(
    "chart_2023_part_2_amount_k", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount K, Form T657 Chart 2023 Part 2 "Amount I plus amount J" K (J "Enter
amount B from above.", Part 1 amount M): amount I plus Part 1's amount M."""

CHART_2023_PART_2_AMOUNT_L = CATALOG.declare(
    "chart_2023_part_2_amount_l", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount L, Form T657 Chart 2023 Part 2 "Enter whichever is less: amount H or
amount K." L: the lesser of amount H and amount K."""

CHART_2023_PART_2_AMOUNT_M = CATALOG.declare(
    "chart_2023_part_2_amount_m", Decimal, non_negative=True
)
"""Chart 2023 Part 2 amount M, Form T657 Chart 2023 Part 2 "Enter whichever is less: line 21 of
Step 1, line 19 of Step 2 or amount L above." M: the lesser of the annual gains limit, the
cumulative gains limit and amount L, the maximum for line 25400 if no other disposition is
reported."""

CHART_2023_PART_2_APPLIES = CATALOG.declare("chart_2023_part_2_applies", int, non_negative=True)
"""Chart 2023 Part 2 gate, Form T657 Chart 2023 Part 2 conditions (a QFFP reserve, you want to
claim the additional deduction, and amount E of Part 1 is no more than the three amounts the
form names): 1 when Part 2 is completed, 0 when it is not."""

CHART_2023_TOTAL_CARRIED = CATALOG.declare("chart_2023_total_carried", Decimal, non_negative=True)
"""Chart 2023 total carried, Form T657 Chart 2023 "Enter the last amount that you calculated for
"Total amount of capital gains included in 2025 income eligible for the capital gains
deduction"" for the charts after it: Part 2's amount L when Part 2 is completed, else Part 1's
amount M."""
