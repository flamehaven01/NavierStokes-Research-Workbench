# Implementation Stage I Receipt

Status: `GREEN`

## Delivered

- Research Proof Contract v1 schema.
- Source-bound OpenAI Navier--Stokes fixture.
- Taylor--Green falsified negative-control fixture.
- Fail-closed semantic, hash, commit, and Lean declaration locator validation.

## Checks

- `PASS[STAGE-I:focused-pytest]`: 9 tests passed.
- `PASS[STAGE-I:full-pytest]`: 9 tests passed; this is the full suite at Stage I.
- `PASS[STAGE-I:actual-source-bindings]`: PDF and Markdown SHA-256 values, OpenAI Git HEAD, and three Lean declaration locators reproduced.
- `PASS[STAGE-I:ruff]`: all `src` and `tests` checks passed.
- `PASS[STAGE-I:mutation-basics]`: missing source, hash mismatch, weakened hypothesis, wrong BKM quantity, scope inflation, and fake confirmation failed closed.
- `PASS[STAGE-I:slop-rules]`: one runtime Python file analyzed; `overall_status=clean`, finding total 0, high 0, critical 0, deficit 0.0.
- `UNAVAILABLE[STAGE-I:slop-ml]`: the installed detector could not load its incompatible local ML artifact. No ML cleanliness claim is made.
- `PASS[STAGE-I:scope]`: claim remains `UNVERIFIED`; static Lean declaration presence is explicitly not a Lean build or semantic-equivalence result.

## Transition

All required Stage I software gates passed. Stage II may begin.
