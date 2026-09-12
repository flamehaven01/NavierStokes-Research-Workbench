# M4-P v0.2.1 Evidence Integrity Patch Plan

Date: `2026-09-11`

Status: `PATCH_PLAN_APPROVED_FOR_IMPLEMENTATION`

Implementation authorization: `AUTHORIZED[P0-P4_README]`

Target release: `v0.2.1`

Scope: verifier integrity hardening only. This plan does not widen any mathematical claim, does not promote M4-S, and does not establish paper--Lean semantic equivalence.

Successor boundary: commit `5434400e9f91ac0892bdca257e7c90e50b32eb35`
preserves the v0.2.1 implementation checkpoint. Remaining hosted closure and
the audit-alignment defects are executed under the v0.2.2 addendum in
`docs/V0.2.1_SUBPATCH_AUDIT_ALIGNMENT_AND_SOURCE_INTERFACE.md`. This parent
contract remains authoritative for its P0--P5 requirements.

Closure note: this is the preserved historical plan, not the current status
ledger. Its requirements were implemented through v0.2.3 and exercised by
hosted run `34617896806`; current results are recorded in
`docs/V0.2.2_AUDIT_PATCH_TO_V0.2.3_CLOSURE.md` and
`docs/stage_receipts/M4P_V0.2.3_HOSTED_LIVE.md`. The unchecked boxes below are
the original acceptance checklist and must not be read as the current release
state.

## 0. Threat Model and Trust Anchors

`v0.2.1` distinguishes four different properties that must not be collapsed into one another:

```text
integrity
  bounded byte/content consistency under declared hashes and schemas

execution
  evidence that the declared command actually ran and produced the admitted artifact

provenance
  evidence about where and under which bounded CI/local execution context the artifact was produced

authenticity
  independent assurance about authorship, signer identity, or supply-chain authority
```

Repository-local hashes establish bounded consistency, not independent authorship, signer identity, or supply-chain authenticity.

Current trust anchors are limited to:

- pinned upstream Git commit/tag;
- pinned Lean toolchain;
- pinned GitHub Actions revisions;
- hosted CI run identity for release-authoritative live evidence;
- protected release/tag process where configured.

These anchors define the current bounded trust model only; they do not create independent authorship or supply-chain authenticity.

The verifier must not silently promote one property into another. In particular, a matching SHA-256 does not prove who produced an artifact, and a historical receipt does not prove that the current machine rebuilt it.

Execution evidence is split into a deterministic canonical evidence receipt and, where applicable, a run-specific provenance envelope:

```text
canonical evidence receipt
  source commit / toolchain / target / command specification / exit code
  artifact digests / dependency surface / manifest digest / verdict
  -> deterministic for identical admitted evidence

execution provenance envelope
  CI provider / workflow identity / run id / attempt / platform / time
  canonical receipt digest
  -> intentionally run-specific
```

Machine-private data such as absolute local paths, usernames, credentials, tokens, or unbounded environment dumps must never appear in public receipts.

## 1. Purpose

`v0.2.0` closed several earlier verifier defects: source-signature binding, structured compiled receipts, baseline-delta mutation attribution, LF/CRLF source custody, Cone relation enum validation, and dangling dependency rejection. Those closures remain valid.

A second adversarial review then found new false-PASS surfaces in the general M4 manifest verifier. The fixed pilot fixture still passes its declared scoped gate, but the verifier can currently admit malformed or semantically weaker inputs that the contract language implies should fail.

The patch objective is therefore narrower than “improve M4.” It is:

> make the M4-P verifier reject every currently reproduced false-PASS while preserving the existing scoped pilot as a bounded control surface.

The governing principle remains `ABSTAIN > FABRICATE`. A verifier that cannot distinguish replay evidence from live artifacts, cannot enforce a declared positivity assumption, or accepts malformed exact arithmetic must not issue an authoritative PASS.

## 2. Canonical current state

```text
M3 engineering                         CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY
M3R scoped compiled evidence           PASS[SCOPED]
M4-P fixed v2 pilot fixture            PASS[SCOPED]
M4-P general manifest verifier         CONTESTED[FALSE_PASS_SURFACES]
M4-P analytic research lane            OPEN
M4-S selected source instance          HELD[NONCOMPUTABLE_SOURCE_INSTANCE]
Paper--Lean semantic equivalence       OPEN_RESEARCH_OBLIGATION
Millennium-problem solution            NOT_ESTABLISHED
```

This distinction is mandatory: the fixed pilot result is not revoked merely because the general verifier has broader false-PASS surfaces. Conversely, the fixed pilot must not be used to claim that arbitrary manifests satisfying the current runtime contract are sound.

## 3. Reproduced false-PASS set

The following malformed or semantically invalid inputs have been reported to pass the full gate under `v0.2.0`:

1. Support cutoff `-1`.
2. A violated `LE` Cone inequality combined with `minimum_margin = -3`.
3. Boolean values used in numeric positions (`True` / `False`).
4. An empty exact-moment identity `terms=[]`, `expected=0`.
5. Receipt replay accepted without requiring the current Lean checkout to contain the referenced `.olean` artifacts.

Each item becomes a mandatory regression falsifier in `v0.2.1`.

## 4. Patch architecture

```text
P0  Evidence-mode / contract integrity
  ↓
P1  Support semantic execution
  ↓
P2  Cone soundness
  ↓
P3  Exact-moment soundness
  ↓
P4  Mutation corpus expansion
  ↓
P5  Full-gate regression / release promotion
  ↓
Optional Rust custody MVP
```

P0--P4 are required for `v0.2.1`. Rust is explicitly not a release blocker.

The required contract amendments have been re-reviewed. Implementation is
authorized for the bounded P0--P4 and README scope; release promotion still
requires the full P5 gate.

---

# P0 — Evidence Mode and Contract Integrity

Status target: `PASS[EVIDENCE_MODE_SEPARATED]`

Importance: critical

Difficulty: high

## P0.1 Problem

`v0.2.0` verifies a committed structured compiled receipt, but receipt replay and current-machine live artifact verification are not represented as distinct evidence modes.

This creates an authority ambiguity:

```text
historical hosted build receipt
      ≠
current local Lean build artifacts
```

A valid historical receipt is useful evidence, but it must not imply that the current `lean_root` contains the same `.olean` files or dependency surface.

## P0.2 Contract v3

Create additive contract version:

`contracts/m4-obligation-manifest-v3.schema.json`

Add top-level or source-binding field:

```json
"compiled_evidence_mode": "RECEIPT_REPLAY | LIVE_ARTIFACT"
```

Semantics:

### `RECEIPT_REPLAY`

Verifies a previously produced bounded receipt.

Required checks:

- receipt exists under evidence root;
- receipt SHA-256 matches manifest;
- schema id matches;
- formal source commit matches;
- toolchain matches;
- target matches;
- recorded exit code is `0`;
- `.olean` path and recorded `.olean` SHA are structurally valid;
- dependency-surface SHA exists and is valid.

Non-claim:

> receipt replay does not assert that the current machine contains or rebuilt the compiled artifact.

Recommended result label:

`PASS[COMPILED_RECEIPT_REPLAY]`

### `LIVE_ARTIFACT`

`LIVE_ARTIFACT` means that the target was rebuilt in the same bounded execution that issues the verdict. Merely finding an existing `.olean` on disk is not live evidence.

Required checks:

- `lean_root` supplied;
- Git HEAD equals formal source commit;
- build occurs from a clean checkout or isolated clean build directory;
- the declared target build command is executed in the same run;
- command, working-directory class, exit code, source commit, toolchain, and target are recorded;
- only the `.olean` produced by that same build execution is admitted and hashed;
- the generated `.olean` exists at the expected path;
- generated `.olean` SHA-256 matches the admitted value;
- direct dependency surface is regenerated from that same toolchain/source execution;
- regenerated dependency-surface digest matches admitted receipt/manifest;
- toolchain identity matches the pinned toolchain;
- missing or stale artifact is FAIL, never SKIPPED/PASS.

Evidence authority is tiered:

```text
existing artifact inspection only
  -> LOCAL_ARTIFACT_INSPECTION

same-run clean local build
  -> PASS[COMPILED_LIVE_ARTIFACT_LOCAL]

same-run clean hosted CI build
  -> PASS[COMPILED_LIVE_ARTIFACT_CI]
```

Only hosted clean CI may grant release-authoritative `PASS[COMPILED_LIVE_ARTIFACT_CI]` status. A local same-run build remains valid execution evidence but does not by itself promote a release.

## P0.3 Receipt generator extraction

Move the GitHub Actions inline Python heredoc that creates the Lean receipt into a project-owned module:

`src/nsrw/lean_receipt.py`

It should expose deterministic functions such as:

```text
build_target_record(...)
build_compiled_receipt(...)
write_compiled_receipt(...)
verify_live_target(...)
```

CI and local tooling must call the same implementation.

Receipt publication must be atomic:

```text
write temporary file
  -> flush / fsync where supported
  -> validate completed bytes
  -> atomic replace of canonical output
```

A failed execution must never leave a previous PASS receipt appearing to be the result of the failed run. The canonical receipt must be deterministic for identical admitted evidence; run-specific CI identity belongs in a separate provenance envelope bound to the canonical receipt digest.

The envelope shape is versioned separately as
`contracts/lean-execution-provenance-v1.schema.json`; its run id and timestamps
are provenance fields, not part of the deterministic canonical receipt.

This removes duplicate evidence-generation semantics from YAML.

## P0.4 Compiled receipt schema

Add:

`contracts/lean-compiled-evidence-v1.schema.json`

Schema must require:

- `schema_id`
- `formal_source_commit`
- `toolchain`
- target map
- for each target:
  - `target`
  - `exit_code`
  - `olean_path`
- `olean_sha256`
- `dependency_surface_sha256`

The compiled receipt contract must also require the fields used by the threat
model: `compiled_evidence_mode`, `command_spec_id`, a normalized command
specification, `build_cleanliness_class`, `input_bytes_sha256`,
`canonical_manifest_sha256`, `dependency_surface_profile`, and
`canonicalization_profile`.

`additionalProperties: false` is the default. Extensions must live under an
explicit namespaced extension object and must not silently enter the authority
surface.

## P0.5 Schema/runtime convergence

The JSON Schema and Python validator currently have overlapping but non-identical authority.

For v3:

- define evaluator object schemas by family;
- constrain numeric fields structurally;
- constrain relation enum in schema as well as runtime;
- require non-empty arrays where the runtime assumes them;
- reject undocumented additional evaluator properties unless an extension point is explicitly intended;
- add a regression test that validates every admitted fixture against JSON Schema and Python runtime validation and compares expected acceptance/rejection.

Goal:

`SCHEMA_RUNTIME_CONSISTENT`

not merely “both happen to pass the pilot fixture.”

## P0.5A Strict JSON input profile

All verifier-controlled JSON inputs must pass a strict parser before schema or mathematical evaluation. Implement this in a dedicated module such as `src/nsrw/strict_json.py`.

Required input policy:

- UTF-8 without BOM; reject a BOM rather than guessing;
- reject duplicate object keys;
- reject `NaN`, `Infinity`, and `-Infinity`;
- enforce explicit maximum manifest/receipt byte size;
- enforce maximum nesting depth;
- enforce maximum object member count and array length;
- do not apply implicit Unicode normalization;
- reject malformed input before evaluator dispatch.

The v3 implementation freezes the initial resource limits at 1 MiB per input,
32 nesting levels, 1024 object members, 4096 array items, and 262144 UTF-8
bytes per string. Exact rational fields are limited to 256 digits per numerator
or denominator, 4096 terms per identity, and 4096 identities per manifest.
Changing a limit requires a contract-version change or a documented migration
receipt.

Custody requires two distinct digests:

```text
input_bytes_sha256
  SHA-256 of the exact admitted UTF-8 input bytes

canonical_manifest_sha256
  SHA-256 of the strict-parsed object serialized under the declared canonical JSON profile
```

The canonical serialization profile must define key ordering, separators/newline
policy, Unicode escaping policy, and exact handling of numeric fields. Raw-input
identity and semantic-object identity must not be conflated.

The v3 profile is `NSRW-CANONICAL-JSON-1`: sorted object keys, compact
separators, UTF-8 without a trailing newline, and the exact numeric/string
rules above. It is a project-local profile, not a claim of full RFC 8785
implementation. The strict parser rejects non-finite constants and duplicate
keys before canonical serialization.

## P0.5C Textual source-locator boundary

The current locator implementation is textual and hash-bound, not an elaborated
Lean declaration resolver. Every such locator must carry:

```json
"locator_evidence_class": "TEXTUAL_PINNED_SOURCE_LOCATOR"
```

This class means only that the declared source bytes, declaration text, and
ordered fragments match the pinned artifact. It does not establish theorem
identity, elaborated dependency semantics, or paper--Lean equivalence.

## P0.5D Status and error lattice

The executable contract uses the following disjoint outcomes:

```text
PASS           every required check completed and passed
FAIL           an admitted input or evidence condition is falsified
ERROR          parser, filesystem, Git, Lean, or resource execution failed
SKIPPED        optional check only; never sufficient for a required gate
NOT_APPLICABLE mutation is outside its declared evidence mode
```

Any required `ERROR`, `SKIPPED`, or `NOT_APPLICABLE` condition leaves the gate
`HELD` unless the mode-specific contract explicitly excludes that condition.
CLI exit codes must be deterministic: `0` for PASS, `1` for FAIL, and `2` for
ERROR or unresolved required execution.

## P0.5B Contract-version routing

`v2` and `v3` have different authority and must be routed explicitly.

```text
v2
  historical compatibility / replay only
  may produce PASS[HISTORICAL_V2_REPLAY]

v3
  hardened verifier contract
  may produce PASS[HARDENED_V3]
```

Rules:

- unknown schema version fails closed;
- no implicit `v2 -> v3` coercion;
- a v2 result can never receive `PASS[HARDENED_V3]`;
- if migration is needed, use a separate deterministic migration command;
- migration must emit its own receipt binding input v2 digest, output v3 digest, and migration-ruleset version.

## P0.6 P0 required tests

- replay mode passes against the pinned committed receipt;
- replay mode passes without local `.olean` only with explicit `RECEIPT_REPLAY` semantics;
- live mode fails when `.olean` is absent;
- live mode fails when `.olean` bytes drift;
- live mode fails when dependency surface drifts;
- live mode fails on wrong Git HEAD;
- live mode fails on wrong toolchain;
- replay and live receipts expose different evidence-class/status labels;
- malformed receipt fails JSON Schema before mathematical evaluators run.
- duplicate JSON keys, BOM input, non-finite constants, and resource-limit
  violations fail before schema/evaluator dispatch;
- canonical receipt bytes are identical across two runs with identical admitted
  evidence;
- required execution errors produce `ERROR`/exit code `2` and cannot reuse a
  previous PASS output.

## P0.7 Promotion condition

P0 closes only when no receipt can be interpreted as stronger evidence than the mode that produced it, and only after strict JSON, version routing, receipt freshness, deterministic canonicalization, and provenance-envelope rules are all executable and covered by regression tests.

---

# P1 — Support Semantic Execution

Status target: `PASS[SUPPORT_SEMANTICS_ENFORCED]`

Importance: high

Difficulty: medium

## P1.1 Problem

The current Support evaluator checks ordering relative to a cutoff but does not fully execute the semantic assumptions named by the fixture. A negative cutoff or negative radial domain can pass if internal ordering remains consistent.

The string assumption `positive_cutoff` is not itself evidence.

## P1.2 Required runtime checks

Add fail-closed checks for:

- `cutoff > 0`;
- reject `bool` as numeric input;
- every radial bound is finite;
- every radial bound is `>= 0` unless the source-derived obligation explicitly allows signed coordinates;
- each interval has a non-empty `name`;
- interval names are unique;
- lower `<=` upper;
- ordered interval policy remains explicit.

Use a numeric helper that excludes Python booleans:

```text
is_real_number(x) := isinstance(x, (int, float)) and not isinstance(x, bool)
```

## P1.3 Boundary-policy contract

Do not guess whether source regions must be contiguous.

Add an explicit policy field, for example:

```json
"boundary_policy": {
  "allow_gaps": true,
  "allow_touching": true,
  "endpoint_convention": "CLOSED_CONTROL_INTERVALS"
}
```

For the pilot manufactured fixture, choose only the policy actually intended by that fixture.

For future source-derived Support obligations, populate this field from the source theorem/definition rather than reusing the pilot setting automatically.

## P1.4 Required tests

Must FAIL:

- `cutoff = -1`;
- `cutoff = 0`;
- negative lower bound;
- negative upper bound;
- `True` as cutoff;
- `False` as bound;
- missing interval name;
- duplicate interval name;
- reversed interval;
- non-finite bound;
- policy violation for the configured boundary policy.

Must PASS:

- the v2 pilot remains valid only through `HISTORICAL_V2_REPLAY`;
- the v3 pilot is a separately migrated fixture with all v3-required fields;
- declared allowed touching boundaries if policy permits them;
- declared allowed gaps if policy permits them.

## P1.5 Evidence label

Retain:

`PASS[MANUFACTURED_SUPPORT_FIXTURE]`

Do not rename the result to a source theorem reproduction until the evaluator inputs are source-derived.

---

# P2 — Cone Soundness

Status target: `PASS[CONE_SEMANTICS_ENFORCED]`

Importance: critical

Difficulty: medium-high

## P2.1 Problem

A negative `minimum_margin` weakens the inequality requirement and can allow an actually violated inequality to pass. Python booleans are also subclasses of `int` and therefore can be admitted by broad numeric checks.

The current threshold dependency graph checks shape, cycles, and dangling references, but does not yet execute positivity or value-order semantics of the thresholds.

## P2.2 Required inequality checks

For every inequality:

- relation is exactly `LE` or `GE`;
- `lhs`, `rhs`, and `minimum_margin` are finite real numbers excluding booleans;
- `minimum_margin >= 0`;
- calculated margin must be `>= minimum_margin`;
- label must be non-empty;
- labels must be unique.

Invalid relation or invalid numeric type must fail before margin computation.

## P2.3 Threshold values

Extend the evaluator contract with explicit values:

```json
"threshold_values": {
  "R_inner": "2",
  "R_outer": "5"
}
```

Threshold values in exact custody fields MUST use strict rational strings. A
sampled numerical threshold is a different field and MUST carry an explicit
tolerance contract. Binary floats are forbidden in custody/exact fields.

Required checks:

- every dependency graph node has a threshold value;
- no threshold value key exists outside the declared graph unless explicitly allowed;
- all thresholds required positive by the obligation are `> 0`;
- booleans rejected;
- dependency semantics are declared.

## P2.4 Dependency edge semantics

A graph edge is currently structural only. Add explicit meaning, for example:

```json
"dependency_relation": "STRICTLY_GREATER_THAN_DEPENDENCIES"
```

Then execute it:

```text
R_outer depends on R_inner
⇒ R_outer > R_inner
```

If another source theorem uses a different dependency meaning, use a different enum; do not infer semantics from graph direction alone.

## P2.5 Exact numeric representation

Numeric representation is a mandatory contract rule, not a preference.

```text
custody / exact fields
  strict rational string only

sampled numerical fields
  JSON number plus explicit tolerance contract
```

Exact rational strings use the same strict lexical discipline as P3 and are converted to exact arithmetic only after lexical validation. Binary float is forbidden in custody/exact fields.

Resource limits are mandatory for exact arithmetic:

- maximum numerator digits;
- maximum denominator digits;
- maximum number of identities/inequalities where exact values are used;
- maximum number of exact terms per identity/control.

These limits are part of fail-closed parsing and prevent unbounded integer/rational resource exhaustion.

## P2.6 Required tests

Must FAIL:

- violated LE plus negative margin;
- violated GE plus negative margin;
- `minimum_margin < 0` even if inequality otherwise holds;
- `True` / `False` in lhs, rhs, margin, or threshold values;
- zero/negative threshold when positivity is required;
- missing threshold value;
- extra undeclared threshold key if disallowed;
- dependency order violation;
- duplicate inequality label;
- malformed rational/decimal representation.

Must PASS:

- current manufactured Cone fixture after explicit threshold values are added;
- valid DAG and valid declared threshold ordering.

## P2.7 Evidence label

Retain:

`PASS[PARAMETRIC_CONE_EVALUATOR]`

This remains a manufactured/parametric control, not a numerical evaluation of `CleanOutgoingCone`.

---

# P3 — Exact Moment Soundness

Status target: `PASS[STRICT_EXACT_ARITHMETIC]`

Importance: high

Difficulty: medium

## P3.1 Problem

An empty term list currently sums to exact zero and can therefore satisfy an identity with expected value zero. Python booleans may also be accepted as integers by permissive parsing.

The label `EXACT_SYMBOLIC` is also too broad for a manufactured arithmetic control.

## P3.2 Strict rational grammar

Define accepted lexical forms explicitly.

Recommended grammar:

```text
INTEGER  := -?(0|[1-9][0-9]*)
RATIONAL := INTEGER | INTEGER '/' POSITIVE_INTEGER
```

Rules:

- reject whitespace-dependent ambiguity after normalization policy is chosen;
- reject floats;
- reject booleans;
- reject denominator zero;
- require denominator `> 0` in canonical input;
- optionally normalize sign to numerator only;
- reject `+1`, `01`, `1/-2`, `1/0`, scientific notation unless deliberately supported.

Python `Fraction` may remain the evaluation backend, but only after lexical validation.

## P3.3 Identity structure

Require:

- non-empty identity list;
- each identity has a non-empty unique `label`;
- `terms` has at least one item;
- expected value matches strict rational grammar;
- every term matches strict rational grammar.

Empty sum is not an admitted witness.

## P3.4 Evidence classes

Replace broad pilot classification:

`EXACT_SYMBOLIC`

with one of:

`MANUFACTURED_EXACT_CONTROL`

or

`EXACT_FIXTURE_ARITHMETIC`

Reserve a future class such as:

`SOURCE_DERIVED_EXACT_IDENTITY`

for identities whose coefficients and expected value are mechanically derived from the pinned source artifact.

## P3.5 Required tests

Must FAIL:

- `terms=[]`, expected `0`;
- `True` as term;
- `False` as expected;
- float term;
- denominator zero;
- negative denominator if canonical grammar forbids it;
- malformed rational string;
- missing label;
- duplicate label.

Must PASS:

- current `1/3 + (-1/3) = 0` manufactured control;
- current `1/4 + 3/4 = 1` manufactured control;
- negative rational values in canonical form.

## P3.6 Rust candidate

P3 is the preferred first Rust differential-verification target after Python v0.2.1 is GREEN because:

- semantics are small and stable;
- exact arithmetic is deterministic;
- test corpus can be language-neutral;
- Python `Fraction` and Rust rational arithmetic can be compared byte-for-byte at the result layer.

Rust is not required to close P3.

---

# P4 — Mutation Corpus Expansion

Status target: `PASS[ADVERSARIAL_CORPUS_BOUND]`

Importance: critical

Difficulty: high

## P4.1 Existing engine

The baseline-delta algorithm introduced in v2 is retained, but the expected detector is now stage-specific:

```text
new_failures = mutated_failures - baseline_failures
kill := required_primary_detector_for_exercised_stage ∈ new_failures
```

Allowed secondary detectors may also appear only when explicitly declared by the mutation oracle. No regression to `any FAIL => killed` is permitted.

## P4.2 Required mutation additions

Add at minimum:

1. `negative_cutoff`
2. `negative_radial_bound`
3. `negative_minimum_margin`
4. `boolean_as_numeric`
5. `empty_moment_terms`
6. `missing_live_olean`
7. `dependency_value_order_drift`
8. `schema_runtime_divergence`

Keep the existing six mutations.

Target bank size after patch: at least 14.

## P4.3 Staged mutation oracle

Schema-first rejection and family-level evaluator rejection are distinct stages. A mutation must therefore declare a staged oracle rather than a single undifferentiated detector.

Each corpus entry must declare at least:

```text
full_manifest_expected_detector
direct_evaluator_expected_detector
applicable_evidence_modes
allowed_secondary_detectors
```

Example:

```text
boolean_as_numeric
  full_manifest_expected_detector    -> manifest_schema
  direct_evaluator_expected_detector -> M4P-CONE-001:cone
  applicable_evidence_modes          -> RECEIPT_REPLAY, LIVE_ARTIFACT
  allowed_secondary_detectors        -> explicitly enumerated only

missing_live_olean
  LIVE_ARTIFACT   -> expected FAIL at compiled-live detector
  RECEIPT_REPLAY  -> NOT_APPLICABLE
```

Full-manifest tests prove that malformed data is rejected at the earliest authoritative stage. Direct-evaluator tests independently prove that family evaluators also reject the malformed value when exercised in isolation.

A mutation is accepted as killed only when the required primary detector for the exercised stage newly fails relative to baseline. Additional failures are allowed only if they are explicitly listed as `allowed_secondary_detectors`. An unrelated failure can never satisfy the oracle.

## P4.4 External golden corpus

Do not rely only on Python mutation functions.

Add language-neutral fixtures, for example:

```text
fixtures/mutations/m4p-v3/
  negative-cutoff.json
  negative-radial-bound.json
  negative-minimum-margin.json
  boolean-as-numeric.json
  empty-moment-terms.json
  missing-live-olean.json
  dependency-value-order-drift.json
  schema-runtime-divergence.json
  expected-results.json
```

`expected-results.json` records:

- mutation id;
- full-manifest expected detector;
- direct-evaluator expected detector;
- applicable evidence modes;
- allowed secondary detectors;
- expected gate result.

Python and any future Rust verifier consume the same corpus independently.

This reduces shared-implementation blind spots.

## P4.5 No-op control

Retain and expand the no-op mutation control:

- pre-existing baseline failure must not kill a no-op;
- unrelated new failure must not satisfy the wrong expected detector;
- reordered manifest obligations must not break mutation target selection.

Mutation selection should use obligation id/family, never list index.

## P4.6 P4 promotion condition

For every `applicable_evidence_mode`, each required corpus entry must fail by
its declared primary detector under both a clean baseline and a deliberately
contaminated baseline with unrelated failures. `NOT_APPLICABLE` entries are
neither killed nor survived and are excluded from the denominator. They cannot
satisfy a promotion gate.

---

# P5 — Full Gate and Release Promotion

Status target: `PASS[V0.2.1_EVIDENCE_INTEGRITY]`

## P5.1 Focused regression gate

Required focused tests include all new P0--P4 cases.

No release promotion if any reproduced false-PASS remains admissible.

## P5.2 Full Python gate

Required:

```text
pytest                    PASS
coverage >= 90%           PASS
ruff                      PASS
compileall                PASS
deterministic replay      PASS
JSON fixture syntax       PASS
schema validation         PASS
```

Test count is descriptive, not an authority signal.

## P5.3 Hosted CI

Required jobs:

1. cross-platform Python quality;
2. research custody replay;
3. pinned Lean scoped builds;
4. M4 v3 receipt replay gate;
5. M4 v3 same-run clean live-artifact gate inside the Lean job;
6. mutation golden-corpus gate;
7. canonical-status regeneration followed by `git diff --exit-code`.

The same release must prove both:

```text
PASS[COMPILED_RECEIPT_REPLAY]
PASS[COMPILED_LIVE_ARTIFACT_CI]
```

without conflating them. The live CI gate must build the target in that same hosted clean execution; a pre-existing artifact is insufficient.

## P5.4 Canonical status generation

Introduce one machine-readable canonical status artifact, for example:

`outputs/status-v0.2.1.json`

or a deterministic generator whose bounded output is committed under `docs/`.

README status, release notes, and stage receipt should derive from the same state model.

Avoid concurrent public states such as:

```text
OPEN[HARDENED_PILOT_GATE_PASS]
OPEN[PARAMETRIC_ONLY]
COMPLETED[PILOT_GATE]
```

without explicit dimension labels.

Recommended dimensions:

```text
implementation_status
hard_gate_status
research_lane_status
source_instance_status
semantic_equivalence_status
```

## P5.5 Historical documentation

Do not rewrite historical receipts silently.

Mark stale documents as:

`HISTORICAL SNAPSHOT — SUPERSEDED`

where appropriate, and point them to the current canonical status artifact.

At minimum review:

- `docs/CI_RECEIPT.md`
- `docs/FINAL_CHECKLIST.md`
- `docs/M3R_CLOSURE_RECOVERY_PLAN.md`
- `docs/stage_receipts/MATH_STAGE_M3.md`

## P5.6 Release status

Only after P0--P4 and hosted CI pass:

```text
M4-P fixed pilot fixture            PASS[SCOPED]
M4-P general manifest verifier      PASS[HARDENED_V3]
M4-P research lane                  OPEN[PARAMETRIC_ONLY]
M4-S                                HELD[NONCOMPUTABLE_SOURCE_INSTANCE]
Paper--Lean semantic equivalence    OPEN_RESEARCH_OBLIGATION
```

No source-derived Support/Cone/Moment theorem claim is created by this patch.

---

# 5. Rust Custody MVP — Post-v0.2.1, Optional

Rust remains a secondary implementation lane, not a replacement for Python/NumPy.

Recommended responsibility split:

```text
Python / NumPy
  mathematical exploration
  finite differences
  numerical integration
  external experiments

Lean
  formal statements
  theorem/dependency surface

Rust
  manifest and receipt validation
  path/hash custody
  strict rational control
  mutation result attribution
  differential verification against Python
```

Do not reimplement Lean declaration parsing in Rust as an independent string parser.

Preferred architecture:

```text
Lean environment/exporter
        ↓
canonical declaration metadata artifact
      ↙   ↘
 Python   Rust
 verifier verifier
```

Both implementations independently validate the same exported artifact.

First Rust milestone:

`P3 strict rational identity verifier + golden mutation corpus consumer`

Promotion criterion:

Python and Rust produce identical normalized verdicts for every admitted and rejected exact-arithmetic fixture.

---

# 6. Explicit non-goals

This patch must not expand into unrelated work.

Not part of v0.2.1:

- full CFD solver development;
- Rust rewrite of NumPy research code;
- selected noncomputable witness reconstruction;
- proof of `CleanOutgoingCone`;
- full paper--Lean semantic equivalence;
- whole-library Lean build as a prerequisite when scoped targets are sufficient;
- independent Navier--Stokes theorem claim;
- source-derived M4 analytic closure.

The patch repairs verifier authority. It does not create new mathematical authority.

---

# 7. Patch order and dependency graph

```text
P0 contract v3 / replay-vs-live
  ├── receipt schema
  ├── lean_receipt.py
  └── schema/runtime convergence
          ↓
P1 Support semantic checks
          ↓
P2 Cone semantic checks
          ↓
P3 strict exact moments
          ↓
P4 external mutation corpus
          ↓
P5 full CI / canonical status / release
          ↓
optional Rust custody MVP
```

P1--P3 can be implemented in parallel after the v3 contract shape is fixed.

P4 must be finalized after P1--P3 detector ids and failure semantics are stable.

Rust starts only after Python gate semantics are frozen for the chosen custody surface.

---

# 8. Definition of Done

`v0.2.1` evidence-integrity closure requires all of the following:

- [x] Required contract amendments are incorporated and implementation is
  authorized under the current P0--P4 and README scope.
- [ ] Replay and live compiled evidence are distinct contract modes.
- [ ] `LIVE_ARTIFACT` PASS is issued only when the target is actually rebuilt in the same clean execution.
- [ ] Hosted clean CI is the only release-authoritative source of `PASS[COMPILED_LIVE_ARTIFACT_CI]`.
- [ ] Existing artifact inspection is labeled `LOCAL_ARTIFACT_INSPECTION`, not live evidence.
- [ ] Live mode fails when current `.olean` is missing.
- [ ] Duplicate JSON keys and non-finite JSON constants are rejected before schema/evaluator dispatch.
- [ ] Strict JSON resource limits cover bytes, nesting depth, object members, and array length.
- [ ] Raw input digest and canonical semantic-object digest are distinct and documented.
- [ ] v2 is historical replay only and can never be promoted to `PASS[HARDENED_V3]`.
- [ ] Unknown schema versions fail closed; migration requires a deterministic migration receipt.
- [ ] Structured compiled receipt has its own enforced schema.
- [ ] CI receipt generation uses project code, not duplicated YAML logic.
- [ ] JSON Schema and Python validator accept/reject the same golden contract corpus.
- [ ] Negative/zero Support cutoff fails as specified.
- [ ] Negative radial bounds fail where the declared domain is radial/nonnegative.
- [ ] Booleans are rejected from all numeric custody fields.
- [ ] Cone minimum margin cannot be negative.
- [ ] Threshold positivity is executable, not prose-only.
- [ ] Threshold dependency value ordering is checked under an explicit relation.
- [ ] Empty moment terms fail.
- [ ] Exact rational input uses strict grammar and custody/exact fields forbid binary float.
- [ ] Exact arithmetic enforces explicit numerator/denominator/term-count resource limits.
- [ ] Moment labels are present and unique.
- [ ] Mutation corpus records full-manifest and direct-evaluator detector oracles, applicable evidence modes, and allowed secondary detectors.
- [ ] `missing_live_olean` is FAIL in live mode and NOT_APPLICABLE in replay mode.
- [ ] Receipt publication is atomic and a failed run cannot leave an earlier PASS appearing current.
- [ ] Identical admitted evidence produces byte-identical canonical receipts.
- [ ] Run-specific CI identity is stored in a separate provenance envelope bound to the canonical receipt digest.
- [ ] Dependency-surface canonicalization is explicitly OS-independent.
- [ ] Canonical status regeneration is checked with `git diff --exit-code`.
- [ ] Public receipts contain no absolute local paths, usernames, tokens, credentials, or machine-private environment dumps.
- [ ] Textual Lean locators are labeled `TEXTUAL_PINNED_SOURCE_LOCATOR` and are never promoted to semantic proof binding.
- [ ] Pilot exact-arithmetic evidence class is no broader than manufactured control.
- [ ] Mutation bank contains the eight new false-PASS mutations plus the existing six.
- [ ] Every mutation is killed by the required primary detector for the exercised stage; only explicitly allowed secondary detectors may co-fail.
- [ ] Mutation target selection is id/family based, not index based.
- [ ] External pre-mutated golden corpus is consumed by Python CI.
- [ ] Fixed v2 pilot remains reproducible as historical compatibility evidence.
- [ ] v3 pilot passes both replay and hosted live-artifact gates.
- [ ] README/release/stage status derives from one canonical state model.
- [ ] Historical documents are labeled rather than silently rewritten.
- [ ] M4-S remains HELD.
- [ ] Paper--Lean semantic equivalence remains open.
- [ ] No global Navier--Stokes theorem claim is promoted.

## Final release boundary

A successful `v0.2.1` means:

> the currently known verifier false-PASS surfaces are closed and the distinction between replayed evidence, live artifacts, manufactured controls, and source-derived claims is executable.

It does **not** mean:

> the M4 analytic obligations, selected source witness, OpenAI paper, Lean formalization, or Navier--Stokes millennium problem have been independently verified.

The contribution is custody: the verifier must make its own limits inspectable and must fail when those limits are crossed.

## Public positioning amendment

NSRW is presented publicly as a governance-oriented lab workbench: it supplies
reproducible source checks, bounded mathematical controls, and explicit
guardrails around Navier--Stokes research. It is not presented as an AI theorem
prover, CFD solver, neural-operator training system, or completed independent
solution program.

The README must use plain-language labels for evidence traceability, scope
records, manufactured controls, and the optional secondary structural check.
Future mathematical, numerical, CFD, and SciML lanes remain research directions and
must not be described as current proof authority.

The contract amendments have been re-reviewed and implementation is authorized
for the bounded P0--P4 and README scope. Release promotion still requires the
full P5 gate and must not be inferred from implementation completion alone.

A hardened verifier must not merely reject bad mathematics. It must also reject ambiguous evidence authority.
