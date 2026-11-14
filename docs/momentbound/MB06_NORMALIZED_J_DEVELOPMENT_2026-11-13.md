# MomentBound MB-06 normalized angular-moment proof

13 November 2026 (Asia/Bangkok).

The module [P2_MB06_NormalizedJ.lean](../../formal/p2/P2_MB06_NormalizedJ.lean)
uses the MB-05 coefficient estimates and the P1 quantitative moment bound.
It derives four exact-real propositions:

| Declaration | Scope |
| --- | --- |
| `mbRepairRatio_pos` | The ratio of exponential differences is positive for the positive lambda carried by the source parameters. |
| `mb_scale_mul_secondBump_mul_weightGap` | The product of the coefficient scale, full second bump mass moment, and weight gap equals the row-moment ratio times `exp(3*lambda/20)*R(lambda)`. |
| `mb_repairRatio_le_scale_mul_secondBump_mul_weightGap` | The L3 row-moment comparison bounds that product below by `R(lambda)`. |
| `mb_normalizedAngularMoment_gt_coarse_mul_ratio` | For the same source Profile and parameter, with `P=m=1`, amplitude greater than 9/10, positive coarse bound and exact mass zero strictly inside the first repair window, `0 < B_coarse*R(lambda) < localAngularMoment/K1`. |

The exact product identity cancels the large exponentials before any
evaluation. The final inequality is strict because the actual coefficient
strictly exceeds the scaled coarse bound and the other factors are positive.
The [factor review](MB06_NORMALIZED_J_FACTOR_REVIEW_2026-11-13.md) records
the exact-rational enclosure of `B_coarse*R(lambda)` at the fixed tuple.
Application to a source instance requires the Profile, its amplitude
hypothesis and the exact mass zero in the stated window.

## Development execution

The development inputs use the admitted dependency bytes from NSRW commit
`fb5ad6001f1637417efda6ef34f3b75c8266c059`. They include the new local module.
The executor pins source `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, its
manifest and dependency revisions, and Lean `4.34.0-rc2`.

The first run `mb06-development-20261113T161934752635Z` compiled all 16
stages with empty stderr and printed the four declarations and their standard
axioms. The development runner then stopped with an assertion during its
post-compile audit, so the original run is recorded as `ERROR[MB06_DEVELOPMENT]`.
The archive was reopened from private Drive, with 64 members and SHA-256
`701704465ae5a971e5164b9fc661e2f44a79f5f0d29afdd9e4648b712527989c`
(1,630,469 bytes). The retry adds explicit audit diagnostics and removes
redundant tactics in the new proof while preserving the declarations.

The retry `mb06-development-20261113T162429652537Z` finished with
`PASS[LOCAL_PROOF_COMPILE:MB06_NORMALIZED_J]`. All 16 stages exited zero
with empty stderr. The new module printed the four signatures above, each
with `Classical.choice`, `Quot.sound` and `propext`. Its output contained
no linter diagnostics or `sorryAx`. Source, dependency and toolchain
identity matched before and after, and the source target digest remained
stable across the external compile chain.

- Proof SHA-256: `e326e79968d7bd9fcba7f7ac0d220b0db50a18a641b901cd0ddf8c05dcd76648`.
- Retry ZIP SHA-256: `5ae29e1c89c23e21a8fd4512d3e98fa5b96a67aae8330a52a0b9ce2b45cb046a`.
- Retry ZIP: 1,629,725 bytes, 64 members.
- Private storage: `MyDrive/NSRW-evidence/2026-11-13/<run-id>/<run-id>-evidence.zip`.

Both Drive copies were reopened in the executing Colab session. Their ZIP
CRCs and recorded input, artifact and log digests matched. The fixed-factor
JSON also passed local recomputation and all 20 focused tests passed.
Development metadata remains `claim_authority: NONE` and
`claim_status: UNVERIFIED`. The next formal step is to pin the successful
proof and runner, replay them at a clean execution commit, and review a
dated receipt for these four propositions.
