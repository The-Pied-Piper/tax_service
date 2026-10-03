# Tax Engine — Capability Composition Design

Status: DRAFT — architecture settled; tax-law claims in §2/§6 are UNVERIFIED
assertions and must be validated against the jurisdiction's official sources
before implementation hardens around them.

Examples come from the pilot jurisdiction, Canada / Ontario (§7). They
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
dependencies. Two kinds:

### Spine artifacts
Named intermediates with an external referent. Every artifact needs an
external justification — a line in the law/worksheet it mirrors, or a
specific consumer contract it satisfies — and "it made the design cleaner"
is neither. Example, from the Canadian pilot (UNVERIFIED — confirm line
semantics against the T1 return):

- `total_income`
- `net_income`            (T1 line 23600 — feeds clawbacks, credit phase-outs)
- `taxable_income`        (T1 line 26000 — bracket input)
- `federal_basic_tax`
- `provincial_basic_tax`
- `provincial_tax_after_credits`
- `tax_owed` (terminal)

Key facts driving this (UNVERIFIED, verify all):
- Deductions are not interchangeable: some compute net income (RRSP), some
  come after it (capital-gains deduction). Placement changes downstream
  credit math keyed to `net_income`.
- Ontario sequence: basic tax → non-refundable credits → surtax (20%/36% on
  the credited amount) → Ontario tax reduction → health premium (keyed to
  taxable income, outside surtax base).
- Cross-phase consumption is routine (age amount consumes `net_income`;
  dividend tax credit keyed to grossed-up amount added on the income side).

### Fold contributions
Commutative deltas accumulating into a spine artifact (RRSP, union dues,
child care → `net_income`). Sibling contributions are unordered **and must
not matter**. Enforced by permutation tests: run sibling contributions in
every order and require identical output. This catches a capability
declared as a fold contribution whose result actually depends on order.

## 3. Capability contract

```
capability:
  consumes:      [artifact, ...]   # spine reads
  produces:      [artifact, ...]   # spine writes (new named artifact)
  contributes_to: artifact         # fold delta (commutative)
```

- Vocabulary is exactly: **consume / produce / contribute_to**.
  **"modify" does not exist.** A capability needing to see another's change
  is a consumer producing a new spine artifact, not a modifier.
- Ordering rule: for each artifact, **all contributions complete before any
  consumer runs**.
- Contracts are declared **in code**, next to the implementation that makes
  them true. The manifest never declares edges (see §4 — single source of
  dependency truth).
- Capabilities are pure mechanism: no jurisdiction constants in code, ever.
  (Prior incident: engine silently US-shaped by agent priors. Same vector.)
- Reuse across jurisdictions = a capability keyed to an artifact is
  indifferent to that artifact's provenance (brackets consume
  `taxable_income` whether 12 contributions built it or 2).

### Rounding

Rounding is a parameter, never a jurisdiction constant in code.

- One central rounding type (precision + mode) is the only way amounts
  are rounded. **Default is no rounding**: exact decimal arithmetic,
  never floats. An assumed default (e.g. half-up to the cent) would be
  a silent prior, the same failure class as implicit carry-forward.
- A capability's rounding rule lives in its parameter dataset, resolved
  per (family, tax_year) like any other parameter. Rounding can
  therefore differ between capabilities in one jurisdiction and between
  tax years, and the provenance fingerprint (§6) covers it.
- Each capability defines *where* it rounds (e.g. per bracket slice vs.
  once at the end); the parameter defines *how*. Given a rule, the
  capability must apply it; given none, it does not round.
- No global rounding step. Rounded values appear as rounded in the
  trace.

## 4. Manifest (per jurisdiction)

YAML. **Selection + parameters only — topology is derived, never authored.**

```yaml
jurisdiction: CA-ON
version: 2                  # increments on structural change only
valid_from_tax_year: 2023   # inclusive; open-ended until a successor
                            # manifest closes it (contiguity invariant)
capabilities:
  - name: rrsp_deduction
    params_family: ca/rrsp          # loader resolves (family, tax_year)
  - name: progressive_brackets
    params_family: ca-on/brackets   # -> that year's dataset or attestation;
                                    #    absent year = loud failure,
                                    #    no implicit carry-forward
  # list order advisory; loader derives true order from code-declared
  # contracts and rejects unsatisfiable selections
```

Rules:
- No edges, no conditionals, no expressions in YAML — the moment an `if`
  appears, the manifest is becoming an untyped programming language
  (the failure mode the zero-code rejection was meant to kill).
  Conditionality lives inside capabilities (a capability may contribute zero).
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
  retroactive successors → each parameter family resolved against that
  tax year.
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
  year; the loader rejects any (jurisdiction, tax_year, computation_date)
  that resolves to more than one.

## 5. Loader (most safety-critical component)

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

Loader derives execution order (topological sort). Manifest list order is
checked against derived order and warnings/errors surfaced — asserted order
is never trusted.

## 6. Provenance

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
- Trace: each capability emits a labeled breakdown; orchestrator
  concatenates in execution order. Target readability: the tax
  authority's own worksheet (e.g. CRA's), line-by-line, each line
  attributable to one capability + parameter set.
  **This trace is the AI-interface safety property: engine computes and
  explains; AI only narrates. Non-negotiable.**

## 7. Scope (first milestone)

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
