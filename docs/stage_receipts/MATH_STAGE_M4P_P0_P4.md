# M4-P P0--P4 Implementation Receipt

Date: `2026-09-10`

Task status: `COMPLETED[PILOT_GATE]`

This receipt covers the first integrated implementation of the parametric M4
audit. It is not an M4 mathematical closure receipt and does not change M4-S.

## Phase status

| Phase | Implementation | Current gate |
|---|---|---|
| P0 contract and quantifier custody | `PASS[SOURCE_SIGNATURE_BOUND]` | Four declaration signatures and ordered fragment projections match |
| P1 Support | `PASS[MANUFACTURED_SUPPORT_FIXTURE]` | `PASS[SCOPED:OutgoingDilation]` |
| P2 Cone | `PASS[PARAMETRIC_CONE_EVALUATOR]` | `PASS[SCOPED:OutgoingCone]` |
| P3 Moment | `PASS[EXACT_FIXTURE_ARITHMETIC]` | `PASS[SCOPED:NominalConeAssembly]` |
| P4 mutations | `PASS[6/6_BASELINE_DELTA]` | Each expected detector is a new failure |

`PASS[CODE/TEST]` means the bounded evaluator and its negative tests execute as
designed. It is not evidence that the paper's analytic obligation is true.

## Implemented surfaces

- additive M4 obligation JSON schema v2 and pilot manifest; v1 is retained;
- normalized Lean signature hashes and ordered source-fragment projections;
- evidence-class, claim-scope, and constructibility custody;
- structured target-specific compiled receipt cross-verification;
- ordered Support interval and cutoff checks;
- Cone inequality margins and threshold dependency-cycle checks;
- exact-rational Moment cancellation and normalization checks;
- six deterministic claim/evidence mutations evaluated against baseline deltas;
- SPAR `ReviewRuntime` adapter with a separate NSRW hard gate;
- fail-closed CLI and deterministic held receipt;
- CI contract/mutation replay.

## Verification

- `PASS[FOCUSED]`: 31 M4 tests passed.
- `PASS[FULL]`: 182 tests passed.
- `PASS[COVERAGE]`: 94.27%, above the 90% gate.
- `PASS[RUFF]`: `python -m ruff check .`.
- `PASS[COMPILE]`: `python -m compileall -q src tests`.
- `PASS[REPLAY]`: two source-bound M4 receipts were byte-identical.
- `PASS[MUTATIONS]`: 6/6 expected detectors appeared only in the mutation delta.
- `PASS[SOURCE_BYTES]`: pinned commit and four obligation file hashes matched.
- `PASS[SOURCE_SIGNATURES]`: 4/4 normalized declaration signatures and ordered
  named-binder/data-existential fragments matched the pinned Lean source.
- `PASS[COMPILED_RECEIPTS]`: 3/3 targets matched the structured receipt across
  receipt hash, source commit, toolchain, target, exit code, `.olean`, and
  dependency-surface fields.
- `PASS[SLOP:M4_CHANGED_RUNTIME]`: zero pattern findings in `m4_audit.py` and
  `m4_cli.py` after refactoring.
- `PASS[SLOP:COVERAGE]`: 25 runtime Python files analyzed.
- `UNAVAILABLE[SLOP:ML]`: no compatible ML model artifact configured.
- `OBSERVED[SLOP:PREEXISTING]`: the repository scan remains `clean`, but one
  unrelated E2 module has one high and one low structural finding.

## Hosted compiled evidence

GitHub Actions run `34497647700` completed successfully against formal-source
commit `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`. The three scoped `.olean`
hashes are:

```text
OutgoingDilation.olean
  E47FA3AFCA76ED83021C1F030E4FE3ACE43586CA03341EA4B2CAF42A913F344D
OutgoingCone.olean
  DA5C2E0CC8C2932346945022706F01379314A8134504BD8A766069C7C03E67A4
NominalConeAssembly.olean
  1E7049B2B8A6BE3B802EE42C856A06DEE40F4331E14E161A495A8A9B6D515A3D
```

The original combined text target-hash receipt has SHA-256
`C5989003C8C7621C51329B03CA4D257A2DAF62F4332961362D3987D937AD2D03`.
The structured receipt consumed by contract v2 has SHA-256
`DD8B248947CAD63804788EC3063E3ED4B8E587BD6D4BFD7029A580B74333E073`.
CI regenerates the structured receipt from the compiled artifacts and requires
byte equality. This closes the scoped compilation evidence binding only; it
does not close paper--Lean semantic equivalence or the M4 analytic lane.

## Artifact digests

```text
m4_audit.py
  3B09D54F4DCF7136F2B2C7833619DDB53720FFAFE2BFDF44D7D1E3FAEC73AF9B
m4_cli.py
  6A0AF6F5036FFE9E1C3CCD2155B8A05FB680FC2A601D8C40A6AACA473CE3FE24
m4-obligation-manifest-v2.schema.json
  48440F1AD1F8B35B04A30A714CA855A884B7A010ED89EB199CB6312A5266E3FF
m4-parametric-pilot-v2.json
  3B0B74F9DDC86C79B36B4E58EC8EEAAAE9F1BE1124D2772668B129127CA763D9
lean-scoped-targets-v1.json
  DD8B248947CAD63804788EC3063E3ED4B8E587BD6D4BFD7029A580B74333E073
m4-parametric-pilot-v2-a.json
  C2771F39BF19A7362685359502B84EEF477BDDA3208012FF63A8E5E892718CBE
m4p-hardening-slop-report.json
  76C4B0C4584BC2E9A540B1C01942BC322683EAB87A1694B41B7379083AF9E1A9
```

## Claim boundary

```text
M3 engineering                         CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY
M4-P pilot implementation              COMPLETED[P0-P4]
M4-P pilot authoritative gate          PASS[SCOPED]
M4-P research lane                     OPEN
M4-S selected source instance          HELD[NONCOMPUTABLE_SOURCE_INSTANCE]
Paper--Lean full semantic equivalence  OPEN_RESEARCH_OBLIGATION
Millennium-problem solution            NOT_ESTABLISHED
```
