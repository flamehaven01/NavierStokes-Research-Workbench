# M4-P P0--P4 Implementation Receipt

Date: `2026-09-10`

Task status: `COMPLETED[PILOT_GATE]`

This receipt covers the first integrated implementation of the parametric M4
audit. It is not an M4 mathematical closure receipt and does not change M4-S.

## Phase status

| Phase | Implementation | Current gate |
|---|---|---|
| P0 contract and quantifier custody | `PASS[CODE/TEST]` | `PASS[HOSTED_SPAR_PIN]` |
| P1 Support | `PASS[CODE/TEST/SOURCE_BINDING]` | `PASS[SCOPED:OutgoingDilation]` |
| P2 Cone | `PASS[CODE/TEST]` | `PASS[SCOPED:OutgoingCone]` |
| P3 Moment | `PASS[CODE/TEST]` | `PASS[SCOPED:NominalConeAssembly]` |
| P4 mutations | `PASS[6/6_KILLED]` | Critical mutations all rejected |

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
- `PASS[COVERAGE]`: 94.44%, above the 90% gate.
- `PASS[RUFF]`: `python -m ruff check .`.
- `PASS[COMPILE]`: `python -m compileall -q src tests`.
- `PASS[REPLAY]`: two source-bound M4 receipts were byte-identical.
- `PASS[MUTATIONS]`: 6/6 required mutations killed.
- `PASS[SOURCE_BYTES]`: pinned commit and four obligation locators/hashes matched.
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

The combined target-hash receipt has SHA-256
`C5989003C8C7621C51329B03CA4D257A2DAF62F4332961362D3987D937AD2D03`.
This closes the target-specific compilation gate only. It does not close
paper--Lean semantic equivalence or the full M4 analytic research lane.

## Artifact digests

```text
m4_audit.py
  E573556C6062C4C1DD15ADFBCDDC8DA7B50F736200DA2C4C9273E3BD88264C55
m4_cli.py
  D72B83FA8DD6D57D2B5A45D18572BFBFB2FB37F20EC3CDA0422FEB6D977FE535
m4-obligation-manifest-v1.schema.json
  88728D4CD65A8CF123BFDF30F87ADC4F5A550564A41C980A50838CA05965AE65
m4-parametric-pilot-v1.json
  B25EB45CC381005609D77890D3C520813BF78A461C82CEDF7596A84FD7C4EBE6
m4-parametric-pilot-receipt.json
  E6A90913EEA3EE6AF832BE4DBC3C873A18D542620CD20F4EA5FDE88DDC66E856
public-release-slop-report-2.json
  730A9346D69F31D8A1B0409DF5D52DE9FB661B69FEC4A704A838E6753EC21137
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
