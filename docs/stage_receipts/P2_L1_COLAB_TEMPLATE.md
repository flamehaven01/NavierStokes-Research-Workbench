# P2 L1 Colab execution receipt template

`receipt_status: NOT_EXECUTED_TEMPLATE`

This file is a template, not evidence of a Colab run. Copy it to a dated
receipt only after `scripts/run-p2-lean-colab.sh` has produced immutable local
logs and metadata for that execution.

## Required identity

| Field | Required value |
| --- | --- |
| Source repository | `https://github.com/openai/NavierStokesAndEuler` |
| Source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Source tracked-tree status | `clean` |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| `lake-manifest.json` committed Git blob SHA-1 | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| `lake-manifest.json` runtime raw SHA-256 | `[RECORD_AFTER_EXECUTION; observational and platform-specific]` |
| NSRW commit | `[RECORD_AFTER_EXECUTION]` |
| Proof module | `formal/p2/P2_L1_MainPulsePositivity.lean` |
| Proof-module SHA-256 | `[RECORD_AFTER_EXECUTION]` |
| Runner | `scripts/run-p2-lean-colab.sh` |
| Runner SHA-256 | `[RECORD_AFTER_EXECUTION]` |

## Runtime and command

Record the following from `run-metadata.txt` and, when bootstrap runs, from the
bootstrap logs themselves. Do not add absolute paths, account names, tokens,
or other private host details to the committed receipt.

```text
UTC timestamp: [RECORD_AFTER_EXECUTION]
OS / kernel: [RECORD_AFTER_EXECUTION]
CPU count: [RECORD_AFTER_EXECUTION]
RAM summary: [RECORD_AFTER_EXECUTION]
disk-free summary: [RECORD_AFTER_EXECUTION]
elan --version: [RECORD_AFTER_EXECUTION]
lean --version: [RECORD_AFTER_EXECUTION]
lake --version: [RECORD_AFTER_EXECUTION]
dependency bootstrap: [SKIPPED[DEPENDENCIES_PRESENT] | PASS[EXECUTED_AND_RECORDED]]
bootstrap exit code: [N/A | RECORD_AFTER_EXECUTION]
bootstrap stdout SHA-256: [N/A | RECORD_AFTER_EXECUTION]
bootstrap stderr SHA-256: [N/A | RECORD_AFTER_EXECUTION]
post-bootstrap manifest committed Git blob SHA-1: [N/A | f07a8454cb6200d90bcc4371bc9965e9f8f46c7d]
post-bootstrap manifest runtime raw SHA-256: [N/A | RECORD_AFTER_EXECUTION; observational]
bootstrap manifest normalization: [N/A | not_required | restored_exact_project_name_normalization]
post-bootstrap source tracked-tree status: [N/A | clean]
source target: +NavierStokes.PulseAmplitude
source-target build exit code: [RECORD_AFTER_EXECUTION]
source-build stdout SHA-256: [RECORD_AFTER_EXECUTION]
source-build stderr SHA-256: [RECORD_AFTER_EXECUTION]
command 1: lake build +NavierStokes.PulseAmplitude
command 2: lake env lean <P2_L1_MainPulsePositivity.lean>
elapsed seconds: [RECORD_AFTER_EXECUTION]
exit code: [RECORD_AFTER_EXECUTION]
stdout SHA-256: [RECORD_AFTER_EXECUTION]
stderr SHA-256: [RECORD_AFTER_EXECUTION]
`#print axioms` output: [RECORD_AFTER_EXECUTION]
```

## Scope and boundary

When a dated receipt records exit code zero and the required identity and
bootstrap admission fields are mutually consistent, it may state only:

```text
check_status: PASS[PINNED_SOURCE_TOOLCHAIN:external_P2_L1_module]
claim_status: CONFIRMED for the two propositions named in P2_L1 only
```

Here `PASS` is authority only for the recorded execution of the two named L1
Lean propositions. It is not mathematical authority over the source theorem
or manuscript.

The runtime raw SHA-256 is recorded to identify the bytes observed by that
executor. It is not a cross-platform admission identity: a Windows CRLF
checkout of the same pinned Git blob has raw SHA-256
`d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f`.

It must not promote `F1 > 0`, the normalized main-moment comparison,
`DeltaM < 0`, the first-repair interior-zero result, the paper's theorem, or
the Navier--Stokes problem. Those obligations require their own source-bound
modules and receipts.
