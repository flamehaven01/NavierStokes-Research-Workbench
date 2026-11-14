# MomentBound coefficient bounds — scoped replay receipt

```yaml
check_status: PASS[COMMIT_BOUND_EXTERNAL_MOMENTBOUND_REPLAY]
artifact_check: PASS[COLAB_ARCHIVE_CROSSCHECK_AND_PRIVATE_DRIVE_REOPEN]
statement_review: PASS[FOURTEEN_EXACT_LEAN_SIGNATURES]
receipt_acceptance: ACCEPTED
claim_status: CONFIRMED for exactly the fourteen named propositions below
task_status: COMPLETED for MB-05 scoped review
reviewed_on: 2026-11-13 (Asia/Bangkok)
operational_exposure: OE-2
shared_trust_domain: true
independent_attestation: false
independent_reproduction: false
```

This dated review admits the propositions listed below after comparing the
printed signatures against the committed Lean files. The original replay
metadata records `claim_authority: NONE` and `claim_status: UNVERIFIED`.

## Exact execution and archive

| Field | Identity |
| --- | --- |
| Proof checkpoint | `80325a2d999c7da6af49398aaf1fae83df024b95` |
| Execution checkpoint | `fb5ad6001f1637417efda6ef34f3b75c8266c059` |
| Upstream source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Dependency manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Toolchain and Lean commit | `leanprover/lean4:v4.34.0-rc2`, `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Replay | `mb05-replay-20261113T152825622234Z` |
| Execution UTC | `2026-11-13T15:32:21.824631+00:00` to `2026-11-13T15:41:39.780461+00:00` |
| Source target .olean SHA-256 | `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c` |
| ZIP bytes | 877,340 |
| ZIP SHA-256 | `4d474507418d5820f10b538f15cf87476c793384d10117c1e0abab9bc143d9e1` |

| Input | SHA-256 | Git blob SHA-1 |
| --- | --- | --- |
| [P2_CoefficientScaledBounds.lean](../../formal/p2/P2_CoefficientScaledBounds.lean) | `7b75a32b7c9ca3023a3e7dfb47389c07af0382c48e32db4caadd82cb1f7c9719` | `5af9c1ddc8ea5757f6a7e76fd80f416d47abe029` |
| [P2_CoefficientSourceBounds.lean](../../formal/p2/P2_CoefficientSourceBounds.lean) | `f2e04f957e37c16ba4428e18dd4640b7662fd66051d2796836464603839e8ccf` | `b26fbb1214a79702e3fdd04f7802374ffea1d6f8` |
| [run-momentbound-replay.py](../../scripts/run-momentbound-replay.py) | `01c98147d2ed2e8434948238edf455d263a5d8880c85eb7889d128de4cd3ca4c` | `6c0b173e22507fb2f0cefd356858be2d571d7080` |

The tracked-clean detached checkout came from the existing repository base
and a verified incremental Git bundle containing both checkpoints. The
pinned Mathlib cache was restored in Colab. Lake built the source target,
then Lean generated nine fresh external artifacts. All ten stages exited
zero with empty stderr. The two coefficient modules printed fourteen
signatures and fourteen axiom lists, each containing `propext`,
`Classical.choice` and `Quot.sound`. The logs contained no `sorryAx`.
SourceBounds emitted three stdout linter diagnostics at lines 81 and 136:
unnecessary sequence focus, unused `ring`, and unreachable tactic.

The Colab archive review checked the exact 41-member inventory, path
safety, ZIP CRCs, 11 committed inputs against Git, nine artifact hashes
and all 20 log sizes and hashes. The pre/post identities of NSRW and the
source matched, including the 11 dependency revisions and source target
digest. The private Drive copy was reopened from
`MyDrive/NSRW-evidence/2026-11-13/mb05-replay-20261113T152825622234Z/mb05-replay-20261113T152825622234Z-replay-evidence.zip`
and matched the Colab archive byte for byte. Execution and artifact review
were conducted within the same research session.

## Named propositions

The declarations below use the `NSRW.P2.` prefix. `c` has type `Parameters`
and, when `F : Profile` is given, `c = F.data.core`. The intrinsic conditions
of these source types apply throughout. Use `C_main = affineCoefficients c 0 1 1`,
`C_prefix = affineCoefficients c 1 0 1`, `c1 = actualSecondRepairCoefficient F eta`,
`s = mbCommonScale c`, `B = mbCoarseBound c eta`, `q* = mbQStar c eta`, and
`p = parameterPolynomial eta = eta * (1 + eta^2)`.

The explicit hypotheses are abbreviated as follows.

| Abbreviation | Hypothesis |
| --- | --- |
| `Hmain` | `s * (1 / (10000 * c.lam)) ≤ C_main` |
| `Hprefix` | `abs(C_prefix) ≤ s * (328 + 3099396717 / 2)` |
| `HA` | `9/10 < F.amp eta`, evaluated at the parameter in the conclusion |
| `HP`, `Hm` | `c.P = 1`, `c.m = 1`, respectively |
| `Hλ` | `c.lam = 1 / 1000000000000` |

For the prefix identity, write `R_i = exp(-(beta c i * center c 0)) * prefixCoefficient c i / rowMoment (c.exponents i)` and `D = exp(2 * beta c 0) - exp(2 * beta c 1)`.

| Declaration | Inputs and additional hypotheses | Exact scope |
| --- | --- | --- |
| `mb_normalizedMainMoment_zero_le_decay_one` | `c` | `normalizedMainMoment c 0 ≤ exp(-2 + 3 * c.lam) * normalizedMainMoment c 1` |
| `mb_prefix_one_eq_row_difference` | `c` | `C_prefix = (R_1 - R_0) / D` |
| `mbCommonScale_pos` | `c` | `0 < s` |
| `mb_actualSecondRepairCoefficient_eq` | `F`, `eta : Real` | `c1 = p * C_prefix + F.amp eta * C_main` |
| `mb_actualSecondRepairCoefficient_gt_qStar` | `F`, `eta`; `HA` | `q* < c1` |
| `mb_qStar_ge_scaled_coarse` | `c`, `eta`; `Hmain`, `Hprefix` | `s * B ≤ q*` |
| `mb_actualSecondRepairCoefficient_gt_scaled_coarse` | `F`, `eta`; `HA`, `Hmain`, `Hprefix` | `s * B < c1` |
| `mb_actualSecondRepairCoefficient_pos_of_scaled_coarse` | `F`, `eta`; `HA`, `Hmain`, `Hprefix`, `0 < B` | `0 < c1` |
| `mb_main_one_ge_coarse` | `c` | `Hmain` |
| `mb_prefix_one_abs_le_coarse` | `c`; `HP`, `Hm` | `Hprefix` |
| `mb_qStar_ge_source_coarse` | `c`, `eta`; `HP`, `Hm` | `s * B ≤ q*` |
| `mb_fixed_coarse_eq` | `c`; `Hλ`; `eta = 1 / 1048576` fixed in the conclusion | `B = 207522463005781740692370179 / 2305843009213693952` |
| `mb_fixed_coarse_pos` | `c`; `Hλ`; `eta = 1 / 1048576` fixed in the conclusion | `0 < B` |
| `mb_actualSecondRepairCoefficient_fixed_pos` | `F`; `HP`, `Hm`, `Hλ`, `HA` at `eta = 1 / 1048576` | `0 < actualSecondRepairCoefficient F (1 / 1048576)` |

The exact rational value is for `B`, and the lower bound for `q*` uses the
positive symbolic factor `s`. Applying the fixed-input positivity theorem to
an instance requires a source `Profile` that satisfies all four explicit
hypotheses, including its actual amplitude at the fixed input.

## Scope for subsequent computation

A numerical value of the symbolic factor or actual coefficient, existence
and admissibility of a source Profile at the fixed tuple, verification of the
amplitude hypothesis, a numerical J certificate, root location and application
utility are outside this admission. The [static correspondence review](../momentbound/MB05_CORRESPONDENCE_REVIEW_2026-11-13.md)
documents the exact rational arithmetic and the historical development runs.
