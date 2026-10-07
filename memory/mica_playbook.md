# NSRW maintenance playbook

This is a short working reference. It does not grant permission, control product
behavior, introduce gates, or establish mathematical claims. Current user scope
and direct repository evidence take precedence over stale memory.

## Start a session

1. Read README.md, its MICA manifest, and the two selected files directly with
   ordinary file access. No external checkout, Python loader, or network is
   required. This is the normal loading path, not a degraded fallback.
   Record what was loaded when provenance matters; otherwise avoid routine
   loading announcements. Direct reading is not runtime emission.
2. Run `git status --short` and inspect relevant local instructions. Preserve
   unrelated tracked and untracked work.
3. Read `docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md` for the active task and its
   last evidence. Follow references only for the task at hand. The ledger is an
   index; receipts and exact proof inputs explain each admitted proposition.
4. Check the actual files and environment before executing. Report conflicts
   with memory instead of silently trusting it. Missing memory tooling is not
   a mathematical failure or a reason to introduce a new project-wide gate.

## Local Python and Lean

From the NSRW repository root on the current Windows workstation:

```powershell
. ..\..\venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pytest --version
```

This resolves to the existing `D:\Sanctum\venv` environment, not a venv inside
NSRW. On another host, locate the explicitly configured environment rather
than assuming this path exists. Do not silently use global Python or install
missing dependencies.

Use the activated Python for local runners and tests. Lean/Lake still use the
pinned source-root environment described in `formal/p2/README.md`; Windows
venv activation does not configure Lean or Colab's Linux Python.

For changed Python behavior, run focused tests with that Python. Pure memory
edits need entrypoint, reference, and readability checks, not a full Lean build
or an external memory runtime.

## Colab work

Use `colab/README.md` for storage and publication practice. Inspect the connected
VM's actual source, toolchain, and dependency state before using historical
notebook output. Environment recovery, compile, and receipt admission remain
separate operations under the existing restart checklist.

Keep local launchers and required execution information under `colab/` and raw
evidence under `colab/evidence/<date>/<unique-run-id>/`. Transfer required VM
evidence before releasing it; record incomplete transfer explicitly. Preserve
failed runs. Do not combine logs from different runs to manufacture success.

## Maintenance and handoff

- Update this archive only for an approved durable decision; update the playbook
  when the actual working procedure changes. Do not store full conversations.
- Update current progress in the existing checklist and dated evidence, not in
  a second MICA status board. Do not rewrite historical receipts.
- Leave a compact handoff in the existing task/run record: active target, last
  observed result, input identity, evidence location, and the next concrete
  action with any outstanding approval. Private runtime context stays local.
- Memory changes do not imply commit, push, install, release, or branch changes.

After changing this package, check that README names one manifest, that its
selected files are readable, and that archive references still exist. Read the
actual contents; a file list alone is not loaded context. From the NSRW root:

```powershell
Get-Content .\mica.yaml
git diff --check
```

The contract version is `mica_spec: 0.2.9`, independent of tool releases.
Optional validation and context emission were tested with MICA v3.3.1. A host
that already has compatible MICA tools may use `mica_pct.py` and
`mica_runtime.py --format context`; do not fetch or install that repository
just to read this package. No tool version is required for direct reading.
Reading, optional emission, and model understanding are distinct observations;
none establishes that a research claim passed.
