# P1 quantitative J-margin — development compile and private preservation

Reviewed: **2026-10-22 (Asia/Bangkok)**. The execution run identifier uses its
UTC start date, 2026-10-21. This is a development execution record, not a
commit-bound receipt or independent attestation.

```yaml
check_status: PASS[LOCAL_PROOF_COMPILE:P2_ZPLUS_J_QUANTITATIVE_MARGIN]
artifact_check: PASS[DRIVE_ARCHIVE_CROSSCHECK:P1_QUANTITATIVE_MARGIN]
task_status: COMPLETED for the approved restoration, development compile and preservation
claim_authority: NONE
claim_status: UNVERIFIED
independent_attestation: false
commit_bound_replay: NOT_PERFORMED
d_archive_copy_verified: false
```

## Mathematical surface actually observed

The compiler printed these four statements and their axiom surfaces:

1. `NSRW.P2.secondBump_massTail_eq_full`: a first-window radius's second-bump
   mass tail equals the full second-bump weighted moment `I01`.
2. `NSRW.P2.firstRepair_weightGap_pos`: `Delta = upper(0)^(-lam) -
   lower(1)^(-lam) > 0`.
3. `NSRW.P2.angularMoment_ge_firstRepair_margin`: for the **same** source
   `Profile F`, `eta`, and `r`, under `lower(0) < r < upper(0)`, exact
   `localMass F eta r = 0`, and `localSecondRepairCoefficient F eta > 0`,
   `K1 * c1 * I01 * Delta <= localAngularMoment F eta r`.
4. `NSRW.P2.firstRepair_margin_pos`: `0 < K1 * c1 * I01 * Delta` under
   `c1 > 0`, without requiring a selected radius or a mass-zero hypothesis.

Here `K1 = momentScale F.data.core 1 * shape eta ^ 2`; all factors belong to
the same `F` and `eta`. The lower bound contains no chosen zero's radius. This
is a conditional exact bound, **not** a computed numerical lower bound.

All four actual `#print axioms` outputs were exactly the set
`[propext, Classical.choice, Quot.sound]`; `sorryAx` was absent.

No positive-eta assumption, C04 epsilon, amplitude-bound hypothesis, numerical
Profile, uniqueness, simple zero, pole, or source-facing `Profile.J` wrapper
was added to this module. Those are not admitted by this execution.

## Execution and exact identities

Run: `nsrw-p1-quantitative-margin-20261021T150804248528Z`.

```text
pinned source +NavierStokes.OutgoingProfile
  -> fresh Z01
  -> fresh Z02
  -> fresh conditional Z+J
  -> fresh QuantitativeMargin
```

All **12** restoration/build/compile stages exited zero. The source build and
four external Lean compilations each had empty stderr. Restoration commands
also exited zero but some emitted ordinary installation/cache progress to
stderr; the empty-stderr statement is limited to the five compile stages.

- Source commit: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
- Manifest Git blob: `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`.
- Manifest raw SHA-256: `5ec1dc8e009008d0efb9601cd38f6ba54e753fd538b0e5f8c3e6c5ec72ee1e09`.
- Toolchain: `leanprover/lean4:v4.34.0-rc2`, Lean commit
  `6a10ac8c22beadecabdbb0919c2b50214762f91d`.
- All **11** manifest dependency revisions matched; source and dependency
  tracked trees were clean. Pre/post source identity was equal.
- `OutgoingProfile.olean` pre/post SHA-256:
  `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c`.

The pinned dependency cache was downloaded and reused. This was not a complete
cold rebuild of Lean/mathlib. All four external proof artifacts were newly
created in this run, not reused from previous experiments.

| Executed input | Raw SHA-256 |
| --- | --- |
| `P2_Z01_LocalMassIdentities.lean` | `ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267` |
| `P2_Z02_BoundaryMassSigns.lean` | `7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c` |
| `P2_ZPLUS_J_FirstRepairAngularMoment.lean` | `2af3c68a73530a97421b3bd971bae5e63bbfb60c1abb7f40361d6d347e875d4a` |
| `P2_ZPLUS_J_QuantitativeMargin.lean` | `7a504d7c9cde6d76f2d0e826572fbbebeae905166802adc3e7b0d9b844e534b6` |
| `p1-quantitative-margin-experiment.py` | `7e8b5fea7847ea0ee2825991eb5c97344d761cef5a9b60f5723c021263197fd6` |
| `run-c02-development.py` (source-identity helper only) | `540f0aadd7add25bc0cfae2d852009e68c23cb13537ec03c4e5bce1ba085a278` |

The helper's portable Git blob was checked as
`518de06530c4c7c56edafdf571e5fb2ef0f808b3`; raw executor bytes are recorded
separately above. The helper's C02 compile function was not executed.

Fresh quantitative module `.olean` SHA-256:
`df1c689ecb54a782d5c5dec41d070f7a8df26d14564f77ec6cc90e10a87e1b75`.
Its stdout SHA-256:
`77222577888f3f8f40d30a16cc54bebb55d5ed1529b747f6a906bbeeef27da8c`.
Its stderr was zero bytes (SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

## Preserved archive and verification route

Original ZIP: `nsrw-p1-quantitative-margin-20261021T150804248528Z-evidence.zip`.

- Size: **396,511 bytes**.
- SHA-256: `2b4d5e11b3f5c9fc7972c4ba0902c432eba2eb474109a72a84a40f0aa1dd1171`.
- Private destination:
  `MyDrive/NSRW-evidence/2026-10-21/nsrw-p1-quantitative-margin-20261021T150804248528Z/`.
- Companion: `preservation-review.json`, SHA-256
  `b79fa7f5b74450f31810425563672707e306aa63b261a25f914efcbe11df47c9`.
- Verification timestamp: `2026-10-21T17:04:15.449283+00:00`
  (2026-10-22 in Asia/Bangkok).

After copying with exclusive creation, a separate review cell **reopened the
Drive ZIP**, compared its size/SHA, tested CRC and member paths/uniqueness, and
verified the metadata's hashes of six inputs, four fresh artifacts and all 24
stage stdout/stderr logs. The archive has **36** members. It also rechecked
the five compile-stage exits/stderr, source identity equality, target artifact
equality, four axiom surfaces, and `NONE / UNVERIFIED` metadata.

This is a separate verification code path in the **same trust domain**, not
independent Lean reproduction. The original ZIP was not rewritten. No full
archive was downloaded to D:, and no D: archive cross-check is claimed. This
small record transcribes the observed results; the original metadata/logs and
proof artifacts remain in the private archive.

## Next boundary

P1-02 is development-complete. Review of the positive product and independence
from the chosen zero is supported by the observed statements. Stable-gap and
normalized-integral identities, the amplitude-bound corollary, and numerical
admissibility remain separate work. P0 computability and P2/P3 evaluation or
certification have not been closed by this compile.

If commit-bound admission is requested, freeze these exact proof bytes and
authorize a separate checkpoint/replay/review step. No commit/push, new dated
authority receipt, public upload, release, or claim promotion occurred here.

Later the same Bangkok date, exact normalization and the conservative plateau
bound were implemented/development-compiled separately; see the
[P1-03 follow-up record](P1_MARGIN_NORMALIZATION_DEVELOPMENT_2026-10-22.md).
This earlier run's proof bytes, metadata and original ZIP remain unchanged.
