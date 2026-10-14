# P2 Z+J Colab execution receipt — 2026-10-12

```text
check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_Z_REPLAY]
artifact_check: PASS[LOCAL_ARCHIVE_CROSSCHECK:Z_PHASE_REPLAY]
claim_status: CONFIRMED for the named conditional and same-point M/J propositions only
task_status: COMPLETED for Z+J replay evidence and same-trust-domain receipt review
reviewed_on: 2026-10-12 (Asia/Bangkok)
independent_attestation: false
shared_execution: same run as the separate Z-core receipt; not independent evidence
```

## Confirmed scope

The [conditional module](../../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean)
proves:

```lean
NSRW.P2.angularMoment_pos_of_firstRepair_mass_zero (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) (hc1 : 0 < localSecondRepairCoefficient F eta) :
    0 < localAngularMoment F eta r
```

This applies to **every admissible first-window mass zero** with positive
second axial coefficient, not merely an IVT-selected witness. The conditional
theorem does not require `eta > 0`; it does require the explicit `hc1` hypothesis.

The [source-composition module](../../formal/p2/P2_ZPLUS_J_SourceComposition.lean)
also confirms `NSRW.P2.profileJ_pos_of_firstRepair_mass_zero`: with the same
strict first-window membership, source `F.M eta (exp(pulseStart)*r) = 0`,
and `actualSecondRepairCoefficient F eta > 0`, the source
`F.J eta (exp(pulseStart)*r)` is positive. Its final proposition is:

```lean
NSRW.P2.profileMJ_firstRepair_zero_small_positive (F : Profile) :
  ∃ epsilon : ℝ, 0 < epsilon ∧
    ∀ eta : ℝ, 0 < eta → eta < epsilon →
      ∃ r : ℝ, F.data.core.lower 0 < r ∧ r < F.data.core.upper 0 ∧
        F.M eta (Real.exp F.data.core.pulseStart * r) = 0 ∧
        0 < F.J eta (Real.exp F.data.core.pulseStart * r)
```

For every fixed source `Profile F`, a Profile-dependent epsilon exists such
that every positive eta below it has **one shared witness** r inside the first
repair window where the source mass is zero and source angular moment is
strictly positive. F, eta, r, and global radial coordinate X are identical in
the M and J clauses. This is not a conjunction of two unrelated existentials.
The epsilon is not uniform or computed; r can depend on eta.

`localAngularMoment_eq_profileJ` is the compiled coordinate bridge for `1 ≤ r`.
It applies `F.J_at_exp` with `pulseStart + log r ≥ 0` and rewrites the exponential.
The final theorem consumes one C04 epsilon, translates its actual coefficient
to the local alias, uses the Z03 conditional mass-zero theorem and then the
source J-positivity bridge at exactly that witness.

### Structural argument reviewed

Write `c = F.data.core`, `R = exp(c.pulseLength)`, and
`Tj = repairBumpTail c 0 j r`, `Sj = repairBumpTail c 1 j r`.
The source angular and mass moments are evaluated at `pulseStart + log r`;
their integral prefactors are positive but are not coordinate-conversion factors.

Endpoint cancellation and the future two-bump decomposition give
`c0*T0 + c1*T1 = 0`. The full second-bump mass tail is strictly positive;
`T0 ≥ 0` and `c1 > 0` force `T0 > 0` and `c0 < 0`.
The compiled explicit ordering is `upper(0) < lower(1)`. Using
`a1 = a0 - lambda` and positive-base real powers yields
`upper(0)^(-lambda)*T0 ≤ S0` and `S1 ≤ lower(1)^(-lambda)*T1`.
Multiplication by negative c0 reverses the first inequality. Thus
`c0*S0 + c1*S1 < 0`; the negative angular-tail prefactor makes local J positive.
No pointwise first-bump positivity at the zero is inferred from `T0 > 0`.
No numerical margin theorem is admitted.

**Not admitted:** common/numerical epsilon; a numerical or certified root;
all-positive-eta or negative-eta sign classification; uniqueness; first-zero;
simple-zero/derivative/monotonicity claims; a numerical J-margin; a Q pole,
limit or boundedness theorem; paper–Lean equivalence; upstream theorem
verification; independent novelty/reproduction; an application/CFD solver;
or a Navier–Stokes solution. In the study's ordinary real-ratio interpretation,
M=0 and J>0 obstruct division by M*H at that point. This receipt does not
formalize partial division, a Lean Q declaration, or any singularity type.

## Exact identity and shared execution

| Field | Identity |
| --- | --- |
| execution checkpoint | `3a50b5f50b034319a469b9de68f556be70fff02c` |
| proof-only checkpoint | `8581a511d4c60c52f8d37663fd49f70e4d835d64` |
| dependency extraction base | `10d5a1f517b8665137f2354746d70752f8ef67fd` |
| OpenAI source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| manifest committed Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Linux manifest raw SHA-256 | `5ec1dc8e009008d0efb9601cd38f6ba54e753fd538b0e5f8c3e6c5ec72ee1e09` |
| declared / observed Lean | `leanprover/lean4:v4.34.0-rc2` / `4.34.0-rc2` |
| observed Lean commit | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| observed Lake | `5.0.0-src+6a10ac8` |

| Input | Executor raw SHA-256 | Git blob SHA-1 |
| --- | --- | --- |
| `P2_ZPLUS_J_FirstRepairAngularMoment.lean` | `2af3c68a73530a97421b3bd971bae5e63bbfb60c1abb7f40361d6d347e875d4a` | `11ccd687f7157c7a1bb5529843344ce04373d7af` |
| `P2_ZPLUS_J_SourceComposition.lean` | `c3444fbe43c633ef1a0be0987cb42ab8264d4a92da81cf961ee647409c16bd89` | `759b0ad12ed646d56388bf9c1bd92485d702bf07` |
| `colab/run-zplus-j-composition-development.py` | `64eb25d0cc5d2c19463746d1843facf8620ee65c4e853b3eec8cb6b1d09950d9` | `6d1806c1eed0130de12b6658a1787a9a1c9cd9d3` |
| `scripts/run-p2-z-replay.py` | `1ad7f7f343aead480a9077034990fff992e5f5bc22d75df86e419ad89e64826c` | `22e17d57f7cd9651ba52a058ddb25b73c75bffe5` |

Run: `nsrw-z-phase-replay-20261012T065216884451Z`.
Wrapper UTC: `2026-10-12T06:52:18.527504+00:00` to
`2026-10-12T07:04:13.230328+00:00`.

```text
source / +NavierStokes.OutgoingProfile
 -> fresh F1 -> strict L2 -> L3 -> D -> C01 -> C02 -> C03 -> C04
 -> fresh Z01 -> Z02 -> Z03 -> Z04-core -> conditional Z+J -> source composition
```

The exact wrapper command and compilation pattern are recorded in the
[Z-core receipt](P2_Z_CORE_COLAB_2026-10-12.md). Both receipts reviewed this
same archive directly; neither inherits authority merely from the other's
status. All seventeen input bytes matched `git show` at the execution checkpoint.
All fifteen stages exited `0`, all stderr files empty, and fourteen external
artifacts were freshly generated. Source/NSRW/base identities matched pre/post;
all eleven pinned dependency revisions matched. Source caches were reused,
not independently attested or fully rebuilt from scratch.

| Record | SHA-256 |
| --- | --- |
| conditional Z+J stdout | `eb3ca8192eb186706bc200601045c0b772fc432470bf0701d22b5555df22a344` |
| source composition stdout | `2ec633bf076cb8eaf6783e33cc02b99b00af7b3c94aee2281c30579b5288f716` |
| all empty stderr files | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| fresh conditional Z+J `.olean` | `63d157dab34c2bd82a8845777581ba3a72ac2705e121389b4ff47a3513523c02` |
| fresh source composition `.olean` | `676672c7c62427e08f35d956663a6c83c7cc2f622693d8ce9a577629ca61db0b` |
| source `OutgoingProfile.olean`, observed unchanged pre/post | `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c` |
| original engine metadata | `bd5dfb97464d070cfe30fbe19343309ab38972af2d44848bc1dd85bfdb97b515` |
| original wrapper metadata | `ea9f8eda1a3603b40c954638b6c3bfc45154a0f376f7502e34356f178ac7a0e3` |

The twelve conditional-module and three source-composition `#print axioms`
results each matched `[propext, Classical.choice, Quot.sound]`; `sorryAx` was
absent. Together with four Z04 surfaces the shared run has nineteen inspected
named surfaces. The target sources contain no `sorry`, `admit`, or new axiom.
Conditional stdout retains one nonfatal linter warning at line 123 about
`tac1 <;> tac2` where `(tac1; tac2)` suffices. It was reviewed, not suppressed;
empty stderr does not mean warning-free compilation. This is an axiom-surface
observation, not a semantic audit of the imported library.

## Preservation and separate admission

Archive: `nsrw-z-phase-replay-20261012T065216884451Z-replay-evidence.zip`,
`815996` bytes, SHA-256
`bd109a6f0db1eaaa1e6054d5ba16f8e07696434f7ffebb5527128f721267d74b`.
Private Drive and the Git-ignored
`colab/evidence/2026-10-12/nsrw-z-phase-replay-20261012T065216884451Z/`
directory preserve the same bytes. No public evidence upload is implied.
The bounded D: verifier was rerun during this review and passed CRC/member
safety, 60 recorded internal hashes, log sizes/exits, fresh artifacts,
exact committed inputs, metadata linkage and pre/post identities. Current
target source bytes also matched the archived inputs. No Lean re-execution
or artifact modification occurred.

The source target `.olean` is only a pre/post executor observation, not an
archived authority artifact. Runtime metadata is not protected hosted
attestation. The engine's original development/uncommitted-label fields remain
unchanged; the outer wrapper separately establishes committed-input custody.
Both original metadata layers retain `claim_authority: NONE / claim_status:
UNVERIFIED`. This subsequent manual receipt review admits only the named
conditional and same-point propositions, not any metadata self-promotion.

Execution, preservation and review share an operator/trust domain. Separate
receipts are not independent executions or independent mathematical reviews.
The previous lost replay ZIP and failed Z+J archive remain disclosed historical
custody gaps; this new run is neither a reconstruction nor a mixture of old logs.
See [the current execution index](../../colab/Z_PHASE_REPLAY_2026-10-12.md).
No execution checkpoint, proof or runner was changed for admission.
No commit/push/tag/release, site deployment or Zenodo publication occurred.
