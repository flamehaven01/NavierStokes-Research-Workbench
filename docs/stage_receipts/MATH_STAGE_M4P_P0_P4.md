# M4-P P0--P4 Implementation Receipt

Date: `2026-09-10`

Task status: `HELD[TARGET_BUILDS/SPAR_IDENTITY]`

This receipt covers the first integrated implementation of the parametric M4
audit. It is not an M4 mathematical closure receipt and does not change M4-S.

## Phase status

| Phase | Implementation | Current gate |
|---|---|---|
| P0 contract and quantifier custody | `PASS[CODE/TEST]` | `HELD[SPAR_IDENTITY]` |
| P1 Support | `PASS[CODE/TEST/SOURCE_BINDING]` | `PASS[SCOPED:OutgoingDilation]` |
| P2 Cone | `PASS[CODE/TEST]` | `HELD[COMPILED_TARGET_MISSING]` |
| P3 Moment | `PASS[CODE/TEST]` | `HELD[COMPILED_TARGET_MISSING]` |
| P4 mutations | `PASS[6/6_KILLED]` | Does not override P2/P3 holds |

`PASS[CODE/TEST]` means the bounded evaluator and its negative tests execute as
designed. It is not evidence that the paper's analytic obligation is true.

## Implemented surfaces

- versioned M4 obligation JSON schema and pilot manifest;
- source and executable quantifier prefixes;
- evidence-class, claim-scope, and constructibility custody;
- target-specific compiled receipt mapping;
- ordered Support interval and cutoff checks;
- Cone inequality margins and threshold dependency-cycle checks;
- exact-rational Moment cancellation and normalization checks;
- six deterministic claim/evidence mutations;
- SPAR `ReviewRuntime` adapter with a separate NSRW hard gate;
- fail-closed CLI and deterministic held receipt;
- CI contract/mutation replay.

## Verification

- `PASS[FOCUSED]`: 24 M4 tests passed.
- `PASS[FULL]`: 175 tests passed.
- `PASS[COVERAGE]`: 94.43%, above the 90% gate.
- `PASS[RUFF]`: `python -m ruff check src tests`.
- `PASS[COMPILE]`: `python -m compileall -q src`.
- `PASS[REPLAY]`: two source-bound M4 receipts were byte-identical.
- `PASS[MUTATIONS]`: 6/6 required mutations killed.
- `PASS[SOURCE_BYTES]`: pinned commit and four obligation locators/hashes matched.
- `PASS[SLOP:M4_CHANGED_RUNTIME]`: zero pattern findings in `m4_audit.py` and
  `m4_cli.py` after refactoring.
- `PASS[SLOP:COVERAGE]`: 25 runtime Python files analyzed.
- `UNAVAILABLE[SLOP:ML]`: no compatible ML model artifact configured.
- `OBSERVED[SLOP:PREEXISTING]`: the repository scan remains `clean`, but one
  unrelated E2 module has one high and one low structural finding.

## Remaining hard gates

1. `+NavierStokes.OutgoingCone` lacks a target-specific compiled receipt and
   `.olean` artifact in the current build directory.
2. `+NavierStokes.NominalConeAssembly` lacks a target-specific compiled receipt
   and `.olean` artifact in the current build directory.
3. Lean/Lake executables were not present on the current process `PATH`, so the
   two missing target builds were not attempted in this run.
4. SPAR imported source reports `0.6.0`, while editable distribution metadata
   reports `0.1.4`; SPAR admission remains held until identity is consistent.

The actual M4 command therefore returned exit code `1` with
`check_status=FAIL`, `task_status=HELD`. This is expected fail-closed behavior,
not a failed unit-test suite.

## Artifact digests

```text
m4_audit.py
  913897C998BB176F05C31B69BDAC27B4A92B54250281F5AA5FB522A192D821A1
m4_cli.py
  D72B83FA8DD6D57D2B5A45D18572BFBFB2FB37F20EC3CDA0422FEB6D977FE535
m4-obligation-manifest-v1.schema.json
  88728D4CD65A8CF123BFDF30F87ADC4F5A550564A41C980A50838CA05965AE65
m4-parametric-pilot-v1.json
  8DC81EE9C9FE16D0FB2576704291A4244398FD9AEC01661ADADA28ED5FCBDBC0
m4-parametric-pilot-receipt.json
  E68E0A968FE9262BD6BB14D2B0BB26AB3C6065A0C6DE937B2697D67C8488D923
m4-slop-report.json
  360DA0AC48927E3D99C47A0E3120B515DA713640E4018AE751B071583291F1C3
```

## Claim boundary

```text
M3 engineering                         CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY
M4-P implementation                    IN_PROGRESS[P0-P4]
M4-P authoritative gate                HELD[TARGET_BUILDS/SPAR_IDENTITY]
M4-S selected source instance          HELD[NONCOMPUTABLE_SOURCE_INSTANCE]
Paper--Lean full semantic equivalence  OPEN_RESEARCH_OBLIGATION
Millennium-problem solution            NOT_ESTABLISHED
```
