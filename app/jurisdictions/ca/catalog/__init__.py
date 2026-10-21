"""The federal Canada artifact catalog: artifact kinds named from Canada's own return (§2, §7).

Only the kinds in use are declared, each non-negative except the lines that print no floor: none of
these lines can be negative on the return as modelled except the refund or balance owing, where
negative means a refund, lines 5 and 9 of the Federal Worksheet for line 25000, the five "Net"
self-employment income lines (T1 lines 22 to 26), line 27, Schedule 8 Part 4 line 1, the net income
before adjustments (line 23400, "if negative, show in brackets") and the lines of Form T1436 and of
Schedule 15 that print no "(if negative, enter "0")". Amounts are Decimal; the counts of eligible
dependants, of infirm children, of the eligible children for child care (Form T778 Part B lines 1
to 3), of the Schedule 6 eligible dependants (line 38100), the two starting counts of the Federal
Worksheet for line 25000, the Schedule 15 count of a maximum participation period that ended in
a prior year, the months of Schedule 8 box A, the Schedule 8 Part 4 and Schedule 13 counts, the
capital cost allowance count of no property left in a class, the day counts of Form T2222 Step 2
and the individual and the zone of a trip are int. Chart A and Chart B of Form
T2222 are record lists, each a `RecordListKind` declared here.
Identifiers are stable: `tests/jurisdictions/ca/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from app.jurisdictions.ca.catalog.base import CATALOG as CATALOG

# The family modules are imported in the order of the T1, which is the order the kinds are
# declared on CATALOG, so they are not sorted.
# isort: off
from app.jurisdictions.ca.catalog.income import *  # noqa: F403
from app.jurisdictions.ca.catalog.rrsp_fhsa import *  # noqa: F403
from app.jurisdictions.ca.catalog.deductions import *  # noqa: F403
from app.jurisdictions.ca.catalog.taxable_income import *  # noqa: F403
from app.jurisdictions.ca.catalog.capital_gains_deduction_charts import *  # noqa: F403
from app.jurisdictions.ca.catalog.personal_amounts import *  # noqa: F403
from app.jurisdictions.ca.catalog.non_refundable_credits import *  # noqa: F403
from app.jurisdictions.ca.catalog.credits_against_federal_tax import *  # noqa: F403
from app.jurisdictions.ca.catalog.resp_aips import *  # noqa: F403
from app.jurisdictions.ca.catalog.other_inputs import *  # noqa: F403
from app.jurisdictions.ca.catalog.net_tax import *  # noqa: F403
from app.jurisdictions.ca.catalog.alternative_minimum_tax import *  # noqa: F403
from app.jurisdictions.ca.catalog.canada_workers_benefit import *  # noqa: F403
from app.jurisdictions.ca.catalog.refundable_credits import *  # noqa: F403
from app.jurisdictions.ca.catalog.refund import *  # noqa: F403
# isort: on
