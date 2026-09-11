# M4-P verifier hardening

Historical authority: `V0.2.0_SCOPED_SNAPSHOT`

This document preserves the v0.2.0 result as recorded. It is not the current
v0.2.2 verifier or release status; later integrity plans and receipts supersede
its operational authority without rewriting this record.

Date: `2026-09-11`

Task status: `COMPLETED[LOCAL_AND_SOURCE_BOUND]`

This record captures a verifier-of-the-verifier review. It does not establish
any Navier--Stokes theorem, paper--Lean equivalence, or selected source witness.

## Reproduced findings

The pre-hardening verifier admitted all four of these counterexamples:

1. invented but internally matching `source_quantifiers` passed because no
   declaration signature or ordered source fragment was checked;
2. a compiled target with only `check_status=PASS` passed without opening a
   receipt;
3. a no-op mutation was reported killed when an unrelated baseline target was
   already failing;
4. an unknown Cone relation with a negative margin and a dependency on an
   undeclared node could pass.

The hosted Lean target builds themselves were valid scoped build evidence. The
defects were in how the Python gate described and consumed that evidence.

## Implemented closure

- Added contract and pilot fixture v2 while retaining v1 unchanged.
- Bound every obligation to the normalized source declaration signature hash
  and ordered source fragments under
  `NAMED_BINDERS_AND_DATA_EXISTENTIALS`.
- Canonicalized source-file hash input from CRLF to LF so the same pinned Git
  source has one locator identity on Windows and Linux.
- Reclassified P1--P3 as manufactured or sampled evaluator controls rather
  than source-theorem reproductions.
- Added a deterministic structured Lean build receipt and required every
  target PASS to bind its path and SHA-256.
- Cross-checked source commit, toolchain, target, exit code, expected `.olean`
  path and hash, and dependency-surface hash.
- Changed mutation verdicts to require the expected detector in
  `mutated_failures - baseline_failures`.
- Restricted Cone relations to `LE`/`GE` and rejected malformed, cyclic, and
  dangling threshold dependencies.
- Extended CI to regenerate the structured receipt from fresh scoped builds,
  compare it byte-for-byte, and execute the required source-bound M4 checks.

## Current scoped result

```text
P0 source signature custody       PASS[4/4]
P1 support control                PASS[MANUFACTURED_SUPPORT_FIXTURE]
P2 cone control                   PASS[PARAMETRIC_CONE_EVALUATOR]
P3 moment control                 PASS[EXACT_FIXTURE_ARITHMETIC]
P4 mutations                      PASS[6/6_BASELINE_DELTA]
compiled receipt binding          PASS[3/3]
M4-P required pilot checks        PASS[SCOPED]
M4-P analytic research lane       OPEN
M4-S selected source instance     HELD[NONCOMPUTABLE_SOURCE_INSTANCE]
paper--Lean semantic equivalence  UNVERIFIED
```

The quantifier binding is deliberately narrower than a Lean parser: it binds a
whole normalized declaration signature and verifies an ordered projection of
named binders and data existentials. Anonymous proof arguments and full
semantic equivalence remain outside this check.

Source-locator `sha256` values are hashes of source bytes after the single
portable transform CRLF to LF. This preserves every non-line-ending byte while
avoiding checkout-policy drift between Windows and Linux.

The local editable structural-check dependency still reports source `0.6.0`
with distribution metadata `0.1.4`. The pinned hosted installation is the
admitted dependency identity; local drift remains an explicit
non-authoritative diagnostic.

The initial hosted hardening run exposed the platform-bound source hash and
failed closed after all Python/custody jobs passed. The LF-canonicalization
patch was then validated against both a Windows CRLF checkout and raw LF Git
blobs before the replacement hosted run.
