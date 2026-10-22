# P1 margin / normalization — commit-bound replay execution record

Observed and archive-reviewed **2026-10-22 (Asia/Bangkok)**. Run ID and
execution timestamps use UTC 2026-10-21. This is an execution/preservation
record, **not a dated claim-admission receipt**.

```yaml
check_status: PASS[COMMIT_BOUND_EXTERNAL_P1_MARGIN_REPLAY]
artifact_check: PASS[PRIVATE_DRIVE_ARCHIVE_REOPEN:P1_MARGIN_REPLAY]
task_status: COMPLETED for approved checkpoints, push, one replay and private preservation
claim_authority: NONE
claim_status: UNVERIFIED
receipt_admission: PENDING
independent_attestation: false
d_archive_copy_verified: false
```

## Checkpoints and local controls

- Proof-only commit: `fba27381bcfda3af6f03e2fbae82f6db016ca534`.
  Only `P2_ZPLUS_J_QuantitativeMargin.lean` and
  `P2_ZPLUS_J_MarginNormalization.lean` were added.
- Execution commit: `7f29ebf0e2b894bf598144628230ae09df436c3d`.
  Only `scripts/run-p1-margin-replay.py` and `tests/test_p1_margin_replay.py`
  were added. Existing pinned source-identity helper bytes were reused.
- Both commits were pushed to `origin/main`; a post-push `git ls-remote`
  returned the exact execution SHA. No force push, tag or release was made.
- Existing dirty README/docs/memory/storage-policy changes and one-off
  development/observation/preservation helpers were excluded from both commits.
- Focused synthetic runner controls: **40 passed**. Entire declared repository
  pytest profile: **590 passed, 3 skipped, 22 subtests passed**, coverage
  **90.29%**. Python 3.14.3 on Windows. Ruff for runner/tests and diff whitespace
  checks passed. Software tests are not Lean evidence or hosted CI results.

The two proof Git blobs are respectively
`16e0f2d48f0205db7a7d3bca9c1ab9262e7b925a` and
`b3d8d48f9cd808a101540fff91f4314f921f6a0e`.
Executor raw SHA-256 values were observed, not inferred from Git:

| Proof | Replay raw SHA-256 (also matches successful development input) |
| --- | --- |
| QuantitativeMargin | `7a504d7c9cde6d76f2d0e826572fbbebeae905166802adc3e7b0d9b844e534b6` |
| MarginNormalization | `058ad35fca4228ea29773cef7c118dce7414745451f7f20361ca159d9a68ab8b` |

## One fresh replay

Run: `nsrw-p1-margin-replay-20261021T181509633115Z`.
Started `2026-10-21T18:15:11.261274+00:00`, finished
`2026-10-21T18:16:26.762401+00:00`.

A new detached checkout of the exact execution commit was tracked-clean.
The runner bound all seven execution inputs to exact committed bytes and
checked six portable blob pins (five Lean inputs plus the source helper).
Runner identity was bound to the exact expected execution commit.

```text
pinned source +NavierStokes.OutgoingProfile
 -> fresh Z01 -> fresh Z02 -> fresh conditional Z+J
 -> fresh QuantitativeMargin -> fresh MarginNormalization
```

All **6/6 stages exited 0**, with empty stderr. Five new external `.olean`
artifacts were created in a new artifacts directory. Inherited Lean search
paths were removed. No F1--C04 branch was rerun, and earlier development
artifacts were not used for these five modules.

Ten actual `#check` statements and their axiom outputs were inspected from
the success archive: four quantitative declarations and six normalization/
plateau declarations listed in the two development records. Every axiom set
was exactly `propext`, `Classical.choice`, `Quot.sound`; `sorryAx` was absent.
The same-Profile/eta/r, strict first-window, exact mass-zero and actual c1>0
hypotheses of the two J lower bounds were present in the printed statements.

Source identity was checked before/after: source
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, manifest Git blob
`f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`, pinned 11 dependencies and Lean
`4.34.0-rc2` commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` matched.
Source/NSRW tracked states and input identities matched pre/post; bounded
Lean-shadow scans passed. The source target `.olean` was unchanged pre/post:
`444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c`.
The source cache was reused: **not a cold rebuild of Lean/mathlib**.
No installation, `lake update`, proof repair or replay retry was performed.

## Private archive and separate review path

Saved ZIP:

`MyDrive/NSRW-evidence/2026-10-22/nsrw-p1-margin-replay-20261021T181509633115Z/nsrw-p1-margin-replay-20261021T181509633115Z-replay-evidence.zip`

- ZIP size: **583281 bytes**.
- ZIP SHA-256: `9163d2ee67a4cab03c152151d1df7c3e4990306c6d2fa184b52d63e556aa52a5`.
- Archived metadata SHA-256: `cf92bac7c368b79368f0d2f2be9bea847b2a9ed79fe535081debd053f734c55b`.
- Drive `archive-review.json` SHA-256:
  `2ebc4da3f1021c74eba36ffd610fc8ba883843484483b2db7a1e4b69d4cf6922`.
- Review timestamp: `2026-10-22T01:17:39.510912+07:00`.

The VM original was copied exclusively (no overwrite), reopened from private
Drive and compared by length/SHA-256. Separate operational review code did
**not** import the runner: it checked ZIP CRC, unique/safe member paths,
absence of symlink members, exact 25-member inventory, all seven input
digests **and Git committed bytes**, five artifact digests, twelve log
digests/lengths, ten statement/axiom surfaces, six exits/stderr and pre/post
identities. Launch JSON, checkout log and launcher stdout/stderr were also
copied beside the ZIP and reread. These auxiliary files are not mathematical
authority inputs. Original development/failure archives were not changed.

This is logically separate verification code in the **same operator and VM
trust domain**, not independent reproduction, external attestation, a D: ZIP
crosscheck, public redistribution approval or claim admission. Full evidence
stays in private Drive; this small record and operational helpers stay on D:.

## Next gate and non-claims

Next: dated receipt review of exactly the ten quantitative/normalization/
plateau propositions. Metadata remains `NONE / UNVERIFIED`; the execution
checkpoint must not be replaced by a later documentation commit.

No numerical q>0, interval expm1 implementation, explicit evaluable Profile,
discharged combinedScale/amplitude hypotheses, root finder, uniform/numerical
epsilon, uniqueness, pole, application performance or literature novelty is
admitted. P0 numerical admissibility and P2/P3 work remain open. The earlier
Z-core/Z+J receipts and their existing admitted scopes are unchanged.

## Subsequent scoped admission — 2026-10-22

After the execution/preservation state above, a separate
[dated receipt](../docs/stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md)
accepted exactly the ten named formal propositions. The original private ZIP
was fetched through the connected Drive file API to the Git-ignored D: evidence
directory and directly rechecked, including exact committed input bytes and
actual declaration/axiom outputs. The later Colab review cell had no completed
output observed by the reviewer and is not credited as a check.

This addendum does not alter the original metadata, execution checkpoint or
archive. The execution's NONE/UNVERIFIED fields above remain original observations;
only the separate receipt records claim admission. OE-2 and the shared operator
trust domain remain. P0 numerical admissibility and P2/P3 are still open.
