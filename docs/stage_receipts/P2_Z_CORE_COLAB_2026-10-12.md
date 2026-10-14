# P2 Z-core Colab execution receipt — 2026-10-12

```text
check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_Z_REPLAY]
artifact_check: PASS[LOCAL_ARCHIVE_CROSSCHECK:Z_PHASE_REPLAY]
claim_status: CONFIRMED for the named source-facing interior mass-zero proposition only
task_status: COMPLETED for Z-core replay evidence and same-trust-domain receipt review
reviewed_on: 2026-10-12 (Asia/Bangkok)
independent_attestation: false
```

## Confirmed scope

The [Z04-core module](../../formal/p2/P2_Z04_FirstRepairInteriorZero.lean)
proves the following proposition under the pinned source and toolchain:

```lean
NSRW.P2.profileM_firstRepair_zero_small_positive (F : Profile) :
  ∃ epsilon : ℝ, 0 < epsilon ∧
    ∀ eta : ℝ, 0 < eta → eta < epsilon →
      ∃ r : ℝ, F.data.core.lower 0 < r ∧ r < F.data.core.upper 0 ∧
        F.M eta (Real.exp F.data.core.pulseStart * r) = 0
```

For every fixed source `Profile F`, a Profile-dependent positive epsilon
exists such that every `0 < eta < epsilon` has a mass-history zero strictly
inside the first repair window. Here `r` is the pulse-local radial coordinate;
the source global radial coordinate is `X = exp(pulseStart) * r`.
The window index is first; the theorem does **not** say this is the first zero.
The witness can depend on eta, and the epsilon can depend on F.

The three other printed Z04 declarations are compiled supporting bridges:
`localSecondRepairCoefficient_eq_actual`,
`exists_firstRepair_zero_small_positive`, and `localMass_eq_profileM`.
The coefficient alias is definitional. The local existence theorem consumes
C04's positive neighborhood and Z03's conditional IVT theorem. The coordinate
bridge requires `1 ≤ r`: it obtains nonnegative global log coordinate
`pulseStart + log r`, applies source `F.M_at_exp`, and rewrites
`exp(pulseStart + log r) = exp(pulseStart) * r`. First-window membership supplies
`1 < r`. No extra `eta^2 ≤ 1` or small-lambda assumption is introduced.

Z01 supplies partial-mass and tail identities. Z02 supplies the strict lower
mass sign and conditional strict upper mass sign. Z03 uses continuity and IVT,
excluding both endpoints using their strict signs. These were freshly compiled
dependencies in this replay, not logs assembled from development runs.

**Not admitted by this receipt:** J positivity or M/J mismatch (reviewed
separately); a common epsilon over Profiles; a numerical epsilon or root;
positivity/zero behavior for all positive or negative eta; uniqueness; a first
zero; simple-zero or derivative claims; a Q pole/limit; full zero-set geometry;
paper–Lean equivalence; upstream theorem verification; independent novelty;
an application/CFD solver; or a Navier–Stokes solution.

## Committed inputs and environment

| Field | Identity |
| --- | --- |
| execution checkpoint | `3a50b5f50b034319a469b9de68f556be70fff02c` |
| six-proof checkpoint | `8581a511d4c60c52f8d37663fd49f70e4d835d64` |
| dependency extraction base | `10d5a1f517b8665137f2354746d70752f8ef67fd` |
| OpenAI source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| manifest committed Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| observed Linux manifest raw SHA-256 | `5ec1dc8e009008d0efb9601cd38f6ba54e753fd538b0e5f8c3e6c5ec72ee1e09` |
| declared / observed Lean | `leanprover/lean4:v4.34.0-rc2` / `4.34.0-rc2`, Linux x86_64 |
| observed Lean commit | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| observed Lake | `5.0.0-src+6a10ac8` |
| source / execution checkout / dependency base | clean, matching identities before and after execution |
| dependencies | all 11 manifest-pinned revisions matched before and after |

| Input | Executor raw SHA-256 | Git blob SHA-1 |
| --- | --- | --- |
| `P2_Z04_FirstRepairInteriorZero.lean` | `f3bce7c0a6d28922bd592d6dbfb5b0735a058ffc84c2100bc4328be1df5b2d5d` | `054eb77f015dd425b574b19b945d9f7e2aa9192f` |
| `colab/run-zplus-j-composition-development.py` | `64eb25d0cc5d2c19463746d1843facf8620ee65c4e853b3eec8cb6b1d09950d9` | `6d1806c1eed0130de12b6658a1787a9a1c9cd9d3` |
| `scripts/run-p2-z-replay.py` | `1ad7f7f343aead480a9077034990fff992e5f5bc22d75df86e419ad89e64826c` | `22e17d57f7cd9651ba52a058ddb25b73c75bffe5` |

All seventeen archived authority inputs were independently compared locally
against `git show 3a50b5f...:<input-path>` in this review. Their raw hashes and
Git blobs matched. Current local Z04, conditional Z+J and source-composition
proof bytes also match the archived inputs; no proof was modified for admission.
Git blobs are portable identities; raw SHA-256 describes executor bytes.

## One shared clean replay, separate claim reviews

Run: `nsrw-z-phase-replay-20261012T065216884451Z`.
Wrapper UTC: `2026-10-12T06:52:18.527504+00:00` to
`2026-10-12T07:04:13.230328+00:00`.

```text
source / +NavierStokes.OutgoingProfile
 -> fresh F1 -> strict L2 -> L3 -> D -> C01 -> C02 -> C03 -> C04
 -> fresh Z01 -> Z02 -> Z03 -> Z04-core -> conditional Z+J -> source composition
```

Command: `python3 scripts/run-p2-z-replay.py --source-root <pinned-source>
--nsrw-root <clean-execution-checkout> --dependency-base <clean-base>
--output-dir <new-run> --expected-nsrw-commit 3a50b5f50b034319a469b9de68f556be70fff02c`.
External compilation uses `lake env lean -R <run>/inputs
-o <run>/artifacts/<module>.olean <run>/inputs/<module>.lean` from the source
root, with the fresh dependency directory on the Lean search path.
Private exact paths/commands remain in the original metadata.

Fifteen stages exited `0`, all stderr files empty; fourteen external `.olean`
artifacts were fresh. The source build reported 2851 jobs. Source cache was
reused: this is not a cache-free full upstream-library rebuild or independent
cache-authenticity attestation. The larger shared run also supports the
[separate Z+J receipt](P2_ZPLUS_J_COLAB_2026-10-12.md), but J is not admitted here.

| Record | SHA-256 |
| --- | --- |
| source stdout | `ef4c85693bfe6f7939358cc63b4aa820fe200cc2e22ba26f748152a0d0778dbb` |
| Z01 stdout | `9644e7b42a7d342e8a683ecfa6e345ecf2752fee108b40296c5205e81296e6a1` |
| Z02 stdout | `df2c8f9f2a78ae28f30adbb42c67473092fc6e9e842135c6b4fa960049fc5bae` |
| Z03 stdout | `d5f323e36d0652ca1460926e466761e7cd400df629a7959bc415989700ff2bfd` |
| Z04 stdout | `b66dafbde5914269368052fb5c6b2348cf1d267e4d5892b3c8188bb74ef201e4` |
| all empty stderr files | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| fresh Z04 `.olean` | `88a8ce535b9c7d4a83807056ef1fc1f5abd2e8d6016d0f50c9824f71950cdf6d` |
| observed source `OutgoingProfile.olean`, unchanged pre/post | `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c` |
| original engine metadata | `bd5dfb97464d070cfe30fbe19343309ab38972af2d44848bc1dd85bfdb97b515` |
| original wrapper metadata | `ea9f8eda1a3603b40c954638b6c3bfc45154a0f376f7502e34356f178ac7a0e3` |

All four Z04 `#print axioms` results exactly matched
`[propext, Classical.choice, Quot.sound]`, with `sorryAx` absent. Across the
three final Z modules, nineteen printed surfaces matched. The reviewed target
sources contain no `sorry`, `admit`, or new axiom. This is axiom-surface and
placeholder observation, not a semantic audit of all imported proofs.
The conditional Z+J stdout contains one nonfatal unnecessary-sequence-focus
linter warning; it does not appear on stderr and was not suppressed or patched.

## Archive review and admission

Outer ZIP: `nsrw-z-phase-replay-20261012T065216884451Z-replay-evidence.zip`.
Bytes: `815996`. SHA-256:
`bd109a6f0db1eaaa1e6054d5ba16f8e07696434f7ffebb5527128f721267d74b`.

It is preserved in private Drive and the Git-ignored repository directory
`colab/evidence/2026-10-12/nsrw-z-phase-replay-20261012T065216884451Z/`.
Drive copy and D: bytes were size/hash crosschecked; no public sharing was enabled.
The existing bounded local verifier was rerun during this receipt review under
the D: virtual environment: CRC, safe/unique non-symlink members, 60 recorded
member hashes, stage exits/log sizes, fresh artifact hashes, exact committed
inputs, metadata linkage, pre/post identity and nineteen axiom surfaces passed.
No ZIP extraction or Lean re-execution was needed.

The source target `.olean` is not archived; its unchanged digest is an executor
observation. Runtime metadata is not independently protected hosted attestation.
The engine retains its original development/uncommitted-label fields; the outer
wrapper establishes the seventeen-input committed identity. Both original
metadata layers still have `claim_authority: NONE / claim_status: UNVERIFIED`.
This separate receipt review admits only the named source-facing mass-zero scope.

Execution, preservation and review share an operator/trust domain. There is no
independent attestation or external reproduction. The lost 2026-10-11 replay ZIP
and first failed Z+J archive remain separate disclosed custody gaps; this new
2026-10-12 archive is not a reconstruction and no old run fragments were reused.
See [the current execution index](../../colab/Z_PHASE_REPLAY_2026-10-12.md).

Receipt/document synchronization does not alter the execution checkpoint.
No Git commit/push, tag/release, Zenodo publication or site deployment is implied.
