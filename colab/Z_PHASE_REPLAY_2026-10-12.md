# Z-core / Z+J recovery replay — 2026-10-12

This session record is a custody index, not mathematical authority itself.

check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_Z_REPLAY]
artifact_check: PASS[LOCAL_ARCHIVE_CROSSCHECK:Z_PHASE_REPLAY]
preservation_check: PASS[DRIVE_COPY_CROSSCHECK:Z_PHASE_REPLAY]
task_status: COMPLETED for the approved restoration, single replay and preservation only
claim_authority: NONE
claim_status: UNVERIFIED
independent_attestation: false
receipt_review: COMPLETED on 2026-10-12 for separate Z-core and Z+J scopes

## Exact execution identity

| Input | Identity |
| --- | --- |
| execution checkpoint | `3a50b5f50b034319a469b9de68f556be70fff02c` |
| dependency extraction base | `10d5a1f517b8665137f2354746d70752f8ef67fd` |
| pinned OpenAI source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Linux manifest raw SHA-256 | `5ec1dc8e009008d0efb9601cd38f6ba54e753fd538b0e5f8c3e6c5ec72ee1e09` |
| observed Lean | `4.34.0-rc2`, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| observed Lake | `5.0.0-src+6a10ac8` |

Run: `nsrw-z-phase-replay-20261012T065216884451Z`.
Wrapper started UTC `2026-10-12T06:52:18.527504+00:00` and finished
`2026-10-12T07:04:13.230328+00:00`. Driver exit: `0`.

```text
pinned source / +NavierStokes.OutgoingProfile
 -> fresh F1 -> strict L2 -> L3 -> D -> C01 -> C02 -> C03 -> C04
 -> fresh Z01 -> Z02 -> Z03 -> Z04-core -> conditional Z+J -> source composition
```

All 15 stages exited `0`, with empty stderr. Fourteen external `.olean`
artifacts were freshly generated and seventeen committed inputs were checked.
Nineteen named Z axiom surfaces matched `propext`, `Classical.choice`,
`Quot.sound`; `sorryAx` was absent. Source/NSRW/base identities matched pre/post.
Source `OutgoingProfile.olean` remained unchanged, SHA-256
`444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c`.

The source build reported 2851 jobs and approximately 635 seconds. This is an
execution observation, not a performance benchmark. Upstream cache was reused;
this was not a full clean upstream-library rebuild. All external modules were fresh.

## Preservation and independent local archive check

Archive: `nsrw-z-phase-replay-20261012T065216884451Z-replay-evidence.zip`

- Bytes: `815996`
- SHA-256: `bd109a6f0db1eaaa1e6054d5ba16f8e07696434f7ffebb5527128f721267d74b`
- Private Drive copy: `MyDrive/NSRW-evidence/2026-10-12/`, exclusive creation;
  size/SHA crosscheck passed. Drive metadata reported `shared: false`.
- D: copy: privately preserved under `colab/evidence/2026-10-12/`; this original
  ZIP is not distributed and its hash is not a public download link.
  PowerShell size/SHA independently matched the Colab and Drive observations.

The existing `check-z-replay-archive.py` ran under the D: virtual environment
with this exact size, digest and checkpoint. It exited `0` and verified 60
internal member hashes, ZIP CRC/path safety, input/artifact/log identities,
15 stages, 14 fresh artifacts, 17 committed inputs and 19 axiom surfaces.
Both execution and archive metadata retain `claim_authority: NONE` and
`claim_status: UNVERIFIED`. Local rechecking is not independent attestation;
execution, preservation and review share the operator/session trust domain.

## Previous archive gap remains historical

The previous [2026-10-11 replay record](Z_PHASE_REPLAY_2026-10-11.md), whose
outer archive digest was `ff47b49f3b2f3ee738a9368b31dd921548cb9b642e08699d8b8a6c047a69bbb0`,
is not replaced or reconstructed by this new run. A read-only observation in
the current VM confirmed that the exact old ZIP and source checkout were absent;
the checked private Drive and D: locations did not contain that archive either.
Its historical execution PASS remains separate from its unresolved preservation gap.

## Next action and boundaries

The subsequent [Z-core receipt](../docs/stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md)
and [Z+J receipt](../docs/stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md) reviewed
this one shared clean execution and its preserved archive. Their named claim
scopes are admitted separately; this index and original metadata retain
NONE / UNVERIFIED and do not self-promote. Do not repeat the replay.
Current claim documents reflect those receipts, not authority inherited from
this session index. Next is separately authorized public-reproduction/technical-note preparation.

No uniform/numerical epsilon, first/unique zero, simple-zero, J-margin, Q pole or
limit, paper equivalence, literature novelty, independent reproduction, application
or Navier–Stokes solution is admitted here. Site and Zenodo work have not started.

Operational recovery launchers are not committed authority inputs. No proof,
authority runner or tests were changed; no Windows Lean installation, `lake update`,
Git commit/push, tag or release was performed in this recovery session.
