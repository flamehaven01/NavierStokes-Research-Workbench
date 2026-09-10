# Implementation Stage IV Receipt

Status: `GREEN`

## Delivered

- One-command source-bound research pipeline.
- Compact receipt by default and full graph/gate evidence with `--full`.
- Deterministic replay fingerprint and byte-for-byte replay test.
- Explicit unavailable Lean toolchain/build and semantic-alignment checks.
- CLI failure receipts for malformed inputs.

## Checks

- `PASS[STAGE-IV:focused-pytest]`: 8 initial Stage IV tests passed after the cycle-summary fail-closed repair; two additional anti-forgery tests were then added.
- `PASS[STAGE-IV:full-pytest]`: 40 cumulative tests passed on Python 3.14.3 after CI portability coverage was added.
- `PASS[STAGE-IV:coverage]`: 90.66% total coverage passed the configured 90% minimum.
- `PASS[STAGE-IV:ruff]`: all source and test files passed.
- `PASS[STAGE-IV:compile]`: all source modules compiled.
- `PASS[STAGE-IV:actual-cli]`: exit 0 with pipeline `GREEN`, claim `UNVERIFIED`, 5/5 mutations killed, and a 31-node/31-edge graph.
- `PASS[STAGE-IV:deterministic-replay]`: two independent compact runs produced identical bytes; output SHA-256 `E3D2CAC09A37B003CE4C64998A5F32B30E1B49EE95D08882F896A00BF0AEE1AF`.
- `PASS[STAGE-IV:anti-self-attestation]`: a forged contract carrying `CONFIRMED` plus self-declared all-PASS checks is held and downgraded to `CONTESTED`.
- `PASS[STAGE-IV:negative-cases]`: wrong source hash, cyclic graph, malformed JSON, missing locators, and surviving mutation paths fail closed.
- `PASS[STAGE-IV:slop-rules]`: six runtime Python files analyzed; finding total 0, high 0, critical 0, weighted deficit 0.0.
- `UNAVAILABLE[STAGE-IV:slop-ml]`: incompatible local detector model; not used for GREEN.
- `UNAVAILABLE[STAGE-IV:lean-build]`: `lake` and `lean` are not installed locally; no build claim is made.
- `UNVERIFIED[STAGE-IV:semantic-alignment]`: the paper-to-Lean crosswalk is locatable but has not received an independent semantic-equivalence judgment.

## Output

- Compact receipt: `outputs/navier-stokes-receipt.json` (ignored by Git as a generated artifact).
- Replay receipt: `outputs/navier-stokes-receipt-replay.json` (ignored by Git).
- Stable logical fingerprint: `FD2921283E0999E04A3C103264711A410A08A2BDAE691DEF085D48765B78FAE5`.

All four implementation stages are GREEN within their software verification scope. The mathematical claim is not GREEN and remains `UNVERIFIED`.
