# CI/CD Foundation Receipt

Status: `CI_CONFIG_GREEN__HOSTED_RUN_UNVERIFIED__CD_HELD`

## Implemented CI

- GitHub Actions workflow at `.github/workflows/ci.yml`.
- Read-only repository permission.
- Push, pull-request, and manual triggers.
- Ubuntu and Windows matrix on Python 3.10, 3.11, and 3.12.
- pytest with a mandatory 90% coverage floor.
- ruff and bytecode compilation.
- two-run deterministic contract/graph, math-kernel, and analytic-spine replays.

## Verification

- `PASS[CI:yaml-structure]`: the workflow parsed and contains the two expected jobs.
- `PASS[CI:local-pytest]`: 115 tests passed on local Python 3.14.3.
- `PASS[CI:coverage]`: 94.74% passed the 90% floor.
- `PASS[CI:ruff]`: source and tests passed.
- `PASS[CI:compile]`: source modules compiled.
- `PASS[CI:contract-only-replay]`: two receipts were byte-identical.
- `PASS[CI:math-kernel-replay]`: two math receipts were byte-identical; local SHA-256
  `505913E2373B9B500F801D7B6335E2806AE6D486354426D9BEABEF9C7CD55DB2`.
- `PASS[CI:analytic-spine-replay]`: two M2 receipts were byte-identical; local SHA-256
  `EBF7A786AD2A39E356A9D8A33AFA1111BA58C7C9A59CFC6C9EE619B10446A015`.
- `PASS[CI:local-source-bound-gate]`: the actual local PDF, Markdown, Git commit, paper locators, and Lean declaration locators passed the bounded pipeline.
- `PASS[CI:slop-rules]`: 18 runtime Python files analyzed with zero findings.
- `UNAVAILABLE[CI:slop-ml]`: no compatible detector model was configured for this run.
- `UNVERIFIED[CI:hosted-execution]`: no remote repository/workflow run exists yet.

## Hosted source boundary

The hosted runner cannot access the local `D:` archive. The CI replay therefore uses `--no-verify-sources`; source and paper-locator checks remain `SKIPPED` in that receipt. This is a portability test, not source-bound verification.

## CD boundary

No CD job is configured. There is no authorized package registry, deployment target, release policy, signing identity, or remote repository. Publication, GitHub Release creation, tagging, and proof-status promotion remain `HELD` until separately authorized and configured.
