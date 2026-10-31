# CI/CD scope and publication boundary

Updated: 2026-10-31. The repository provides software/research CI and a bounded GitHub Pages deployment workflow. Release and paper publication use separately authorized operations; pushing code does not automatically publish a new software Release or paper.

The [research-site workflow](../.github/workflows/pages.yml) builds from an explicit file allowlist. Build permissions are read-only; only the deploy job has pages-write and OIDC permissions. The site includes two selected PDFs and three scalar JSON files, not raw logs, caches, private reviews or unselected manuscripts. Its deployment does not admit a new mathematical claim. [Software v0.5.0](releases/v0.5.0.md) was published after six exact-commit CI jobs passed. The historical 13 October snapshot below describes the earlier CI-only state.
Workflow edits do not authorize commit/push, a hosted run, tag, Release, Zenodo
deposit, website deployment or independent mathematical attestation.

## What the workflow checks

| Lane | Executed checks | What it does not establish |
|---|---|---|
| Python quality | Ubuntu/Windows, Python 3.10/3.12; Ruff; Python syntax; docs/public-file controls; pytest and >=90% software coverage | P2 Lean compilation, human privacy/rights clearance or hosted results before execution |
| Research controls | Deterministic software receipts, manufactured controls, SPAR identity, schema/parser and mutation checks | General PDE correctness or a selected numerical source witness |
| Scoped Lean | Pinned upstream targets consumed by M4; structured same-run M4 evidence | Fresh P2 full-DAG replay or replacement of any P2 dated receipt |

The doc controls check file-link existence, required replay input availability,
portable blobs declared by the Z runner, immutable action references, checkout/
artifact configuration and the Git index versus ignore rules. A synthetic
force-add negative control demonstrates that an ignored raw artifact **can** be
indexed and is then detected. This is not a general secret scanner or an
independent verifier of the proof. Heading anchors are not universally checked.

## Failure records and permissions

- Workflow permissions remain `contents: read`; checkout does not persist the
  repository token/SSH credential into local Git configuration.
- Existing action commit pins are unchanged. Development dependencies are not
  described as fully locked: SPAR is revision-pinned, while other declared
  requirements retain their existing version ranges. No new dependency is installed
  or upgraded by this documentation change.
- Each Python matrix job attempts to retain its JUnit and coverage XML on success
  **or failure**, with separate artifact names and seven-day retention. If the
  install/test process fails before reports exist, the upload warns; the original
  failed job is not converted to PASS. Missing tests remain unexecuted.
- The M4 Lean job also attempts its existing, narrowly listed evidence upload on
  failure. Partial/missing artifacts do not constitute admitted successful evidence.
- No upload path includes local `colab/evidence/`, held `publication/` candidates,
  caches, tokens or the entire working directory. XML reports are diagnostic CI
  outputs, not release assets. Generated source evidence retains its original scope.

These controls reduce bounded credential/publishing risks. They do not stop all
untrusted dependency behavior or replace human review of public files.

## Local checks and final hosted gate

Use your already configured Python environment; no install is implied:

```text
python -m pytest tests/test_docs.py -o addopts= -q
python -m ruff check src tests
python -m compileall -q src scripts colab
python -m pytest -ra --junitxml=<local-evidence-directory>/junit.xml --cov-report=xml:<local-evidence-directory>/coverage.xml
git diff --check
```

Local records belong in Git-ignored evidence storage. A local pass is not the
hosted 4-job matrix. After separately authorized path-scoped commit/push, inspect
the exact commit's hosted result, all job outcomes and missing/skipped obligations.
Do not use an older green badge as evidence for an unpushed workflow revision.

### Local reinforcement snapshot — 2026-10-13

- Existing Windows virtual environment, Python 3.14.3; no dependency installation.
- Focused public-file/workflow controls: 8 passed, including the force-add
  negative control and declared portable replay-input identities.
- CI-style full pytest invocation: 548 passed, 3 skipped, 22 subtests; software
  coverage 90.29%. JUnit parses as 573 cases including subtests/skips, with zero
  failures/errors; coverage XML parses as line-rate 0.9029.
- The three skips are the existing M5 external raw-export integration checks,
  not freshly executed P2 Lean results. Ruff, Python compilation, YAML parse
  smokecheck using an already installed parser, and diff-whitespace checks passed.
- Local reports: `colab/evidence/2026-10-13/ci-reinforcement-full/`, Git-ignored.
  JUnit SHA-256 `7f4271f2afe62d0899d41d49d1d36ebc37324ccec6cb1548c4db1c8558c021b0`;
  coverage XML SHA-256 `85b1fe87fce31b0a861357a1434a71da74a2a10da3a40e1637ad05ccd6724044`.
- Repository HEAD remains `3a50b5f50b034319a469b9de68f556be70fff02c`, with
  uncommitted workflow/document/test edits. This is not a commit-bound release
  verification, hosted CI matrix, actionlint/schema audit or live artifact upload.

No hosted workflow was dispatched, M4/P2 Lean rerun performed, or claim promoted.
Checkout options were inspected in the existing pinned official action source;
no action version/pin was changed.

Review the staged inventory with `git diff --cached --name-only`; ordinary
`git status --short` must include new files. Ignore does not untrack existing
files, remove secrets from history, or preserve ignored evidence against cleanup.

Historical release approval, 2026-10-14, covered NSRW software plus P01, with P02/P03 deferred.
The [publication plan](NSRW_PUBLICATION_AND_REPRODUCTION_PLAN_2026-10-08.md)
and [v0.4.0 scope](releases/v0.4.0.md) retain exact-commit hosted CI and actual
post-upload checksum/access checks as separate observations. No automated CD
workflow was introduced by that historical change. No additional Lean replay is required just to change CI/docs.
