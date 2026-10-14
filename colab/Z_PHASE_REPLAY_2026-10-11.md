# Z-core / Z+J clean replay — 2026-10-11

This session record links development and execution evidence. It is a custody
index, not mathematical authority itself.

check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_Z_REPLAY]
claim_authority: NONE
claim_status: UNVERIFIED
task_status: HELD for final local archive review and separate receipt admission
independent_attestation: false

## Checkpoint lineage

| Event | Exact identity |
| --- | --- |
| six-proof checkpoint, no docs/runner included | `8581a511d4c60c52f8d37663fd49f70e4d835d64` |
| wrapper/engine/two-test checkpoint | `3a50b5f50b034319a469b9de68f556be70fff02c` |
| wrapper Git blob | `22e17d57f7cd9651ba52a058ddb25b73c75bffe5` |
| engine Git blob | `6d1806c1eed0130de12b6658a1787a9a1c9cd9d3` |
| dependency extraction base | `10d5a1f517b8665137f2354746d70752f8ef67fd` |
| pinned OpenAI source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| manifest blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Lean | `4.34.0-rc2` |

Both checkpoints were pushed and remote main was observed to match the execution
checkpoint. Existing seven dirty tracked documents and unrelated untracked work
were excluded. No tag or release was created. Local tests: 64 focused controls
and 542 full-suite tests passed, 3 skipped, 22 subtests passed, coverage 90.29%;
Ruff/compileall passed. This is local software evidence, not remote CI or Lean evidence.

## One fresh replay

Run: `nsrw-z-phase-replay-20261011T150531375936Z`.
Clone/checkout steps exited 0; the wrapper enforced exact committed inputs and
tracked cleanliness before/after execution.
Wrapper finished UTC: `2026-10-11T15:07:33.286018+00:00`.

```text
pinned source / +NavierStokes.OutgoingProfile
 -> fresh F1 -> strict L2 -> L3 -> D -> C01 -> C02 -> C03 -> C04
 -> fresh Z01 -> Z02 -> Z03 -> Z04-core -> conditional Z+J -> source composition
```

Fifteen stages exited 0 with empty stderr; fourteen external `.olean` artifacts
were newly generated. Seventeen committed authority inputs were checked.
Nineteen named Z04/conditional Z+J/composition axiom surfaces matched exactly
`propext`, `Classical.choice`, `Quot.sound`; no `sorryAx` was observed.
Source/NSRW/base identities and source target artifact matched pre/post.
Source cache reuse is explicit; this is not a full clean upstream-library rebuild.

| Archive | Bytes | SHA-256 |
| --- | --- | --- |
| inner execution ZIP | 807572 | `86215906ed76ef96ce0ad4e3927681b2b9004993a4f3dfe8e837d6a1cf8b5d99` |
| `nsrw-z-phase-replay-20261011T150531375936Z-replay-evidence.zip` | 815297 | `ff47b49f3b2f3ee738a9368b31dd921548cb9b642e08699d8b8a6c047a69bbb0` |

The outer archive contains raw inputs/logs/fresh artifacts plus both metadata
layers and the exact wrapper. It does not include the upstream target `.olean`,
whose stability is only an execution observation. The inner engine keeps its
original development labels; committed custody is imposed by the outer wrapper.
Neither metadata layer admits claims.

## Preservation and remaining gate

The [conditional development ZIP](ZPLUS_J_DEVELOPMENT_2026-10-11.md) and
[source-composition development ZIP](ZPLUS_J_COMPOSITION_DEVELOPMENT_2026-10-11.md)
have completed D: size/SHA/internal hash checks. They are not reused to assemble
this replay's authority.

### Preservation recheck — 2026-10-12 (Asia/Bangkok)

preservation_check: ERROR[REPLAY_ARCHIVE_UNAVAILABLE_AT_CHECKED_LOCATIONS]
task_status: HELD[RAW_REPLAY_ARCHIVE_RECOVERY_OR_NEW_AUTHORIZED_REPLAY]

The authorized Drive-copy cell stopped before copying, at the assertion that
the exact `/content` archive exists and has 815297 bytes. This observation does
not distinguish a missing file from a size mismatch. The notebook still shows
historical successful replay output; that output is not current archive custody.
Runtime replacement is suspected, not established solely by that assertion.

The approved Drive date folder contained only the two development archives.
No exact final replay ZIP was found in the local `colab/evidence/2026-10-11/`
tree or the top-level Downloads folder. A separate read-only Colab diagnostic
cell was submitted, but its result could not be retrieved because browser reads
timed out. Do not describe its unobserved result as confirmation of deletion.

The 2026-10-11 execution PASS remains a historical observation. Final archive
size/SHA/internal verification and both claim admissions remain incomplete.
The preserved development archives must not replace or reconstruct this replay's
authority evidence. If an original copy is recovered, verify this exact archive.
Otherwise, obtain new explicit approval for Colab-only restoration and a new
clean replay at the same execution checkpoint, followed by immediate preservation.
Do not overwrite old evidence or silently reuse the prior run identifier.

After local verification, review source-facing Z-core existence and Z+J
conditional/final M/J mismatch separately, disclosing their shared execution and
same operator/session trust domain. Only then update current claim documents.
The missing first failed Z+J development archive remains a disclosed custody gap;
the distinct successful runs do not reconstruct that failed archive.

No uniform/numerical epsilon, first/unique zero, simple-zero, J-margin, Q pole or
limit, paper equivalence, independent reproduction, novelty or application is
admitted. Optional strengthenings are not prerequisites for this phase close.
Zenodo research and the site remain subsequent publication work, not launched here.

### Later recovery — separate execution on 2026-10-12

The later read-only VM diagnostic confirmed that this exact old ZIP and the
source checkout were absent. Following explicit approval, a new run at the same
checkpoint completed and its distinct ZIP was verified in private Drive and D:.
See [the new recovery record](Z_PHASE_REPLAY_2026-10-12.md). This does not recover
or rewrite the old archive; its custody gap remains historical. The current phase
now has preserved new execution evidence, with separate claim reviews still pending.
