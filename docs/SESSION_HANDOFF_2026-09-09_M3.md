# Session Handoff — 2026-09-09 — M3 Review

Status: `M3_REVIEW_IN_PROGRESS__M4_HELD`

## 1. Research objective and claim boundary

This workbench is part of the Equation to Artifact track. The goal is not to claim a new Navier–Stokes proof. The goal is to preserve and inspect the checkable surface of the OpenAI paper/formalization track: source identity, exact formulas that can be isolated, executable diagnostics, formal-source locators, expected outputs, falsifiers, and the boundary of what remains unverified.

The theorem/result belongs to the original authors. The workbench currently targets the forced Clay alternatives (C)/(D). Unforced global regularity or blowup, a complete independent reproof, and paper–Lean semantic equivalence remain explicit non-claims.

The wider research program remains fourfold:

1. reproduce and audit the checkable numerical/formal surface of the OpenAI result;
2. map the surrounding mathematical research and proof architecture;
3. explore approaches materially different from the OpenAI construction;
4. investigate whether any stronger or independent bounded Navier–Stokes result can be developed without inflating the current evidence.

Claim-custody principle: the core computation is not the novelty claim. The contribution is the custody — isolating the exact checkable statement, reproducing it under a pinned environment, and making its failure boundary inspectable.

## 2. Pinned source boundary

Current contract records:

- primary PDF: `navier-stokes.pdf`, SHA-256 `0E779481C4DA40BD28D1E642E1D8CA57447D129610DF28DFA5A11E9AF8AE228F`;
- searchable Markdown transport: SHA-256 `B0AB289505D375DD99DA0F87219CD4C23B80F00B3E7003B6DA76F907008DB652`;
- OpenAI formal source: commit `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

Authority order remains: PDF = primary mathematical source; Markdown = lossy locator transport; Lean repository = formal source; workbench crosswalks/receipts = derived evidence.

## 3. Work completed before this review

### Software integrity stages

Implementation Stages I–IV previously reached `GREEN` within software scope: contract validation, fail-closed mutations, proof/evidence graph, deterministic pipeline receipts, and authority separation. This did not promote the theorem claim, which remains `UNVERIFIED`.

### Math M1

M1 implemented exact scaling algebra, similarity-coordinate reconstruction, differential operators, manufactured positive/negative controls, and bounded residual diagnostics. Exact rational scaling checks and local numerical diagnostics were separated by evidence class.

Recorded stage evidence: 80 cumulative tests, 93.33% coverage, deterministic math receipt SHA-256 `505913E2373B9B500F801D7B6335E2806AE6D486354426D9BEABEF9C7CD55DB2`.

### Math M2

M2 implemented the concentrating leading-field interface `(E,U,V0,Pi)`, exact affine-in-h exponent bookkeeping, local incompressibility and radial-pressure checks, stress-region/core diagnostics, and finite asymptotic falsifiers. The source paper profiles were deliberately not instantiated.

Recorded stage evidence: 115 cumulative tests, 94.74% coverage, deterministic M2 receipt SHA-256 `EBF7A786AD2A39E356A9D8A33AFA1111BA58C7C9A59CFC6C9EE619B10446A015`.

### Math M3 current implementation

M3 currently implements:

- equation (4.6) radial average with an axis extension;
- equation (4.7) derivation of `V0` from `U` and its radial average;
- equation (4.25) canonical pressure using a finite cutoff plus explicit tail contract;
- `ClosedLeadingProfiles`, preventing independent `V0`/`Pi` drift;
- static paper–Lean crosswalk and missing-link register;
- deterministic M3 closure receipt;
- negative tests for invalid quadrature, invalid domain inputs, and missing static Lean files.

Recorded M3 receipt: `outputs/m3-closure-receipt.json`, SHA-256 `92AF490C3ADCDEED0AA67BF4C632F8B29982D9C3562708F5EFD9DA76308B649E`, with `check_status=PASS` and `claim_status=UNVERIFIED`.

Historical M3 stage receipt records 129 tests and 93.91% coverage. This is retained as prior evidence, not treated as a fresh run on 2026-09-09.

## 4. Review order used today

The detailed review is intentionally performed in this order:

1. `README.md`
2. `docs/` and stage receipts
3. fixtures / receipts / CI boundary
4. runtime code
5. tests
6. fresh verifier execution where the current environment permits it

This order is intended to detect claim inflation and documentation drift before accepting code behavior.

## 5. README review

The README preserves the most important authority boundaries correctly:

- software pipeline GREEN is separated from theorem `UNVERIFIED`;
- Lean build is `UNAVAILABLE` rather than inferred from source presence;
- M1/M2/M3 diagnostics are explicitly bounded;
- manufactured profiles are not presented as source witnesses;
- forced (C)/(D) scope is separated from unforced global claims.

No blocking README claim inflation was found.

One freshness issue remains: README presents M3 as `PASS[LOCAL]`, while the current connected Python runtime cannot freshly rerun pytest because the `pytest` module is absent. The recorded M3 PASS is therefore a stored receipt/status, not a newly reproduced status in this session.

## 6. Docs review

The design documents maintain the intended layer separation well. Two historical documents can be misread as current global state:

- `docs/FINAL_CHECKLIST.md` records an earlier Stage-IV snapshot with 40 tests and six runtime Python files;
- `docs/CI_RECEIPT.md` records the M2-era 115-test state and deterministic replay through the analytic spine.

These are not false as historical receipts, but they should be labeled or superseded as snapshots before a public release so they are not confused with the current M3 state.

`docs/PROFILE_CLOSURE_M3_DESIGN.md` correctly holds Lean build and Theorem 4.6 semantic equivalence. The remaining open audit items ML-003 and ML-004 are still valid blockers against claim promotion.

## 7. Code review findings — M3 blockers before M4

### F-M3-001 — source parameter domain weakened in M3

Severity: `HIGH / BLOCK M4`

M1/M2 consistently enforce the source-inspected condition `0 < h < 1/100`. In `src/nsrw/math_kernel/profile_closure.py`, both `ClosedLeadingProfiles.__post_init__` and `derived_radial_flux` instead accept `0 < h < 1/2`.

This widens the executable contract beyond the currently cited source domain. A caller can therefore obtain an apparently valid M3 closure object for values that M1/M2 would reject.

Required repair:

- reuse `ConcentrationParameters` or an exact `Fraction`-bound parameter object in M3;
- enforce the same `0 < h < 1/100` source boundary;
- add negative tests at `h=1/100` and for values in `(1/100, 1/2)`;
- keep float conversion only at numerical evaluation boundaries.

### F-M3-002 — canonical-pressure integrand at X=0 is under-specified and numerically wrong for the current source-shaped fixture

Severity: `HIGH / BLOCK M4`

`canonical_pressure()` handles `radial_x == 0` by requiring `E(0,eta)=0` and then returning integrand value `0.0`.

For the source-shaped form `E=sqrt(2X)F`, however,

`E(X,eta)^2 / (2X) -> F(0,eta)^2`

as `X -> 0`, which is generally finite but not generally zero. For the current manufactured swirl `E=sqrt(2X) exp(-X)`, the limiting integrand is `1`, not `0`.

The existing tests integrate from positive `X=0.75`, so this axis-endpoint defect is not exercised.

Required repair options:

- provide an explicit source-authorized axis-limit callback for `E^2/(2X)`; or
- represent the source factor `F` directly and derive the axis limit from it; or
- fail closed at `X=0` until the limit is explicitly supplied.

Do not silently substitute zero.

Add an analytic regression test for canonical pressure evaluated from `X=0` using the manufactured exponential swirl.

## 8. Additional M3 hardening items

### F-M3-003 — M3 deterministic replay is not yet in GitHub Actions

Severity: `MEDIUM-HIGH`

The CI quality job runs the complete pytest suite, but the `deterministic-replay` job currently replays only the contract pipeline, M1 math receipt, and M2 analytic receipt. It does not execute and byte-compare the M3 closure receipt.

Before M4, add two M3 receipt runs and a byte-comparison assertion.

### F-M3-004 — static Lean locator audit uses substring matching

Severity: `MEDIUM`

`audit_lean_crosswalk()` checks markers using `marker in text`. This can theoretically match comments or non-declaration text. Since this evidence is already labeled static-only, it does not create a proof claim, but the locator should still be hardened with declaration-aware regex or a parsed/formal query when the Lean toolchain becomes available.

### F-M3-005 — eta endpoint closure is not executable with the current centered derivative

Severity: `MEDIUM / DOCUMENT BOUNDARY`

`_validate_point()` accepts `eta` in `[-1,1]`, but `parameter_derivative_of_average()` requires a centered step that stays inside that interval. Consequently `derived_radial_flux()` cannot evaluate at the endpoints `eta=±1` with the current method.

This may be acceptable as a bounded interior diagnostic, but the executable domain should be stated explicitly. If Theorem 4.6 obligations require endpoint control, use a source-justified analytic or one-sided treatment rather than silently extrapolating.

### F-M3-006 — pressure-tail contract is supplied, not verified

Severity: `MEDIUM / BOUNDARY`

The finite cutoff plus `pressure_tail(eta)` design is preferable to silently truncating infinity. However, the current callable is trusted input: M3 does not verify that the supplied tail equals the actual integral from the cutoff to infinity.

For manufactured fixtures this is acceptable and should remain labeled diagnostic. For any source-profile instantiation, tail validation must become a separate obligation or exact/analytic witness.

## 9. Fresh verifier status on 2026-09-09

Workspace: `<local-workspace>/NavierStokes-Research-Workbench`

Git status before this handoff write:

- branch: `main`;
- repository has no commits yet;
- tracked diff: empty.

Fresh pytest attempt:

- interpreter resolved to a local Python 3.14 executable;
- execution failed before collection with `No module named pytest`;
- therefore no fresh test PASS/FAIL result exists for this session.

This does not invalidate the stored M3 receipt. It means the 129-test PASS is prior evidence and must not be described as freshly reproduced today.

No dependency installation was authorized or performed during this review.

## 10. Tomorrow — exact M3 continuation order

Do not start M4 yet. Resume M3 in this order:

1. repair F-M3-001 by unifying the `h` contract with M1/M2 (`0<h<1/100`, preferably exact `Fraction` custody);
2. repair F-M3-002 by making the `X=0` pressure-integrand limit explicit and fail-closed;
3. add boundary/falsification tests for the new `h` and axis-pressure cases;
4. decide and document the executable `eta` endpoint policy;
5. harden static Lean declaration matching;
6. add M3 deterministic receipt replay to CI;
7. restore/use an authorized dev environment containing pytest/ruff and rerun the full suite, coverage gate, Ruff, compile check, and M3 deterministic replay;
8. regenerate/update the M3 stage receipt only from that fresh run;
9. review ML-003 and ML-004 again;
10. only then decide whether the M3 gate is GREEN enough to enter M4.

## 11. M4 entry boundary

M4 remains `HELD` until the M3 source-domain and axis-pressure defects are repaired and freshly tested.

When M4 begins, it should consume the closed profile bundle and move narrowly toward stress support, cone, and moment obligations. A passing M4 diagnostic still must not be promoted to Theorem 4.6 existence, full paper–Lean equivalence, or a global Navier–Stokes proof.

## 12. Public-language boundary

Preferred description:

> We reproduce the checkable surface of selected Navier–Stokes claims and profile identities under an explicit computational contract. The workbench records source custody, numerical/formal diagnostics, falsifiers, and unresolved bridges. It is not a new proof, and the global theorem claim remains unverified.

The boundary is intentional. A strong artifact is not strong because it claims more; it is strong because its assumptions, commands, expected outputs, and failure modes are inspectable.
