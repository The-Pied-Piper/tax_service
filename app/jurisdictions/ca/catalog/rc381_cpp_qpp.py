"""The federal catalog: Form RC381 Part 2 and Part 3 lines 1 to 69.

Form RC381 (2025), "Inter-Provincial Calculation for CPP and QPP Contributions and Overpayments":
Part 2 (the months and the monthly proration table, lines G to J being the QPP side) and the CPP
side of Part 3 on employment income (lines 1 to 26), then its QPP side and the totals (lines 27
to 69). Lines C to F of Part 2 are Schedule 8 Part 2's lines B to E,
the existing artifacts read with the same months.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.parameters.rate import Rate
from app.jurisdictions.ca.catalog.base import CATALOG

QPP_MONTHS = CATALOG.declare("qpp_months", int, non_negative=True)
"""Months that QPP applied, Form RC381 Part 2 line B "Enter the number of months that QPP applied
in 2025.": a count the filer enters, as the months of line A are. "The number you enter on line A
cannot be more than the number you enter on line B.", which `RC381_PART_2_LINE_B` checks."""

RC381_PART_2_LINE_B = CATALOG.declare("rc381_part_2_line_b", int, non_negative=True)
"""QPP months, Form RC381 Part 2 line B "Enter the number of months that QPP applied in 2025.",
after the check that "The number you enter on line A cannot be more than the number you enter on
line B.": the key of the monthly proration table for lines G to J."""

T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC = CATALOG.declare(
    "t4_cpp_pensionable_earnings_outside_quebec", Decimal, non_negative=True
)
"""CPP pensionable earnings outside Quebec, Form RC381 Part 3 line 1 and line 50339 "Total CPP
pensionable earnings from box 26 of all of your T4 slips where the province of employment is not
Quebec": the amount the filer enters, a starting amount. The form's "(if box 26 is blank, enter
the amount from box 14)" and "(maximum $81,200 per slip)" are the filer's to apply to each slip."""

T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC = CATALOG.declare(
    "t4_qpp_pensionable_earnings_in_quebec", Decimal, non_negative=True
)
"""QPP pensionable earnings in Quebec, Form RC381 Part 3 line 2 and line 50329 "Total QPP
pensionable earnings from box 26 of all of your T4 slips where the province of employment is
Quebec": the amount the filer enters, a starting amount. The form's "(if box 26 is blank, enter the
amount from box 14)" and "(maximum $81,200 per slip)" are the filer's to apply to each slip."""

T4_CPP_SECOND_ADDITIONAL_BOX_16A = CATALOG.declare(
    "t4_cpp_second_additional_box_16a", Decimal, non_negative=True
)
"""CPP second additional contributions on T4 slips, Form RC381 Part 3 line 25 and line 50341 "Total
actual second additional contributions on CPP pensionable earnings from box 16A of all of your T4
slips": the total the filer enters, a starting amount."""

T4_QPP_CONTRIBUTIONS_BOX_17 = CATALOG.declare(
    "t4_qpp_contributions_box_17", Decimal, non_negative=True
)
"""QPP contributions on T4 slips, Form RC381 Part 3 line 39 and line 50330 "Total actual base and
first additional contributions on QPP pensionable earnings from box 17 of all of your T4 slips":
the total the filer enters, a starting amount."""

T4_QPP_SECOND_ADDITIONAL_BOX_17A = CATALOG.declare(
    "t4_qpp_second_additional_box_17a", Decimal, non_negative=True
)
"""QPP second additional contributions on T4 slips, Form RC381 Part 3 line 45 and line 50331 "Total
actual second additional contributions on QPP pensionable earnings from box 17A of all of your T4
slips": the total the filer enters, a starting amount."""

RC381_PART_2_LINE_G = CATALOG.declare("rc381_part_2_line_g", Decimal, non_negative=True)
"""QPP maximum pensionable earnings, Form RC381 Part 2 line G "Your maximum pensionable earnings
for 2025 (maximum $71,300)": the "Maximum pensionable earnings" column of the monthly proration
table, in the row for line B's months."""

RC381_PART_2_LINE_H = CATALOG.declare("rc381_part_2_line_h", Decimal, non_negative=True)
"""QPP maximum amount subject to second additional contributions, Form RC381 Part 2 line H "Your
maximum amount subject to second additional contributions for 2025 (maximum $9,900)": that column
of the monthly proration table, in the row for line B's months."""

RC381_PART_2_LINE_I = CATALOG.declare("rc381_part_2_line_i", Decimal, non_negative=True)
"""QPP additional maximum pensionable earnings, Form RC381 Part 2 line I "Your additional maximum
pensionable earnings for 2025 (maximum $81,200)": that column of the monthly proration table, in
the row for line B's months."""

RC381_PART_2_LINE_J = CATALOG.declare("rc381_part_2_line_j", Decimal, non_negative=True)
"""QPP maximum basic exemption, Form RC381 Part 2 line J "Your maximum basic exemption for 2025
(maximum $3,500)": that column of the monthly proration table, in the row for line B's months."""

RC381_PART_3_LINE_3 = CATALOG.declare("rc381_part_3_line_3", Decimal, non_negative=True)
"""Total pensionable earnings, Form RC381 Part 3 line 3 "Line 1 plus line 2"."""

RC381_PART_3_LINE_6 = CATALOG.declare("rc381_part_3_line_6", Rate)
"""Share of pensionable earnings outside Quebec, Form RC381 Part 3 line 6 "Line 4 divided by line 5
(calculated to the fifth decimal place without rounding)": a rate (0 to 1), not money, truncated
to five decimal places."""

RC381_PART_3_LINE_7 = CATALOG.declare("rc381_part_3_line_7", Decimal, non_negative=True)
"""CPP additional maximum pensionable earnings share, Form RC381 Part 3 line 7 "Amount from line E
of Part 2 multiplied by the rate at line 6"."""

RC381_PART_3_LINE_8 = CATALOG.declare("rc381_part_3_line_8", Decimal, non_negative=True)
"""CPP maximum pensionable earnings share, Form RC381 Part 3 line 8 "Amount from line C of Part 2
multiplied by the rate at line 6"."""

RC381_PART_3_LINE_9 = CATALOG.declare("rc381_part_3_line_9", Decimal, non_negative=True)
"""CPP basic exemption share, Form RC381 Part 3 line 9 "Amount from line F of Part 2 multiplied by
the rate at line 6"."""

RC381_PART_3_LINE_10 = CATALOG.declare("rc381_part_3_line_10", Decimal, non_negative=True)
"""CPP second additional maximum share, Form RC381 Part 3 line 10 "Amount from line D of Part 2
multiplied by the rate at line 6"."""

RC381_PART_3_LINE_11 = CATALOG.declare("rc381_part_3_line_11", Decimal, non_negative=True)
"""Earnings subject to CPP contributions, Form RC381 Part 3 line 11 "Enter whichever is less:
amount from line 1 or line 7."."""

RC381_PART_3_LINE_14 = CATALOG.declare("rc381_part_3_line_14", Decimal, non_negative=True)
"""Form RC381 Part 3 line 14 "Line 12 minus line 13 (if negative, enter "0")", line 12 being the
amount from line 11 and line 13 the amount from line 8."""

RC381_PART_3_LINE_15_LESSER = CATALOG.declare(
    "rc381_part_3_line_15_lesser", Decimal, non_negative=True
)
"""Form RC381 Part 3 line 15 "Enter whichever is less: amount from line 10 or line 14.", before the
gate "If the amount from line 3 is more than the amount from line C of Part 2, complete lines 12 to
15." decides whether line 15 takes it."""

RC381_PART_3_LINE_15 = CATALOG.declare("rc381_part_3_line_15", Decimal, non_negative=True)
"""Earnings subject to second additional CPP contributions, Form RC381 Part 3 line 15 "Enter
whichever is less: amount from line 10 or line 14.", when the amount from line 3 is more than the
amount from line C of Part 2, else 0."""

RC381_PART_3_LINE_16 = CATALOG.declare("rc381_part_3_line_16", Decimal, non_negative=True)
"""Form RC381 Part 3 line 16 "Line 11 minus line 15"."""

RC381_PART_3_LINE_18 = CATALOG.declare("rc381_part_3_line_18", Decimal, non_negative=True)
"""Earnings subject to base and first additional CPP contributions, Form RC381 Part 3 line 18
"Line 16 minus line 17 (if negative, enter "0")", line 17 being the amount from line 9."""

RC381_PART_3_LINE_20 = CATALOG.declare("rc381_part_3_line_20", Decimal, non_negative=True)
"""Actual base contributions on CPP pensionable earnings, Form RC381 Part 3 line 20 "amount from
line 19 x 83.1933%"."""

RC381_PART_3_LINE_21 = CATALOG.declare("rc381_part_3_line_21", Decimal, non_negative=True)
"""Actual first additional contributions on CPP pensionable earnings, Form RC381 Part 3 line 21
"Line 19 minus line 20"."""

RC381_PART_3_LINE_22 = CATALOG.declare("rc381_part_3_line_22", Decimal, non_negative=True)
"""Required base contributions on CPP pensionable earnings, Form RC381 Part 3 line 22 "amount from
line 18 x 4.95% = (maximum $3,356.10)"."""

RC381_PART_3_LINE_23 = CATALOG.declare("rc381_part_3_line_23", Decimal, non_negative=True)
"""Required first additional contributions on CPP pensionable earnings, Form RC381 Part 3 line 23
"amount from line 18 x 1% = (maximum $678.00)"."""

RC381_PART_3_LINE_24 = CATALOG.declare("rc381_part_3_line_24", Decimal, non_negative=True)
"""Required base and first additional contributions on CPP pensionable earnings, Form RC381 Part 3
line 24 "Line 22 plus line 23"."""

RC381_PART_3_LINE_26 = CATALOG.declare("rc381_part_3_line_26", Decimal, non_negative=True)
"""Required second additional contributions on CPP pensionable earnings, Form RC381 Part 3 line 26
"amount from line 15 x 4% = (maximum $396.00)"."""

RC381_PART_3_LINE_27 = CATALOG.declare("rc381_part_3_line_27", Decimal, non_negative=True)
"""QPP additional maximum pensionable earnings left, Form RC381 Part 3 line 27 "Amount from line I
of Part 2 minus the amount from line 7"."""

RC381_PART_3_LINE_28 = CATALOG.declare("rc381_part_3_line_28", Decimal, non_negative=True)
"""QPP maximum pensionable earnings left, Form RC381 Part 3 line 28 "Amount from line G of Part 2
minus the amount from line 8"."""

RC381_PART_3_LINE_29 = CATALOG.declare("rc381_part_3_line_29", Decimal, non_negative=True)
"""QPP basic exemption left, Form RC381 Part 3 line 29 "Amount from line J of Part 2 minus the
amount from line 9"."""

RC381_PART_3_LINE_30 = CATALOG.declare("rc381_part_3_line_30", Decimal, non_negative=True)
"""QPP second additional maximum left, Form RC381 Part 3 line 30 "Amount from line H of Part 2
minus the amount from line 10"."""

RC381_PART_3_LINE_31 = CATALOG.declare("rc381_part_3_line_31", Decimal, non_negative=True)
"""Earnings subject to QPP contributions, Form RC381 Part 3 line 31 "Enter whichever is less:
amount from line 2 or line 27."."""

RC381_PART_3_LINE_34 = CATALOG.declare("rc381_part_3_line_34", Decimal, non_negative=True)
"""Form RC381 Part 3 line 34 "Line 32 minus line 33 (if negative, enter "0")", line 32 being the
amount from line 31 and line 33 the amount from line 28."""

RC381_PART_3_LINE_35_LESSER = CATALOG.declare(
    "rc381_part_3_line_35_lesser", Decimal, non_negative=True
)
"""Form RC381 Part 3 line 35 "Enter whichever is less: amount from line 30 or line 34.", before the
gate "If the amount from line 3 is more than the amount from line G of Part 2, complete lines 32 to
35." decides whether line 35 takes it."""

RC381_PART_3_LINE_35 = CATALOG.declare("rc381_part_3_line_35", Decimal, non_negative=True)
"""Earnings subject to second additional QPP contributions, Form RC381 Part 3 line 35 "Enter
whichever is less: amount from line 30 or line 34.", when the amount from line 3 is more than the
amount from line G of Part 2, else 0."""

RC381_PART_3_LINE_36 = CATALOG.declare("rc381_part_3_line_36", Decimal, non_negative=True)
"""Form RC381 Part 3 line 36 "Line 31 minus line 35"."""

RC381_PART_3_LINE_38 = CATALOG.declare("rc381_part_3_line_38", Decimal, non_negative=True)
"""Earnings subject to base and first additional QPP contributions, Form RC381 Part 3 line 38
"Line 36 minus line 37 (if negative, enter "0")", line 37 being the amount from line 29."""

RC381_PART_3_LINE_40 = CATALOG.declare("rc381_part_3_line_40", Decimal, non_negative=True)
"""Actual base contributions on QPP pensionable earnings, Form RC381 Part 3 line 40 "amount from
line 39 x 84.375%"."""

RC381_PART_3_LINE_41 = CATALOG.declare("rc381_part_3_line_41", Decimal, non_negative=True)
"""Actual first additional contributions on QPP pensionable earnings, Form RC381 Part 3 line 41
"Line 39 minus line 40"."""

RC381_PART_3_LINE_42 = CATALOG.declare("rc381_part_3_line_42", Decimal, non_negative=True)
"""Required base contributions on QPP pensionable earnings, Form RC381 Part 3 line 42 "amount from
line 38 x 5.4% = (maximum $3,661.20)"."""

RC381_PART_3_LINE_43 = CATALOG.declare("rc381_part_3_line_43", Decimal, non_negative=True)
"""Required first additional contributions on QPP pensionable earnings, Form RC381 Part 3 line 43
"amount from line 38 x 1% = (maximum $678.00)"."""

RC381_PART_3_LINE_44 = CATALOG.declare("rc381_part_3_line_44", Decimal, non_negative=True)
"""Required base and first additional contributions on QPP pensionable earnings, Form RC381 Part 3
line 44 "Line 42 plus line 43"."""

RC381_PART_3_LINE_46 = CATALOG.declare("rc381_part_3_line_46", Decimal, non_negative=True)
"""Required second additional contributions on QPP pensionable earnings, Form RC381 Part 3 line 46
"amount from line 35 x 4% = (maximum $396.00)"."""

RC381_PART_3_LINE_49 = CATALOG.declare("rc381_part_3_line_49", Decimal, non_negative=True)
"""Total actual base contributions, Form RC381 Part 3 line 49 "Total actual base contributions: line
47 plus line 48", line 47 being the amount from line 20 and line 48 the amount from line 40."""

RC381_PART_3_LINE_52 = CATALOG.declare("rc381_part_3_line_52", Decimal, non_negative=True)
"""Total required base contributions, Form RC381 Part 3 line 52 "Total required base contributions:
line 50 plus line 51", line 50 being the amount from line 22 and line 51 the amount from line 42."""

RC381_PART_3_LINE_53 = CATALOG.declare("rc381_part_3_line_53", Decimal)
"""Form RC381 Part 3 line 53 "Line 49 minus line 52 (if negative, show in brackets)": signed, the
actual base contributions can be less than the required ones."""

RC381_PART_3_LINE_56 = CATALOG.declare("rc381_part_3_line_56", Decimal, non_negative=True)
"""Total actual first additional contributions, Form RC381 Part 3 line 56 "Line 54 plus line 55",
line 54 being the amount from line 21 and line 55 the amount from line 41."""

RC381_PART_3_LINE_59 = CATALOG.declare("rc381_part_3_line_59", Decimal, non_negative=True)
"""Total required first additional contributions, Form RC381 Part 3 line 59 "Line 57 plus line 58",
line 57 being the amount from line 23 and line 58 the amount from line 43."""

RC381_PART_3_LINE_60 = CATALOG.declare("rc381_part_3_line_60", Decimal)
"""Form RC381 Part 3 line 60 "Line 56 minus line 59 (if negative, show in brackets)": signed, the
actual first additional contributions can be less than the required ones."""

RC381_PART_3_LINE_61 = CATALOG.declare("rc381_part_3_line_61", Decimal)
"""Form RC381 Part 3 line 61 "Line 53 plus line 60 (if negative, show in brackets)": signed."""

RC381_PART_3_LINE_64 = CATALOG.declare("rc381_part_3_line_64", Decimal, non_negative=True)
"""Total actual second additional contributions, Form RC381 Part 3 line 64 "Line 62 plus line 63",
line 62 being the amount from line 25 and line 63 the amount from line 45."""

RC381_PART_3_LINE_67 = CATALOG.declare("rc381_part_3_line_67", Decimal, non_negative=True)
"""Total required second additional contributions, Form RC381 Part 3 line 67 "Line 65 plus line
66", line 65 being the amount from line 26 and line 66 the amount from line 46."""

RC381_PART_3_LINE_68 = CATALOG.declare("rc381_part_3_line_68", Decimal)
"""Form RC381 Part 3 line 68 "Line 64 minus line 67 (if negative, show in brackets)": signed, the
actual second additional contributions can be less than the required ones."""

RC381_PART_3_LINE_69 = CATALOG.declare("rc381_part_3_line_69", Decimal)
"""Form RC381 Part 3 line 69 "Line 61 plus line 68 (if negative, show in brackets)": signed, the
total of the contributions over or under the required ones."""
