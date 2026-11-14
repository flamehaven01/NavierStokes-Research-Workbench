# MomentBound normalized angular-moment bound

```yaml
check_status: PASS[COMMIT_BOUND_EXTERNAL_MB06_NORMALIZED_J_REPLAY]
artifact_check: PASS[COLAB_ARCHIVE_CROSSCHECK_AND_PRIVATE_DRIVE_REOPEN]
statement_review: PASS[FOUR_EXACT_LEAN_SIGNATURES]
receipt_acceptance: ACCEPTED
claim_status: CONFIRMED for exactly the four named propositions below
task_status: COMPLETED for MB-06 scoped replay and review
reviewed_on: 2026-11-13 (Asia/Bangkok)
operational_exposure: OE-2
shared_trust_domain: true
independent_attestation: false
independent_reproduction: false
```

This dated review compared the committed [Lean module](../../formal/p2/P2_MB06_NormalizedJ.lean)
with the four signatures printed during the replay. The archived execution
metadata records `claim_authority: NONE` and `claim_status: UNVERIFIED`.

## Admitted propositions

All names carry the `NSRW.P2.` prefix. For `c : Parameters`, let
`lambda = c.lam`, `s = mbCommonScale c`, `I01 = mbSecondBumpMass c`,
`Delta = mbFirstRepairWeightGap c`, and `A_i = rowMoment (c.exponents i)`.
Write `R(lambda) = (exp(17*lambda/10)-1)/(exp(2*lambda)-1)` for
`mbRepairRatio c.lam`. For the last row, `c = F.data.core`,
`B = mbCoarseBound c eta`, and `K1 = momentScale c 1 * shape eta^2`.

| Declaration | Inputs and hypotheses | Conclusion |
| --- | --- | --- |
| `mbRepairRatio_pos` | `c : Parameters` | `0 < R(lambda)` |
| `mb_scale_mul_secondBump_mul_weightGap` | `c : Parameters` | `s*I01*Delta = (A_0/A_1)*exp(3*lambda/20)*R(lambda)` |
| `mb_repairRatio_le_scale_mul_secondBump_mul_weightGap` | `c : Parameters` | `R(lambda) ≤ s*I01*Delta` |
| `mb_normalizedAngularMoment_gt_coarse_mul_ratio` | `F : Profile`, `eta r : Real`, `c.P = 1`, `c.m = 1`, `9/10 < F.amp eta`, `0 < B`, `c.lower 0 < r`, `r < c.upper 0`, `localMass F eta r = 0` | `0 < B*R(lambda)` and `B*R(lambda) < localAngularMoment F eta r / K1` |

The first three propositions use the conditions carried by `Parameters`.
The last proposition uses the same `F, eta, r` for the amplitude, exact mass
zero and angular moment. Its printed signature quantifies over real eta
subject to the stated conditions.

## Execution and preservation

| Field | Identity |
| --- | --- |
| Proof checkpoint | `42932fc256473e12acd912e6e1b032a2de2d0c00` |
| Execution checkpoint | `40e0cfe7c2defeeeee871f1923552c352f28ee5c` |
| Proof SHA-256 | `e326e79968d7bd9fcba7f7ac0d220b0db50a18a641b901cd0ddf8c05dcd76648` |
| Proof Git blob | `a3990853ab8e3ef70ab47aa592d88941123b47c3` |
| Runner SHA-256 | `773ee0dea2a2cd8fb6d03b9e71011f2f8b58d0c24230b93c377ea724cc4b95ea` |
| Upstream source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Lean toolchain and commit | `leanprover/lean4:v4.34.0-rc2`, `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Source target .olean SHA-256 | `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c` |
| Replay | `mb06-replay-20261113T164610223735Z` |
| Execution UTC | `2026-11-13T16:46:11.750369+00:00` to `2026-11-13T16:48:13.827049+00:00` |
| ZIP size | 1,636,335 bytes |
| ZIP SHA-256 | `cc5fbbdde35ffbd153564ca5c698b3f98652710555136ad84e6a9819969c6a86` |

The detached NSRW checkout was clean and used the exact execution commit
imported by Git bundle. The replay reused the pinned Colab source cache and
compiled 15 fresh external modules. All 16 stages, including the source
target, exited zero with empty stderr. The four target declarations each
reported `propext`, `Classical.choice` and `Quot.sound`. The logs contained
no `sorryAx`. NSRW and source identities matched before and after execution,
including the source dependency revisions and source target digest.

The private Drive copy was reopened at
`MyDrive/NSRW-evidence/2026-11-13/mb06-replay-20261113T164610223735Z/mb06-replay-20261113T164610223735Z-replay-evidence.zip`.
Review checked its whole-file digest, ZIP CRCs, exact 65-member inventory,
17 inputs against committed bytes, 15 artifact hashes and 32 log hashes and
sizes. Execution and review used the same Colab trust domain. The earlier
development run with a post-compile audit error has its own
[development record](../momentbound/MB06_NORMALIZED_J_DEVELOPMENT_2026-11-13.md).

## Scope for application

The receipt establishes an exact-real conditional lower bound. Applying it to
the fixed numerical tuple still requires a source Profile satisfying the
amplitude hypothesis and an exact mass zero in the specified window.
The [factor enclosure](../momentbound/MB06_NORMALIZED_J_FACTOR_REVIEW_2026-11-13.md)
covers the scalar expression `B*R(lambda)`. An instantiated numerical
angular-moment certificate and application utility remain open.
