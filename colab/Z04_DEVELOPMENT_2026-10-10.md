# Z04-core development handoff — 2026-10-10

This is a preserved development-compile record, not a commit-bound admission receipt.

## Current boundary

- Implementation: four named Z04-core propositions written.
- Runner controls: `PASS[FOCUSED_TESTS:Z04_DEVELOPMENT_DRIVER]`, 26 tests.
- Ruff: `PASS[RUFF:Z04_DEVELOPMENT_DRIVER]`.
- Actual Lean compile: `PASS[LOCAL_PROOF_COMPILE:P2_Z04_CORE]`.
- Archive transfer/review: `PASS[LOCAL_ARCHIVE_REVIEW:Z04_DEVELOPMENT]`.
- Compile task: `COMPLETED[Z04_CORE_DEVELOPMENT_ONLY]`.
- `claim_authority: NONE`; `claim_status: UNVERIFIED`.
- Colab-only environment restoration was explicitly approved and completed.
- No J/Q implementation, claim admission, Windows installation, `lake update`,
  commit, push, tag, or release.

The original tab crashed. A second tab was recovered using the documented
browser UI and connected to a runtime. A new read-only cell
`cell-yYJbLgC6qC9b` was actually executed, separate from historical Z03 output:

```text
Z04_VM_OBSERVATION_ONLY
source_exists False
elan_exists False
z03_run_exists False
```

No `nsrw-c04c-clean-*` base candidate was printed. The runtime subsequently
disconnected, as observed on screen. At that observation, no Z04 compile had
been launched. The user then explicitly approved Colab-only restoration and
compilation. The initial observation and screenshot remain preserved in
`colab/evidence/2026-10-10/z04-vm-observation/`; they are not compile evidence.

## Exact inputs prepared

| Input | SHA-256 |
| --- | --- |
| `formal/p2/P2_Z04_FirstRepairInteriorZero.lean` | `f3bce7c0a6d28922bd592d6dbfb5b0735a058ffc84c2100bc4328be1df5b2d5d` |
| `colab/run-z04-development.py` | `8103a9353a0d152d8f0f2f28af9c72b8e932c124db27536bc6124154d5b21643` |
| `tests/test_p2_z04_development.py` | `d3472d8a261162e29685a6daa4839889a3e1d3a6e76f26fe61f5295a74fa38c6` |

The proof imports only `P2_C04_SmallPositiveEta` and
`P2_Z03_ConditionalInteriorZero`. Its named surfaces are:

1. `localSecondRepairCoefficient_eq_actual` — definitional coefficient alias.
2. `exists_firstRepair_zero_small_positive` — C04 supplies the sign consumed by Z03.
3. `localMass_eq_profileM` — same mass object at `exp(pulseStart) * r`, with `1 ≤ r`.
4. `profileM_firstRepair_zero_small_positive` — per-Profile existential epsilon
   and an interior first-repair zero of source `Profile.M`.

All four statements compiled in the fresh development run below. There is no
uniform/numerical epsilon, uniqueness, first-zero, angular moment, or Q result.

## Executed development run

- Environment restoration: `nsrw-z04-restore-20261010T163852Z`.
- Fresh base checkout: `10d5a1f517b8665137f2354746d70752f8ef67fd`.
- Compile run: `nsrw-z04-development-20261010T164504Z`.
- Compile started UTC: `2026-10-10T16:45:04.892203+00:00`.
- Compile finished UTC: `2026-10-10T16:55:35.200084+00:00`.
- Source: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
- Toolchain observed: Lean `4.34.0-rc2`, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`.
- Portable manifest blob: `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`.

Environment restoration recorded nine bootstrap stages, all exit 0. This run
had **no manifest normalization**: before/after bootstrap bytes were identical
and `manifest.diff` was empty. A local review initially assumed the previously
observed name normalization was mandatory; that check failed. Inspecting the
actual archived bytes established the unchanged-manifest case instead. No
bootstrap input or execution record was modified to satisfy that check.

The compile chain recorded 13 stage exits (source + 12 external modules), all
exit 0 with empty stderr. Twelve fresh external `.olean` artifacts and 14 input
files are archived. The four Z04 axiom surfaces each contain exactly
`Classical.choice`, `Quot.sound`, `propext`; no `sorryAx` was observed. Local
proof/driver bytes still match the execution inputs and the SHA table above.

Source/base pre-post identities matched; source tracked state was clean and
the base checkout observation was tracked-clean with no untracked files. The
source-target `.olean` hash was unchanged. All archived input, artifact, and
stdout/stderr hashes were recomputed locally and matched their metadata.

This reused the revision-bound mathlib cache, then built the requested source
target; it was not a clean rebuild of the whole upstream library. Execution,
browser transfer, and local review share the same trust domain and do not
constitute independent attestation. New Z01–Z04/driver bytes remain development
inputs, not exact committed inputs admitted by an authority replay.

## Evidence preservation

Local store: `colab/evidence/2026-10-10/z04-development-20261010T164504Z/`.

| Archive | Bytes | SHA-256 |
| --- | --- | --- |
| `nsrw-z04-restore-20261010T163852Z-evidence.zip` | 20236 | `04790112a767230a702f1233f3d4d412c475f11cc9b4dd242834de272e486cba` |
| `nsrw-z04-development-20261010T164504Z-evidence.zip` | 612552 | `5853d258e0074b09332161352922b704bc696826978d98ca25ae60da20941a09` |

Archive bytes were explicitly displayed by the Colab preservation cell and
transferred through that visible output. An initial unchunked DOM read was
truncated and was not admitted or saved as the compile archive. Thirteen
bounded chunks then reconstructed the same archive; byte count and SHA-256
matched Colab, and local ZIP CRC/hash review passed. `local-review.json`
records the bounded review; it preserves `NONE / UNVERIFIED`.

`z04-restore-start.py`, `z04-development-start.py`, `z04-progress-observe.py`,
`z04-preserve-evidence.py`, and `z04-result-summary.py` are operational helpers
under `colab/`, not new mathematical dependencies or admission surfaces.

## Development execution surface

The runner reads the eight committed F1→C04 inputs and the source-identity helper
from checkout `10d5a1f517b8665137f2354746d70752f8ef67fd`, checking each Git blob.
Z01/Z02/Z03 are exact development inputs with their successful SHA pins embedded
in the runner. The checkout's dirty/untracked state is observation, not an
authority admission gate. The new target uses an explicit executor SHA.

The requested chain is:

```text
pinned source / +NavierStokes.OutgoingProfile
→ fresh F1 → L2 → L3 → D → C01 → C02 → C03 → C04
→ fresh Z01 → Z02 → Z03 → Z04-core
```

Expected completion is 13 stage exits (source + 12 external modules) and 12 fresh
external `.olean` files. The run captures binary stdout/stderr, source and base
observations pre/post, source-target `.olean` hashes, input/artifact/log hashes,
and the four Z04 axiom observations. It rejects stderr, `sorryAx`, source/target
or input/artifact/log drift. The alias surface may be empty or inherit exactly
the three standard imported axioms; the other surfaces require exactly
`propext`, `Classical.choice`, and `Quot.sound`. Observed values are recorded,
never manufactured. The runner cannot admit a claim.

Use a new output directory outside all input roots. Do not reuse an earlier
run's `.olean`. After verifying the current VM and transferring exact Z01–Z04
and runner bytes, invoke the runner with its five required paths:

```text
python3 run-z04-development.py
  --source <observed pinned source checkout>
  --base <observed checkout at 10d5a1f517b8665137f2354746d70752f8ef67fd>
  --dependencies <directory containing exact Z01/Z02/Z03 .lean files>
  --proof <exact P2_Z04_FirstRepairInteriorZero.lean>
  --output <new unique run directory>
  --proof-sha256 f3bce7c0a6d28922bd592d6dbfb5b0735a058ffc84c2100bc4328be1df5b2d5d
```

The runner creates an exclusive evidence ZIP on success or failure. Preserve it
under `colab/evidence/2026-10-10/<unique-run>/` and cross-check its SHA before
recording actual execution. Success is limited to
`PASS[LOCAL_PROOF_COMPILE:P2_Z04_CORE]`, with `NONE / UNVERIFIED` unchanged.
If environment restoration is needed, obtain scoped approval before installing.

## Local test history

The first synthetic run found an input-directory `__pycache__` created when
importing the pinned helper. The driver now suppresses bytecode writing only
during that import and restores the previous setting. A separate second test
run passed all 26 controls. Both test-run directories remain under
`colab/evidence/2026-10-10/z04-runner-tests-01` and `z04-runner-tests-02`.
Synthetic tests are not Lean evidence.

Next research task: bounded Z+J source mapping against these frozen successful
Z04-core bytes. That work was not started in this execution request. Z-core
claim admission remains pending a later exact checkpoint/clean phase replay
and separately scoped receipt review; this development PASS does not admit it.
