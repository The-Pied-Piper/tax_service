# Tax Engine — Capability Composition Design

Status: DRAFT — architecture settled; tax-law claims in §2 are UNVERIFIED
assertions and must be validated against the jurisdiction's official sources
before implementation hardens around them.

Examples come from the pilot jurisdiction, Canada / Ontario (§8). They
illustrate the design; they are not the engine's vocabulary. Generic code,
names and tests must not reuse them (e.g. `net_income`, `rrsp_deduction`)
unless the jurisdiction's own law does.

---

## 1. Core decision

Zero-code jurisdiction onboarding is rejected. Jurisdictions differ in
**computational structure**, not just parameters, and the set of structures is
open-ended. Consequences:

- **Mechanism lives in code** (capabilities — tested, typed, versioned).
- **Parameters live in data** (brackets, thresholds, rates — versioned per tax year).
- **Composition lives in a manifest** (which capabilities run for a jurisdiction).
- Design goal is **cost containment per new mechanism**, not completeness:
  adding a jurisdiction/mechanism must be additive (new capability + new
  manifest entry + new tests), never a modification of existing capabilities.
  Metric: blast radius per new mechanism ≈ 0 shared files touched.

## 2. Artifact model

Ordering is expressed through **artifacts**, not capability-to-capability
dependencies. An artifact is a named intermediate with an external referent,
produced by exactly one capability within a worksheet and consumed by any number. Every artifact
needs an external justification — a line in the law/worksheet it mirrors, or a
specific consumer contract it satisfies — and "it made the design cleaner"
is neither. A kind may also declare a constraint its line carries: a money
kind or a count declared non-negative never holds a value below zero: a
negative input is the caller's error, a negative output is the producing
capability's contract failure. Example, from the Canadian pilot
(UNVERIFIED — confirm line semantics against the T1 return):

- `total_income`
- `net_income`            (T1 line 23600 — feeds clawbacks, credit phase-outs)
- `taxable_income`        (T1 line 26000 — bracket input)
- `federal_basic_tax`
- `provincial_basic_tax`
- `provincial_credit_amounts` (ON428 line 58800 — the credit amounts, summed)
- `provincial_tax_credits`  (ON428 line 61500 — the credits, the rate applied once)
- `provincial_tax_after_credits`
- `tax_owed` (terminal)

Key facts driving this (UNVERIFIED, verify all):
- Deductions are not interchangeable: some compute net income (RRSP), some
  come after it (capital-gains deduction). Placement changes downstream
  credit math keyed to `net_income`.
- Ontario sequence: basic tax → non-refundable credits → surtax (20%/36% on
  the credited amount) → Ontario tax reduction → LIFT credit (keyed to
  employment and net income) → health premium (keyed to taxable income,
  outside surtax base).
- Cross-phase consumption is routine (age amount consumes `net_income`;
  dividend tax credit keyed to grossed-up amount added on the income side).

### Totals
A total (total income, total deductions → `net_income`) is an artifact like
any other, produced by one generic sum capability (`core/sum`) over a **list
slot**: a consume slot that takes several kinds of one value type. The
manifest lists which lines make up the total, in the order the trace shows
them; the engine knows only that it is adding amounts.

Non-refundable credits are worked out in the same generic steps: each credit
amount is an artifact (from `core/credit_amount`, `core/capped_amount`,
`core/tapered_amount`, `core/per_unit_amount`, `core/times_count` or an input),
`core/sum` adds them into one summed-amounts artifact, `core/apply_rate`
applies the one credit rate once to that sum (rounded with the rate dataset's
rule) to produce the credits artifact, and `core/subtract_not_below_zero` takes
the credits off the tax, never below zero; the part of the credits the tax
cannot absorb is lost, not refunded.

## 3. Capability contract

```
capability:
  parameters:    {slot: parameter kind, ...}  # datasets it is built from
  consumes:      {slot: value type, ...}      # reads; list[value type] = a list slot
  produces:      {slot: value type, ...}      # writes (new named artifact)
```

- Vocabulary is exactly: **consume / produce**.
  **"modify" does not exist.** A capability needing to see another's change
  is a consumer producing a new artifact, not a modifier.
- Ordering rule: an artifact's **one producer runs before any consumer**.
- Contract **shapes** are declared **in code**, next to the implementation
  that makes them true: each capability names its slots — parameter slots,
  each with a parameter kind, and artifact slots for what it consumes and
  produces, each with a value type. A capability may have zero, one or
  several parameter slots. The manifest chooses which parameter families
  and which artifacts fill those slots (§4); it never declares edges or
  order. The order is derived from what each selection consumes and
  produces (§5 — single source of dependency truth).
- A slot holds one kind when the input has a role of its own that the
  mechanism treats differently (`base`, `tax`, the two sides of a
  subtraction). A slot holds a list when every input plays the same role
  and the jurisdiction decides how many there are (the parts of a sum): the
  only names left for them would be positional. A list is not "optional"
  (every slot is filled, a list possibly with nothing) and not "mixed roles"
  (a base plus any number of adjustments is one single slot and one list).
- Capabilities are pure mechanism: no jurisdiction constants in code, ever.
  (Prior incident: engine silently US-shaped by agent priors. Same vector.)
- Reuse across jurisdictions = a capability keyed to an artifact is
  indifferent to that artifact's provenance (brackets consume
  `taxable_income` whether 12 parts built it or 2).

### Rounding

Rounding is a parameter, never a jurisdiction constant in code.

- One central rounding type (increment + mode) is the only way amounts
  are rounded. The increment is the step rounded to (e.g. 0.01, 1,
  0.05), which covers decimal-place precision and more. **Default is no
  rounding**: exact decimal arithmetic, never floats. An assumed default
  (e.g. half-up to the cent) would be a silent prior, the same failure
  class as implicit carry-forward.
- Exactness is enforced, not assumed: every capability runs under a `decimal`
  context that traps `Inexact`, so arithmetic that would lose digits raises
  instead of being rounded to the context's precision. A division is done as an
  exact fraction and handed to the rule, which rounds once; the rule is the only
  place allowed to be inexact. With no rounding, a quotient that has no finite
  decimal expansion raises.
- A capability's rounding rule lives in its parameter datasets, resolved
  per (family, tax_year) like any other parameter. A capability with
  several parameter slots decides which slot's rule it applies where. Rounding can
  therefore differ between capabilities in one jurisdiction and between
  tax years, and the provenance fingerprint (§7) covers it.
- A figure a parameter's own values compute is rounded by a rule its dataset
  states beside the capability's, in the same form. A bracket schedule holds
  each bracket's lower bound and rate; it computes the tax at each bracket's
  start as the exact tax on the brackets below, rounded by the dataset's
  `tax_at_start_rounding` (the dataset for a form that prints that tax to the
  cent states half-up to 0.01). The dataset never repeats a figure the engine
  computes; that the computed figure matches the form's printed one is a
  jurisdiction test.
- Each capability defines *where* it rounds (e.g. each tier's part vs.
  once at the end); the parameter defines *how*. Given a rule, the
  capability must apply it; given none, it does not round. Progressive tax
  rounds once, on the column's tax; the tax at the bracket's start inside it
  is already rounded by the schedule's own rule.
- No global rounding step. Rounded values appear as rounded in the
  trace.

## 4. Manifest (per jurisdiction)

YAML. **Selection + slot bindings only — topology is derived, never authored.**
Each selection names a capability and fills the slots its code declares (§3):
parameter slots with parameter families, artifact slots with artifact
identifiers.

```yaml
jurisdiction: CA-ON
version: 2                  # increments on structural change only
valid_from_tax_year: 2023   # inclusive; open-ended until a successor
                            # manifest closes it (contiguity invariant)
capabilities:
  - name: core/progressive_tax          # <namespace>/<local id>
    params:                             # parameter slot -> family; resolution
      schedule: ca-on/brackets          #   looks up (family, tax_year) -> that
                                        #   year's dataset or attestation;
                                        #   absent year = loud failure,
                                        #   no implicit carry-forward
    consumes:                           # artifact slot -> artifact identifier
      base: ca/taxable_income
    produces:
      output: ca-on/ontario_basic_tax
  - name: core/apply_rate
    params:
      rate: ca-on/credit_rate           # one rate, stated once, in its own dataset
    consumes:
      base: ca-on/non_refundable_credit_amounts  # the summed credit amounts
    produces:
      output: ca-on/non_refundable_tax_credits
  - name: core/subtract_not_below_zero
    consumes:
      amount: ca-on/ontario_basic_tax
      less: ca-on/non_refundable_tax_credits
    produces:
      output: ca-on/ontario_tax_after_credits
  # `params` may be omitted when a capability has no parameter slots,
  # `consumes` when it consumes nothing; `produces` is required.
  # list order advisory; composition derives true order from what each
  # selection consumes and produces, and rejects unsatisfiable selections
```

A manifest is `(jurisdiction, version, valid_from_tax_year, inputs, forms)`:
`inputs` are the artifacts a computation starts from, the instances kinds
among them, and `forms` are the
groups of selections that run (§6). The `capabilities` list above is the
selections of the default form; a part may instead give its selections to a
named form with a `form:` key. In YAML the default form is written as
top-level `capabilities` and `outputs` (its exports); `inputs` is required.

Rules:
- No edges, no ordering, no conditionals, no expressions in YAML — the moment an `if`
  appears, the manifest is becoming an untyped programming language
  (the failure mode the zero-code rejection was meant to kill).
  Conditionality lives inside capabilities (a capability may produce zero).
- Two version axes, independent:
  - **Manifests** version on structural change only (capability added or
    removed, composition changed). Each declares `valid_from_tax_year`
    (inclusive, open-ended); a successor's `valid_from` closes it. Unchanged
    years produce no new manifest.
  - **Parameter datasets** resolve by (family, tax_year). Every covered tax
    year requires an affirmative dataset — real values or an explicit
    attestation ("2027 = 2026, confirmed"). No implicit carry-forward: an
    absent year fails resolution loudly; silence means *missing*, never
    *assumed unchanged*.
  - **Dataset immutability mirrors manifest immutability, keyed to
    release:** a dataset revision is frozen once released to production
    (exposed to users); before release, edit freely. Any post-release
    change — transcription error or legal amendment alike — is a new
    *revision* of that (family, tax_year), never an edit in place; the
    revision record states its cause; prior revisions are retained
    forever. Resolution picks the revision deterministically via
    computation_date (a March return reproduces on the revision current
    in March). Enforcement: release-pipeline check — released revisions
    never diff.
- Tax year is a query input, not a manifest field. Resolution:
  (jurisdiction, tax_year, computation_date) → the one manifest whose
  validity range covers the tax year, with computation_date disambiguating
  retroactive successors → each parameter slot's family resolved against
  that tax year.
- The tax year is the atomic unit of computation and resolution. Mid-year
  legal changes land through one of three channels — never through
  sub-annual resolution:
  - *Values, pre-release*: expressed inside the year's dataset (e.g. 2025's
    mid-year 15%→14% federal cut = blended 14.5% bottom rate), with an
    effective-date audit trail.
  - *Values, post-release*: a new dataset revision — same mechanics as a
    correction.
  - *Structure* (e.g. a new incentive requires a new capability): a
    successor manifest with `valid_from_tax_year` = the current year — the
    retroactive-successor mechanism, disambiguated by computation_date.
  Forbidden is sub-annual *resolution*: no manifest or dataset applies to
  part of a year. Where the law itself splits a year (e.g. a mid-year
  inclusion-rate change creating period-1/period-2 amounts), the split
  lives in the capability's inputs and parameters, not in the resolver.
- Contiguity invariant: one manifest's `valid_from` = its predecessor's end;
  no gaps, no overlaps; no stored `valid_to`.
- History is immutable: corrections close a version early and issue a
  successor; never edit in place.
- Retroactive amendments appear as multiple manifests covering the same tax
  year; resolution rejects any (jurisdiction, tax_year, computation_date)
  that resolves to more than one.

## 5. Composition (most safety-critical component)

Validates at **registration time**, fails loudly. Rejects:

1. Selection with unsatisfied `consumes` (no selected producer).
2. Cycles.
3. Type-mismatched artifact wiring (artifacts are typed, not stringly named).
4. Orphan outputs / unreferenced producers.
5. **Seeded policy data not referenced by the resolved graph** — the
   dead-surtax-data bug class: data staged, composition silent.
6. Version-resolution ambiguity (§4).
7. Absent parameter dataset for a resolved (family, tax_year) — enforcement
   point for §4's no-carry-forward rule: no values and no attestation ⇒
   resolution fails.

Rules 5–7 involve manifests and parameter data, which the composition never
sees; they are enforced at resolution (the application service), not by the
composition.

The composition derives execution order (topological sort). Manifest list
order is ignored — asserted order is never trusted.

Each form (§6) has its own inner `Composition`, built once, which checks the
form's wiring by rules 1-4 and orders its capabilities. `FormSet` adds
one more order, over forms: a form runs after every form whose exports it
imports.

## 6. Forms

A **form** is a named group of capabilities with the artifacts it exports. A
**Worksheet** is one filled-in copy of a form: the figures one run of it
produced. The return is not a form with others beneath it: forms are **peers**,
flat, and none is special. Some jurisdictions' returns are one form, others
are a set of forms that together are the return (Canada is close to the second).
A form is never a capability, and forms do not nest.

- `Form` is frozen manifest data: `name`, `instances`, `exports`,
  `capabilities` (its selections) and the optional limits `max_instances`,
  `min_instances` and `exclusive_group` (see Limits). A form exports at least one artifact. A
  form's inputs are not declared: with instances they are the fields of the
  record; without, the starting artifacts its selections read or export; plus
  its imports.
- `FormComposition` is the form wired: its inner `Composition`, whose outputs
  are the form's exports.
- `FormSet` holds a computation's forms. It orders them by what they import,
  runs each form once per instance on its own `Worksheet`, keeps the derived
  `<form>.<export>` kinds in one store, and hands each run its imports as
  starting artifacts.

**Instances.** A form's `instances` kind is a record list the caller supplies,
one record per instance (a second T2125 is a second record); the record's
fields are the form's inputs. The instances kind is itself one of the
manifest's `inputs`, supplied with the other starting artifacts. A form with
no instances list has exactly one implicit instance, and takes its inputs from
the computation's starting artifacts.

**Limits.** A form may declare `max_instances` (at least 1) and
`min_instances` (at least 0, at most the maximum); both together with 1 and 1
say "exactly one" (Schedule 8, RC381). Every form has an instances count: a
form with no instances list has a default list of one instance, so a limit
applies to it the same way, and a `min_instances` above 1 on it is refused when
the manifest loads. Too many or too few instances is refused when the
computation starts, before any form runs, naming the form (`ValidationError`:
the count is the caller's input). A form may also name an `exclusive_group`:
at most one form of a group may have instances (a declared empty list claims
nothing). A group naming one form, or two forms that always have an instance,
is refused when the `FormSet` is built. The loader reads the three keys from
the part that declares the form's exports.

**Exports.** For each export `X` of form `B`, the engine derives the kind
`B.X`: a record list of one field, `X`, with one record per instance, in
instance order. A kind identifier has at most one dot; a form cannot export a
dotted kind. A list-valued export is a list of lists. A kind a record cannot
hold (a rate, say, or digits) gets none and stays on the form's own worksheets.
The dot is the delimiter (the slash stays the namespace): were T2125 its own
form, its export would be `ca/t2125.business_income`. The dotted identifier is built by the engine, never written in a manifest.

**Imports.** Any form may read another's exports, by the derived kind, and
none needs declaring. Forms are run in the order the imports give. A cycle of
imports (a form reading its own `B.X` is one), an import no form exports, and a
derived kind given as an input are among those refused when the `FormSet` is
built (a derived kind given at `compute` is refused too).

**Result.** A computation returns a plain mapping: form name to one
`Worksheet` per instance, in instance order, an empty tuple for a form whose
instances list is empty. Errors and the trace name the form and the instance:
`<form>, instance N` (1 for a form without an instances list).

**Loader.** A part with a `form:` key (`name`, and optionally `exports` and
`instances`) gives its `capabilities` to that form. A form may span several
parts, but exactly one declares its exports; a part with a `form:` key takes no
`inputs` or `outputs`. A part with no `form:` key joins the default form,
`<namespace>/return` (the lower-cased jurisdiction code; for Ontario
`ca-on/return`), whose exports are the manifest's `outputs`. The default
form's name is reserved for those parts: a part with a `form:` key that names
it is rejected. A single manifest file is not a part and takes no
`form:` key (all of it is the default form). Only `name` is required in a
`form:` block; `exports` and `instances` are optional per part, but `instances`
without `exports` is an error, and every form needs a part that declares its
exports. Default-form `outputs` sharing a local id (`ex/x` and `ca/x`) are
rejected.

## 7. Provenance

- `datasetVersion` hash covers the **resolved computation identity**:
  manifest version + graph topology + each resolved (family, tax_year,
  revision) dataset identity — where an attestation contributes its *own*
  identity
  (the attestation record and what it points at), never merely the values
  it dereferences to. Rule: identical values reached by different
  resolution paths must not share a version string — same principle as
  topology (identical brackets, different graph shape ⇒ different
  version), extended to parameter resolution.
- Every computation records manifest version; "recompute under current
  rules" and "reproduce the prior result" are distinct, both-supported
  operations — covering both retroactive amendments *and* dataset
  corrections (a correction is a retroactive change to our data rather
  than to the law; same mechanics). Recall workflow falls out: "find every
  return computed on the bad revision" is a fingerprint lookup, not an
  investigation. (Retroactivity requirement — accounting-firm audit
  question.)
- Trace: each capability emits a labeled breakdown; the `FormSet` emits one
  trace per form instance (form name and instance number), forms in run order,
  capabilities in execution order within each. Target readability: the tax
  authority's own worksheet (e.g. CRA's), line-by-line, each line
  attributable to one capability + parameter set.
  **This trace is the AI-interface safety property: engine computes and
  explains; AI only narrates. Non-negotiable.**

## 8. Scope (first milestone)

Generality earns its existence on repetition, not anticipation. The rule
of three is a guideline, not a rule: by default, generalize once a third
case needs the same thing. Generalize earlier when reuse is clearly
foreseeable, e.g. a mechanism Canadian provinces share with each other or
with the federal level.

- **One jurisdiction:** the CA-ON manifest with `valid_from_tax_year: 2025`,
  and one parameter dataset per family for tax year 2025.
- **Artifact catalog for that jurisdiction only.** Every name must map to
  that jurisdiction's own law or return (§2). Names borrowed from other
  tax systems (e.g. US `agi`, `standard_deduction`) bring foreign
  structure into the engine.
- **Capabilities:** only those the CA-ON 2025 computation needs.
- **No multi-jurisdiction tooling,** no manifest editors and no speculative
  primitives without repetition or clearly foreseeable reuse.
