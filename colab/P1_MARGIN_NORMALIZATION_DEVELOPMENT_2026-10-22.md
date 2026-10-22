# P1-03 — exact normalization and plateau-bound development experiment

Reviewed **2026-10-22 (Asia/Bangkok)**. Run identifiers and Drive folders use
their UTC start date, 2026-10-21. This is not a commit-bound admission receipt.

```yaml
check_status: PASS[LOCAL_PROOF_COMPILE:P1_MARGIN_NORMALIZATION]
artifact_check: PASS[DRIVE_ARCHIVE_INTERNAL_CROSSCHECK:P1_NORMALIZATION]
task_status: COMPLETED for P1-03 development implementation, compile and preservation
claim_authority: NONE
claim_status: UNVERIFIED
commit_bound_replay: NOT_PERFORMED
independent_attestation: false
d_archive_copy_verified: false
```

## Exact surface

New module: `formal/p2/P2_ZPLUS_J_MarginNormalization.lean`.
Single import: `P2_ZPLUS_J_QuantitativeMargin`.

Let `ell = exp(-23/20)`, `v = exp(-17/20)`, `L = c.pulseLength`,
`a0 = c.exponents 0 = -(1/2 + c.lam)`, and `beta0 = 1/2 - c.lam`.
The new `normalizedSecondBumpMoment c` is initially a whole-line weighted
bump integral; the second theorem below identifies it with the requested
interval integral over `ell..v`. It uses the **actual source cutoff**, not
a replacement bump or sampled surrogate.

Six public statements were printed and development-compiled:

| Declaration in `NSRW.P2` | Exact role |
| --- | --- |
| `firstRepair_weightGap_exp_eq` | `Delta = exp(-13 + 23*lam/20) * (exp(17*lam/10) - 1)` |
| `normalizedSecondBumpMoment_eq_interval` | Whole-line normalized moment equals the integral over `ell..v` |
| `secondBumpWeightedMoment_eq_normalized` | `I01 = exp(L * beta0) * mu01` |
| `normalizedSecondBumpMoment_eq_rowMoment` | `mu01 = exp(-beta0) * rowMoment(a0)` |
| `normalizedSecondBumpMoment_ge_plateau` | `(v - ell)/4 <= mu01` |
| `angularMoment_ge_plateau_margin` | Under the original same-`F,eta,r`, first-window, exact mass-zero and `c1>0` hypotheses, `K1*c1*(exp(L*beta0)*(v-ell)/4)*Delta <= localAngularMoment F eta r` |

The plateau proof integrates the constant lower bound 1 on
`[(ell+v)/2-(v-ell)/8, (ell+v)/2+(v-ell)/8]`. It uses the source
`cutoff_one_of_abs_le`, positive bases below 1 and the nonpositive exponent,
then nonnegative interval-integral monotonicity. Positivity of `v-ell` follows
from the fixed exponential endpoints; no quadrature is used.

All six success-run axiom sets were exactly
`[propext, Classical.choice, Quot.sound]`. The successful target stdout contains
no `sorryAx`, error, or warning. These are exact-real statements, not a verified
floating-point `expm1`, interval implementation, numerical lower bound for q,
explicit Profile, or discharged `combinedScale` hypothesis.

## Failed first attempt and minimal retry

Both attempts compiled the source and all earlier external modules afresh:

```text
source +NavierStokes.OutgoingProfile
 -> fresh Z01 -> fresh Z02 -> fresh conditional Z+J
 -> fresh QuantitativeMargin -> fresh MarginNormalization
```

First run: `nsrw-p1-normalization-20261021T173532560914Z`.

- Proof SHA-256: `ed3a1286d98dd56d2f1dc4c306d24d5fa1c188223093c4ba43c5555af6451d7b`.
- First five stages exited 0; the new module exited 1.
- Errors at original lines 87 and 92: `No goals to be solved`. The preceding
  `congr 1` had already completed each elementary exponential equality.
- Failure output also reported unnecessary-sequence linter warnings. Compiler
  recovery printed `sorryAx` for affected declarations; **this failed run was
  rejected**, not used as proof evidence or merged with success logs.
- Minimal repair removed the two redundant `ring` calls and changed four
  unnecessary `<;> ring` sequences to ordinary next-step `ring`. No theorem
  hypothesis, conclusion, definition, imported proof or runner changed.
- A small exact failed-input copy is retained under
  `colab/evidence/2026-10-22/p1-normalization-failed-20261021T173532560914Z/`.
  This is not a local copy of the original evidence ZIP.

Fresh retry: `nsrw-p1-normalization-20261021T174119519906Z`.

- Final proof SHA-256: `058ad35fca4228ea29773cef7c118dce7414745451f7f20361ca159d9a68ab8b`.
- **6/6** stages exited 0; all six stderr streams were empty.
- **5** fresh external `.olean` artifacts were created in this retry.
- New `.olean` SHA-256:
  `f0dc7b951b92bf0c35fff96658c06ad06eef7d892cff74a44c247fb9a17944bd`.
- New module stdout: 2,205 bytes, SHA-256
  `84be9c1a4d9e236891ffdbaa464a83e88fa4508ee0070d5167f93952e4e7a880`.
- Execution driver `colab/p1-normalization-development.py` SHA-256:
  `ca2d5631eeb7da4c3be3bb3561bb78cb15c3bf7bbdb949a88200d2c217b29651`.

The original quantitative proof remained exactly
`7a504d7c9cde6d76f2d0e826572fbbebeae905166802adc3e7b0d9b844e534b6`.
The Z01/Z02/conditional-Z+J input hashes also matched the original P1 record.
The [earlier quantitative experiment](P1_QUANTITATIVE_MARGIN_DEVELOPMENT_2026-10-22.md)
and its ZIP were not changed.

## Source and artifact observations

- Source commit: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
- Manifest Git blob: `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`.
- Lean: `4.34.0-rc2`, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`.
- All 11 dependency revisions and clean tracked states were checked by the
  frozen source-identity helper. In the success run, source identity matched
  pre/post, and source target `.olean` SHA-256 stayed
  `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c`.
- The failed run stopped before post-compile identity checks; its metadata
  does not claim those checks completed.
- The pinned cache/source target were reused. This is not a complete cold
  Lean/mathlib rebuild. External artifacts were fresh per attempt; artifact
  hashes are run-specific, not a claim of cross-run binary determinism.
- No new installation, `lake update`, Windows Lean installation, or additional
  F1--C04 branch execution occurred.

## Private Drive preservation and reopened-archive review

Each original ZIP is in its own private directory:

`MyDrive/NSRW-evidence/2026-10-21/<run-id>/<run-id>-evidence.zip`.

| Run suffix | ZIP bytes | ZIP SHA-256 |
| --- | ---: | --- |
| `173532560914Z` (failed) | 390035 | `de024c3d36f16130f851f82f0a8fd7bfb0008b9a9624572a78612538f843d7f8` |
| `174119519906Z` (success) | 581793 | `22fe3abb685a73977f5e70434f8d273183a1c59485c8ef2ce60d46da640f3b52` |

The driver exclusively created each Drive copy, reopened it, and compared
size/SHA and CRC. A **separate review cell** then reopened both saved ZIPs
and rechecked member path safety/uniqueness, all seven input hashes, available
fresh artifact hashes, and the 12 stage log hashes/lengths in each run.
It checked the failure classification separately from success criteria.
The successful ZIP has 25 members; the failed ZIP has 24.

The success review also checked all six exits/stderr, five fresh artifacts,
pre/post identity and target artifact equality, six exact axiom sets, and the
absence of warnings/errors/`sorryAx` in target stdout. Both retain
`claim_authority: NONE / claim_status: UNVERIFIED`.

Each Drive directory contains `archive-review-2026-10-22.json`:

- Failed review SHA-256:
  `55adf1b6ded81baabe5ee79134a6c018424099f1a4a077687c00efe0434614e8`.
- Successful review SHA-256:
  `dd30f727176ca3bb1ffcb56e3292884409281baf19a06404e9ebd9e8f1350810`.
- Review timestamps: `2026-10-21T17:43:34.274813+00:00` and
  `2026-10-21T17:43:34.405325+00:00` (2026-10-22 Asia/Bangkok).

These are same-trust-domain archive checks, not independent reproduction or
D: ZIP verification. Full archives were not downloaded locally or published.

## Remaining boundary

P1-03 exact normalization/plateau development is complete. Before admission,
freeze exact quantitative and normalization bytes and perform only a separately
authorized commit-bound replay/review. P0 computability/admissibility, P2
directed interval arithmetic and q, the C01 coefficient-gap computational
implementation, and P3 witness certification remain open. No root finder,
uniqueness, pole, numerical epsilon, new receipt admission or Git operation
was introduced here.
