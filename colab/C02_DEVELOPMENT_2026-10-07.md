# C02 development compile — 2026-10-07

This is a development-run handoff, not a claim-admission receipt. The executor
and this review share the same trust domain; this is not independent attestation.

## Observed result

- Run: `c02-development-20261007T090736Z`.
- Started: `2026-10-07T09:07:37.110324+00:00`.
- Finished: `2026-10-07T09:18:07.902279+00:00`.
- Check: `PASS[LOCAL_PROOF_COMPILE:P2_C02]`.
- Claim authority: `NONE`; claim status: `UNVERIFIED`.
- Source target: `lake build +NavierStokes.OutgoingProfile`, exit `0`,
  2851 jobs; 622.55 seconds. mathlib cache was used, not a full clean rebuild.
- Fresh external C02 compile: exit `0`; 4.81 seconds.
- Both stderr files: empty.
- Both named axiom surfaces: `[propext, Classical.choice, Quot.sound]`;
  no `sorryAx` observed. This is not a semantic audit of the imported library.

Only these equalities were compiled:

1. `NSRW.P2.actualRepairCoefficient_decomposition`.
2. `NSRW.P2.profile_secondRepairCoefficient_decomposition`.

No actual `c1(0)` positivity, small-positive-eta sign, or first-repair zero
proposition is promoted. C-02C commit-bound replay was not performed.

## Input and artifact identities

| Surface | Identity |
| --- | --- |
| OpenAI source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Source manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| NSRW observed HEAD | `9f39e82f9cc57b2d43e3d08bb7294920bdb74c0c` |
| C02 proof Git blob | `fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c` |
| Executor proof SHA-256 | `a2ad4f0e47428c869873de96ba681d17f0d9299ae80094f9c40462b1a8cfd5f7` |
| Runner SHA-256 | `540f0aadd7add25bc0cfae2d852009e68c23cb13537ec03c4e5bce1ba085a278` |
| Source target `.olean`, before/after | `444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c` |
| Fresh C02 `.olean` | `0f4254af1c0c429ac5d2cb4b8d35c690a32270caa4b5291933f9b1f5a2b80fdc` |

The run metadata records matching pre/post source and proof identities. The
source tracked tree was clean; NSRW tracked cleanliness was an observation,
not an authority gate. Untracked count increased with local execution outputs.
No F1/L2/L3/D/C01 external dependency chain was replayed.

## Local preservation

Local store: `colab/evidence/2026-10-07/c02-development-20261007T090736Z/`.

`logs-package.zip` is a lossless transport package of original metadata and
logs, not a reconstructed receipt. Its SHA-256 was checked against Colab:
`c0bbedf9c6d7dbcdc620bf2d6eeb55b76e2bb07f7623345ac550bb15dd27c9f3`.
Its `raw/` extraction contains original source/C02 stdout and stderr,
run metadata, launcher record/logs, and bootstrap metadata. All four stage-log
hashes match the run metadata. Local input copies are separately hash-checked.

**Preservation check: `PASS[LOCAL_ARCHIVE_HASH_MATCH]`.** Both original archives
are saved in the local store. Their locally computed hashes match the hashes
observed in Colab:

| Archive | Bytes | Matching Colab/local SHA-256 |
| --- | ---: | --- |
| `c02-development-20261007T090736Z-evidence.zip` | 17514 | `0ce1d330329ce990524285695eabf436fbb4b3ac8045a203202bc9824fa2be1c` |
| `nsrw-c02-bootstrap-20261007T090037Z-evidence.zip` | 14607 | `4d4e5333dcf019a24cc5acbfbb1011b0fe453be15da9049d177ed486720b936c` |

The full C02 ZIP includes exact inputs and the fresh `.olean`; the bootstrap
ZIP contains original installation/cache logs. Browser download routes did not
deliver local files, so the original ZIP bytes were transferred through the
notebook's lossless encoding. This transfer did not rerun the experiment or
reconstruct its metadata. `full/` and `bootstrap/` are separate extractions;
the four C02 stage-log hashes, two input hashes, and fresh `.olean` hash match
the original run metadata. The bootstrap metadata records restoration PASS.
Git ignores this local store; matching hashes are not a backup or independent
attestation. Keep a separate copy for long-term retention.

Next: obtain explicit commit/push approval for C-02C checkpoint/clean replay.
Do not recompile C02 merely to fix a download failure, combine historical runs,
or relabel this uncommitted development runner as an authority runner.

The old Windows `Core.olean.private` failure and the notebook upload-interface
failure remain debugging history, not mathematical counterexamples.
