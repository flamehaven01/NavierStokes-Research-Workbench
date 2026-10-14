# Z-01D development compile — 2026-10-10

This record indexes a development experiment, not claim authority or a
commit-bound receipt. The uncommitted proof bytes were compiled in the existing
Colab VM; no restoration, Windows installation, or `lake update` was performed.

## Exact scope

- `NSRW.P2.localMass_partial_identity`
- `NSRW.P2.localMass_tail_identity`

Both concern source `massMoment` at `pulseStart + log r`, with
`1 <= r <= exp pulseLength`. The partial identity uses source
`exp_weight_substitution` with `log r` and explicit `exp_log` normalization.
The tail identity combines that primitive with `pulse_closes_prefix` and an
integrable interval split. It does not re-prove endpoint cancellation.

## Execution identity

| Input | Observed identity |
| --- | --- |
| OpenAI source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Lean | `4.34.0-rc2`, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Manifest committed Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Identity-helper checkout | `10d5a1f517b8665137f2354746d70752f8ef67fd` |
| Proof raw SHA-256 | `ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267` |
| Development driver SHA-256 | `1eda051bf2775b598df55729eeaf2b56a4dcb82b73c1ba4914c6f2282142af9e` |
| Fresh Z01 `.olean` SHA-256 | `362b61b96ff800a09578d26a577f595213a8be5a9d38476d84eb1462e573a52c` |

The helper checkout supplies only the committed source-identity checks from
`run-c02-development.py`. It is **not** the execution commit of this new proof.
No F1/L2/L3/D/C01/C02/C03/C04 external proof chain was recompiled: the Lean
dependency surface is `OutgoingProfile -> Z01`.

Run: `nsrw-z01-development-20261010T083448Z`.
Started `08:34:48 UTC`; finished `08:36:04 UTC`.

```text
source: lake build +NavierStokes.OutgoingProfile
  exit 0; stderr 0 bytes; existing source/dependency cache reused
Z01: lake env lean -R <run>/inputs -o <run>/artifacts/P2_Z01_LocalMassIdentities.olean
  <run>/inputs/P2_Z01_LocalMassIdentities.lean
  exit 0; stderr 0 bytes
both named axiom surfaces: [propext, Classical.choice, Quot.sound]
sorryAx: absent
source identity pre/post: equal
OutgoingProfile.olean pre/post SHA-256: equal
check_status: PASS[LOCAL_PROOF_COMPILE:P2_Z01]
claim_authority: NONE
claim_status: UNVERIFIED
```

## Evidence preservation

Git-ignored local evidence:
`colab/evidence/2026-10-10/nsrw-z01-development-20261010T083448Z/`.
The ZIP contains metadata, four raw logs, three execution inputs, and the fresh
Z01 artifact; extracted bytes are in `raw/`.

ZIP: `nsrw-z01-development-20261010T083448Z-evidence.zip`, **62,282 bytes**.
SHA-256: `0b10325a50879e1bbe96a0030b848b2b044c522c950e76ca0aa21ed207f0e87d`.

The in-app page crashed while preparing a download link after compilation.
A recovery tab reconnected to the same VM. The already completed ZIP was
transferred through an explicitly displayed base64 output; its displayed SHA
matched the locally decoded ZIP. No second proof execution was performed.
Local extraction cross-checked input/log/artifact hashes and metadata identity
observations: `PASS[LOCAL_ARCHIVE_CROSSCHECK:Z01_DEVELOPMENT]`.

These checks and execution share the same trust domain. They are not an
independent attestation or a full clean rebuild of the source library.
Ignored evidence is not protected by Git history.

## Non-claims / next implementation

No boundary mass signs, second-bump positivity, IVT, interior zero, uniqueness,
first-zero claim, or full Z admission. No commit/push/tag/release performed.
Runner parser controls (one positive, six negative), Ruff and `git diff --check`
passed; those checks are not Lean proof evidence.

Next implementation: **Z-02 boundary signs and upper-tail localization**.
The Z01 proof remains uncommitted development bytes; commit-bound replay and
receipt admission must not be inferred from this record.
