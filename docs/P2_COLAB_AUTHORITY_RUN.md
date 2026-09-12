# P2 Colab authority-run rationale and method

`task_status: COMPLETED[P2_L1_AUTHORITY_RUN]`

## Decision

For the current P2-L1 reproduction, Colab is the most practical low-overhead
execution route. It is used as a **fresh, short-lived Linux executor whose
project state is reconstructed from pinned inputs** for one Lean target and one
external proof module. It is not the research environment, a source of
mathematical authority, or a replacement for a reproducible build recipe.

Here, `authority run` means authority only for the recorded execution of the
named Lean propositions under the pinned source, toolchain, manifest, proof,
and runner identities. It does not mean mathematical authority over the source
theorem or the manuscript.

## Latest recorded result

The authority run recorded in
[`stage_receipts/P2_L1_COLAB_2026-09-12.md`](stage_receipts/P2_L1_COLAB_2026-09-12.md)
completed under NSRW commit `9f374f928e57a8955f6795d1cc6360549ed5b75b`.
It compiled `+NavierStokes.PulseAmplitude` and the external P2-L1 module with
exit code zero. Its confirmation scope is limited to the two L1 propositions
listed in the receipt; it does not close the broader P2 obligations.

This choice is driven by the shape of the work:

- the exact Lean source tree, manifest, and toolchain are already pinned;
- the requested task is a single target build plus one small external module;
- the local Windows environment does not currently expose the required Lean
  executable path; and
- the work does not justify creating a new project, changing the OpenAI source
  tree, or maintaining a persistent build service before L1 is known to work.

Colab therefore minimizes operational change while preserving the required
identity checks. A fresh session is useful here because it makes hidden local
state less likely to stand in for the pinned source, toolchain, and manifest.
The freshness of the VM is an operational convenience, not an identity claim;
the admitted project state is established by the recorded pins, hashes, Git
status, and execution outputs.

## What is executed

The authority boundary is deliberately narrow:

```text
pinned OpenAI source checkout
  + exact Lean toolchain
  + unchanged committed Lake manifest Git blob
  + target build: +NavierStokes.PulseAmplitude
  + NSRW commit-bound external module: P2_L1_MainPulsePositivity.lean
```

The runner is
`scripts/run-p2-lean-colab.sh`. It verifies source identity, the committed
manifest Git blob,
proof-file custody, runner custody, and the shared NSRW Git revision before
building the source target and compiling L1.

The committed manifest identity is Git blob SHA-1
`f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`. The runner records a raw
SHA-256 of the runtime file for observation, but does not use it as an
admission gate: a byte-level raw hash changes when the same Git content is
checked out with Windows CRLF versus Linux LF line endings. The previously
recorded Windows CRLF SHA-256
`d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f`
is therefore historical runtime metadata, not a portable source identity.

The target is intentionally not a full-library build. L1 needs the
`PulseAmplitude` surface; compiling unrelated Navier--Stokes or Euler targets
would add execution cost and failure modes without increasing the authority of
the two L1 propositions.

## Why this is the right current method

| Requirement | Colab authority-run response |
| --- | --- |
| Preserve the original formal environment | Run from the OpenAI source root with its own `lean-toolchain` and `lake-manifest.json`. |
| Avoid local-environment drift | Reconstruct the project from pinned inputs in a fresh external Linux session rather than adapting the Windows installation. |
| Keep the experiment small | Build only `+NavierStokes.PulseAmplitude`, then compile L1. |
| Make the run reviewable | Record source/NSRW commits, runner and proof hashes, tool versions, target outcome, and stdout/stderr hashes. |
| Avoid infrastructure drift | No new Lean project, no source modification, no CI workflow, no L2--L4 draft. |

The executor may be replaced by another fresh Linux host later. The authority
comes from the captured identity and execution record, not from the Colab
brand or an interactive notebook.

## Run method

Run only the following sequence after checking out the recorded NSRW commit
and the pinned OpenAI source commit.

1. Install the source-declared Lean toolchain. The `elan` installer is
   bootstrap transport only; the admitted Lean identity is the version named
   by the source `lean-toolchain` and observed again from the source root at
   execution.
2. Invoke the committed runner with `--bootstrap-dependencies` only when the
   source dependency directory is absent.
3. If bootstrap runs, preserve `bootstrap.stdout.log` and
   `bootstrap.stderr.log`, record their hashes in the dated receipt, and
   re-check the pinned source for tracked changes before admitting the compile
   result. Lake's known one-line project-name normalization is accepted only
   when its complete Git diff exactly matches the runner's pinned value; the
   runner immediately restores `lake-manifest.json` from Git and then requires
   the pinned committed blob and a clean tracked tree. Any other manifest or
   tracked-source change fails closed.
4. Let the runner reject a changed manifest, dirty source tree, dirty proof,
   dirty runner, mismatched proof/runner worktrees, or missing toolchain.
5. Capture `run-metadata.txt`, the bootstrap logs when present, the
   source-build logs, and the Lean stdout and stderr logs.
6. Copy only the allowed, redacted values into a dated receipt based on
   `stage_receipts/P2_L1_COLAB_TEMPLATE.md`.

The run command is:

```bash
source "$HOME/.elan/env"
/content/NavierStokes-Research-Workbench/scripts/run-p2-lean-colab.sh \
  --lean-root /content/NavierStokesAndEuler \
  --proof /content/NavierStokes-Research-Workbench/formal/p2/P2_L1_MainPulsePositivity.lean \
  --output-dir /content/p2-l1-run \
  --bootstrap-dependencies
```

Do not add an L2/L3/L4 module, edit a proof, run a full library build, or mix
CFD/ML experiments into this session.

## Admission and result rule

L1 may be recorded as
`PASS[PINNED_SOURCE_TOOLCHAIN_EXTERNAL_MODULE]` only when all of the following
are present and mutually consistent:

1. dependency bootstrap is either `SKIPPED[DEPENDENCIES_PRESENT]` or
   `PASS[EXECUTED_AND_RECORDED]`; when executed, its stdout/stderr hashes are
   recorded, any observed manifest normalization exactly matches and is
   restored by the runner, and the source tracked tree is clean after
   bootstrap;
2. `lake build +NavierStokes.PulseAmplitude` exited zero;
3. `lake env lean P2_L1_MainPulsePositivity.lean` exited zero;
4. `#print axioms` output was captured;
5. source commit, manifest committed Git blob identity, declared and observed toolchain identity,
   NSRW commit, proof hash, and runner hash match the dated receipt.

A failure or unavailable runtime is evidence about this execution route, not a
reason to edit the proof or weaken the identity checks. Preserve the logs and
record `ERROR` or `HELD` with the failing boundary. A failed authority run
must never be converted into a PASS by editing the proof inside the same
execution record.

## Scope after a successful run

The only propositions eligible for confirmation are:

```text
0 <= z -> 0 <= mainPulse z
0 < mainPulse (1 / 25)
```

It does not establish `F1 > 0`, `DeltaM < 0`, a first-repair interior zero,
the manuscript's theorem, or a solution to Navier--Stokes. Those remain
separate obligations with their own source-bound modules and receipts.
