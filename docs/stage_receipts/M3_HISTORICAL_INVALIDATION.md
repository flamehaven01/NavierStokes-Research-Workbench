# M3 historical execution-assertion tombstone

Date: `2026-09-11`

Status: `AUTHORITY_REVOKED[F-SP-001_PATH_PRESENCE_ASSERTION]`

## Affected assertion

Before the v0.2.2 correction, `src/nsrw/m3_evidence_cli.py` could report
`build_attempted=true` and a Lean build `PASS` from `lake`/`lean` PATH presence
without starting a build subprocess. Any receipt produced by that code path is
not admissible as compiled evidence.

## Inventory

No committed `nsrw.m3-evidence-execution.v1` receipt containing
`build_attempted` was found in the repository at this audit point. The
inventory may be incomplete for uncommitted or externally retained outputs;
unknown receipts are not reconstructed.

The following documents are not revoked by this tombstone:

- `docs/M3_EVIDENCE_EXECUTION_ADDENDUM_2026-09-09.md`, SHA-256
  `F18693F37B13E8FBB0579F4988A752AF990B6D5D30D96169447C4E27F8B3F5EE`,
  because it explicitly records that no build ran;
- `docs/stage_receipts/MATH_STAGE_M3.md`, SHA-256
  `B0D401F491C1D1206EB0C5EDE89393E7F2ED81E801E90976AB9F2A77A8A594C3`,
  because its compiled-target statement is based on the separately captured
  M3R target build rather than the defective PATH-presence branch.

## Superseding rule

An M3 compiled PASS now requires an actual subprocess start and zero exit code.
The receipt records the command, exit code, and bounded stdout/stderr digests.
Tool presence alone yields no execution claim.

This tombstone is additive. Historical files remain unchanged.
