# Colab execution files and local evidence

Local storage policy, effective 2026-10-07.

Keep required Colab launchers, development runners, input manifests, notebook
exports, logs, and handoff information in this repository's `colab/` directory,
not a local Temp directory. Preserve previous run evidence without overwriting it.
This directory is a storage location, not a source of mathematical authority.

## Storage and publication

- Keep reusable, reviewed launchers and instructions as ordinary tracked files.
- Keep raw execution evidence under `colab/evidence/<date>/<unique-run-id>/`.
  This subtree is ignored by Git. Save inputs, metadata, command exit codes,
  stdout/stderr, artifact hashes, and archives there before handoff.
- Git-ignored evidence is not protected by Git history. A destructive cleanup
  such as `git clean -fdx` can delete it; do not run cleanup against this subtree
  without first preserving and checking a separate copy. For long-term retention,
  keep an additional backup outside the working checkout.
- Do not automatically stage raw ZIPs, `.olean` files, screenshots, notebook
  output, or logs. Review any proposed public summary for secrets, hostname,
  absolute paths, and unnecessary private context first.
- Continue to place reviewed dated receipts in `docs/stage_receipts/`. A session
  index can link a run to its receipt; it does not replace receipt admission.
- Colab's `/content` is the remote execution workspace, not durable storage.
  Copy required evidence into this local directory before releasing the VM.
  If transfer fails, record that preservation is incomplete.
- Do not migrate or delete historical evidence stores merely to apply this
  forward-looking policy.

## Local Python environment

Use your already configured virtual environment and checkout, not a presumed
environment inside the repository. Substitute your own approved paths below:

```powershell
. "<venv-path>\Scripts\Activate.ps1"
Set-Location -LiteralPath "<checkout-path>"
python -c "import sys; print(sys.executable)"
python -m pytest --version
```

Use this activated environment for local Python development runners and tests.
Do not silently fall back to a global Python or install missing dependencies.
Virtual-environment activation does not configure Lean: Lean compilation still
uses the pinned source-root Lean/Lake environment. Colab's Linux Python is also
distinct from this Windows venv.

## Current phase and publication boundary — 2026-10-13

Z-core and bounded Z+J have separate named-proposition receipts from the shared
2026-10-12 replay. No new compile is scheduled solely for publication preparation.
See [the current checklist](../docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md) and
[draft release notes](../docs/releases/v0.4.0.md).

Raw evidence and held publication ZIPs remain under ignored `colab/evidence/`.
One-off launch/restore/observe helpers are also ignored; reviewed `run-*.py`
engines, replay runners, tests and their required frozen-input fixtures remain
eligible for Git. Ignore rules do not remove tracked files or protect against
destructive cleanup. A local file must not be force-added to bypass review.

## Historical C02 development example

`run-c02-development.py` is a standalone, standard-library development runner.
It does not bootstrap dependencies, require a clean NSRW checkout, or admit
claims. It builds only `+NavierStokes.OutgoingProfile` and then the exact C02
input. `inputs/` holds source copies; `artifacts/` holds the fresh `.olean`.
Only the C02 proof path must have no tracked diff and must match the pinned
Git blob `fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c`. HEAD, proof path status,
working-tree Git blob and executor raw SHA are recorded separately. Unrelated
NSRW changes remain observations. Source shadow checks include ignored Lean-like
files outside `.git`/`.lake`. Invocation exceptions retain the command and
exception with `SOURCE_INVOCATION` or `C02_INVOCATION`, not a theorem-failure claim.
`elan` and its pinned toolchain must already be installed and visible on PATH;
the runner refuses an absent pinned toolchain before invoking Lean/Lake.
Prepare the pinned environment first and supply the reviewed **executor raw
SHA-256** of the proof, not the Windows hash by assumption or a Git blob ID:

```text
python colab/run-c02-development.py --source-root <pinned-source-root> \
  --nsrw-root <nsrw-root> --proof-sha256 <reviewed-raw-sha256> \
  --output <new-run-directory>
```

The example uses shell continuation for Linux; on Windows use one line or
PowerShell continuation. Local output belongs under `colab/evidence/`.
Colab output can be under `/content` for execution, then transferred here.
Every run directory must be new. Logs are captured as raw bytes; metadata
records failure boundaries without interpreting compiler errors as mathematical
counterexamples. Source `OutgoingProfile.olean` is hashed before/after C02.
Development success remains `PASS[LOCAL_PROOF_COMPILE:P2_C02]` with
`claim_authority: NONE`. Clean replay and receipt admission belong to C-02C.

Follow [the restart checklist](../docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md).
C-02B completed its single approved Colab development compile on 2026-10-07:
`PASS[LOCAL_PROOF_COMPILE:P2_C02]`, with no claim admission. See
[the development handoff](C02_DEVELOPMENT_2026-10-07.md).
Both original archives, exact inputs, raw logs, and the fresh `.olean` are saved
locally under `colab/evidence/2026-10-07/c02-development-20261007T090736Z/`.
Archive hashes match the Colab observations; extracted C02 input/log/artifact
hashes match the run metadata. This is local preservation, not independent
attestation or a backup. At that 2026-10-07 development handoff, C-02C had not
started and downstream sign/zero claims were unpromoted. Those are historical
observations, not the current task: later separate C02/C03/C04/Z receipts are
indexed in [the documentation status index](../docs/README.md).
