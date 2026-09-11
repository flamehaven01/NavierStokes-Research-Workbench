# M4-P v0.2.2 hosted live evidence

Date: `2026-09-11`

Candidate commit: `447e86347a150bfa98e3bc5c6a61bc07c1c6223c`

Workflow run: [GitHub Actions 34579077366](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/runs/34579077366)

Check status: `PASS[HOSTED_LIVE]`

Claim status: `UNVERIFIED[NAVIER_STOKES_THEOREM]`

## Observed execution

```text
Python matrix                  PASS[4/4]
contract/replay validation     PASS
pinned Lean targets            PASS[3/3]
compiled evidence mode         LIVE_ARTIFACT
M4 live receipt                PASS[COMPLETED]
live mutations rejected        PASS[14/14]
artifact upload                PASS
```

The workflow checked out formal source commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, used
`leanprover/lean4:v4.34.0-rc2`, built the declared targets in that clean hosted
checkout, discovered their `.olean` files, generated the compiled receipt and
run-specific provenance, and consumed the generated live manifest in the same
job.

The downloaded provenance envelope identifies provider `GITHUB_ACTIONS`, run
`34579077366`, and attempt `1`.

## Downloaded artifact identities

```text
lean-compiled-receipt.json
  2D7B65C876D8C9E962E2372B091F171E91E4CDC607990498A31E634C88C8D3F8

lean-execution-provenance.json
  3639506E408487B87A890E8A9975E7DC623001473FF91AB14DD3489931C008DB

m4-parametric-pilot-v3-live.json
  42B9AB7538D4F7C60ADE21B4B8A54C34EFC6BF07F475DCA7D3CBAF2672F4C087

m4-parametric-pilot-v3-live-receipt.json
  2A6368739054EE8122E9E176C2E5A3CBB5DCD062C9F53077F1B00AC8B25FD0EB
```

Dependency outputs were also uploaded for all three targets. GitHub retains the
workflow artifact for the configured 30-day period; the hashes above preserve
their observed identities after expiry.

## Boundary

This is direct hosted execution evidence for the declared software and Lean
target scope. It does not establish the paper's correctness, paper--Lean
semantic equivalence, a computable selected-source witness, or a solution to
the Navier--Stokes millennium problem.
