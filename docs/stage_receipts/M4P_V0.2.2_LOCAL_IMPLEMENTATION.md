# M4-P v0.2.2 local implementation receipt

Date: `2026-09-11`

Base rollback commit: `5434400e9f91ac0892bdca257e7c90e50b32eb35`

Task status: `COMPLETED[LOCAL_IMPLEMENTATION]`

Release status: `HELD[HOSTED_LIVE_LEAN_GATE_PENDING]`

Claim status: `UNVERIFIED[NAVIER_STOKES_THEOREM]`

## Implemented scope

- v3 replay pilot with explicit `TEXTUAL_PINNED_SOURCE_LOCATOR` authority;
- metadata-only migration receipt binding the historical v1 Lean receipt to the
  v3 replay shape without claiming a new execution;
- 14-case staged mutation corpus with full-manifest, direct-evaluator,
  evidence-mode, and allowed-secondary oracles;
- replay result: 13 applicable mutations killed, one live-only mutation marked
  `NOT_APPLICABLE`;
- strict JSON lexical depth and total-node limits;
- M3 build evidence based on actual subprocess execution and exit status;
- observed `.olean` discovery rather than a fixed Lake prefix in the live build
  producer;
- project-owned build, dependency normalization, atomic receipt publication,
  live-manifest generation, and run-specific provenance in
  `src/nsrw/lean_receipt.py`;
- CI inline receipt-construction code removed.

## Local verification

```text
pytest                         PASS[204]
coverage                       PASS[91.65% >= 90%]
ruff                           PASS
compileall                     PASS
git diff --check               PASS
v3 deterministic replay       PASS[BYTE_IDENTICAL]
v3 applicable mutations       PASS[13/13]
v3 live-only mutation          NOT_APPLICABLE[LOCAL_REPLAY]
```

The two deterministic v3 replay outputs share SHA-256:

`081DC50C19F6A958357E9A4267BAA481FA81477D396C01558F56E308B9933BF3`

## Code-quality heuristic scan

Rule-based scan using the project's configured heuristic tool:

```text
overall_status                 clean
weighted_deficit_score         0.578573085216451
files analyzed                 47
critical findings              0
changed runtime findings       0
ML scoring                     disabled
```

The whole-repository scan retains six heuristic findings across five files,
including two high findings outside the v0.2.2 runtime patch: pre-existing complexity in
`external_experiments/fno_dataset_audit.py`, and an intentional constant
manufactured test function in `tests/test_profile_closure.py`. They are not
silently represented as zero findings. ML cleanliness is not claimed.

## Key local identities

```text
v3 pilot
  C53438E871127EAD09CA47E8F7F19EF17897ECC4D88AEC8CCDD94F2FF125F847

14-case mutation corpus
  BF5D978352D453175357C8296472C3732A39436A9E151924FD39B1E121C39EF4

v3 replay receipt
  5754A71C14D11585F030A90225552232E2A920A9B75915E3347D176973DDAEEE

metadata-only migration receipt
  51EBE06258D9372485D715079FA39A41FDD9479C3DEA6C6C8F45D5203AD91DBC

Lean request input bytes
  7AE55647C60C53978B386D7469709056DEBF4850D93DBD79596E3FD5A39EC61A
```

## Remaining gate

No local test can promote the hosted live lane. v0.2.2 remains unreleased until
GitHub Actions executes the pinned clean Lean checkout, generates the live
receipt and provenance envelope in the same run, kills all 14 applicable live
mutations including `missing_live_olean`, and uploads the resulting artifacts.

This receipt does not establish a source numerical witness, paper--Lean
semantic equivalence, a new analytic theorem, or a Navier--Stokes solution.
