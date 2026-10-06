# Current project position — 2026-10-05

Document status: `SNAPSHOT`
Valid as of: `2026-10-05`
Scope: planning/status view; not an execution receipt.

All execution states below are derived from repository receipts or current
artifact inspection. This document does not replace those receipts.

## 1. Source and repository pins

| Field | Recorded value |
| --- | --- |
| OpenAI source repository | `https://github.com/openai/NavierStokesAndEuler` |
| OpenAI source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Lean toolchain declaration | `leanprover/lean4:v4.34.0-rc2` |
| Lean commit recorded in P2 receipts | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Manifest committed Git blob SHA-1 | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| NSRW main baseline | `30c8c4fdd4854ee228d9fd6ea1178c8bf716484d` |
| Current strict-L2 file | `formal/p2/P2_L2_NormalizedMainMomentComparison.lean` |
| Current strict-L2 SHA-256 | `624f1aa042377db7e2bbe50ba70d08a35035cddc51697bd5a69a1ce0bd9bbcdd` |

The strict-L2 file is a tracked working-tree modification relative to the
recorded NSRW main baseline. Its current bytes have no compiled authority.

The resource-document edits made on this date do not change those strict-L2
bytes.

## 2. Active mathematical chain

~~~text
P2-L1
  -> P2-F1
  -> P2-L2-A
  -> strict L2
  -> L3
  -> DeltaM < 0
  -> repair-coefficient sign
  -> first-repair zero
~~~

## 3. Claim-level status view

OE level and evidence class are separate axes. Historical compiled evidence is
not erased because the current executor is unavailable, but no row is promoted
to OE-3 merely from a single historical compile.

| claim_id | status | OE | evidence class | gate/boundary |
| --- | --- | --- | --- | --- |
| `nsrw/p2/l1/mainpulse-nonnegative` | `CONFIRMED` | OE-2 | historical external compile | two named L1 propositions only |
| `nsrw/p2/l1/mainpulse-positive-1-25` | `CONFIRMED` | OE-2 | historical external compile | same receipt; not F1/L2 |
| `nsrw/p2/f1/mainmoment-one-pos` | `CONFIRMED` | OE-2 | historical local clean compile | `0 < mainMoment c 1` only |
| `nsrw/p2/l2a/log-short` | `CONFIRMED` | OE-2 | historical external clean compile | normalized bridge only |
| `nsrw/p2/l2a/one-pos` | `CONFIRMED` | OE-2 | historical external clean compile | normalized `i=1` positivity only |
| `nsrw/p2/l2/strict-normalized` | `SUPPORTED` | OE-1 | source review + uncompiled Lean source | `UNVERIFIED[NO_COMPILED_RECEIPT_CURRENT_BYTES]` |
| `nsrw/p2/l3/template-ratio` | `UNVERIFIED` | OE-0 | target only | not implemented |
| `nsrw/p2/deltam-negative` | `SUPPORTED` | OE-1 | source-definition derivation | not promoted without L2+L3 closure |
| `nsrw/p2/l4/first-repair-zero` | `SUPPORTED` | OE-1 | source-definition tail argument | formal closure open |
| `nsrw/m5/h-scaling-reconstruction` | `CONFIRMED` | OE-2 | local source-derived bounded reconstruction | reviewer replay not executed |
| `nsrw/m4s/source-instance` | `HELD` | OE-1 | source-interface review | no pinned numerical evaluator |
| `nsrw/e2/vorticity-reconstruction` | `HELD` | OE-1 | contract only | source/sample/hash admission missing |

The machine-readable record is `E2A_RESOURCE_CLAIM_LEDGER.yaml`.

## 4. Evidence-class distinctions

The following phrases are intentionally not flattened:

- P2-L1: historical **external compile**;
- P2-F1: historical **local clean compile**;
- P2-L2-A: historical **external clean compile** with fresh F1 `.olean`;
- M5 H-scaling: local bounded reconstruction with a separately operated review
  whose pytest replay was not executed;
- strict L2: current source-reviewed implementation with no compile receipt for
  the current bytes.

A historical receipt remains evidence for its recorded bytes and environment.
It is not evidence that a fresh runtime is currently available.

## 5. Immediate execution tasks

~~~text
T0  recover and observe a fresh pinned executor
T1  separate stable L2-A bridge from strict-L2 proof surface
T2  build bounded fresh F1 -> bridge -> strict dependency chain
T3  development compile of strict L2
T4  commit-bound clean replay with pre/post identity and axiom surface
T5  strict-L2 receipt and narrow documentation synchronization
T6  begin L3
~~~

The T-axis is a task sequence, not a maturity scale. See
`E2A_RESOURCE_STAGE_CROSSWALK.md`.

## 6. Progress representation

This snapshot intentionally contains no hand-written completion percentage.

The previous percentage view mixed infrastructure, open mathematics, and future
technology under incompatible denominators.

Progress is now represented by the claim ledger:

- status;
- OE level;
- evidence class;
- gate reason;
- lineage;
- dated receipt;
- negative-result record.

Any future percentage or aggregate count must be generated from the ledger with
a published formula.

## 7. External audit boundary

A structural audit can validly identify inconsistencies such as missing pins,
stage conflicts, evidence flattening, stale status, or unsupported transfer
language.

If the auditor did not independently inspect the primary source, reproduce the
Lean execution, or verify the receipt artifacts, that audit does not promote a
mathematical claim. It is recorded as structural review evidence only.

## 8. Translational position

No weather, cyclone, semiconductor, plasma, biomedical, or industrial
application is currently established.

Current PDE transfer candidates remain `unanchored_hypothesis` until TR-0
binds them to a specific claim_id.

The existing evidence-graph and mutation machinery may support an earlier
infrastructure-primitive branch, but that branch requires comparison against
existing provenance and regression-testing baselines and does not substitute
for the NSRW mathematical objective.

## 9. Current long-range objectives

Mathematical objective:

> close at least one nontrivial, source-bounded result with executable/formal
> custody and independent semantic review appropriate to the claim.

Translational objective:

> take at least one admitted claim/artifact, extract a bounded primitive, and
> determine through preregistered comparison whether it adds measurable value.

## 10. One-line restart target

> Fresh pinned execution: compile the strict normalized comparison, close the
> exact commit-bound receipt, then move to L3 without promoting downstream
> claims.

## 11. Dated addendum — 2026-10-06

Sections 1–10 remain the 10/5 snapshot, not current execution status.
The following paragraph records the position immediately after strict-L2 closure;
later 10/6 results are recorded in section 12.
The subsequent [strict-L2 receipt](stage_receipts/P2_L2_COLAB_2026-10-06.md)
records a clean checkout of `b02002b1ab954e34e7017a45e3afb338b21abfc5`, with
source build, fresh F1 artifact, and strict-L2 module all exit 0 in one run.
The exact strict comparison is now `CONFIRMED` at pinned-source compiled scope.
The historical snapshot's no-compile status is therefore superseded only for
that claim. L3 remains unimplemented; `DeltaM`, repair-coefficient signs, and
first-repair zero remain unpromoted. No independent attestation is claimed.

## 12. Subsequent closure update — 2026-10-06

The separate [L3 receipt](stage_receipts/P2_L3_COLAB_2026-10-06.md) confirms
`exp (-(3/20)*c.lam) * rowMoment (c.exponents 1) <= rowMoment (c.exponents 0)`.
The [D receipt](stage_receipts/P2_D_COLAB_2026-10-06.md) confirms NSRW
`deltaM c < 0` and two source-debt identities. The
[C01 receipt](stage_receipts/P2_C01_COLAB_2026-10-06.md) confirms the positive
matrix gap, exact main-only coefficient formula, and
`0 < affineCoefficients c 0 1 1`.

These results supersede only the corresponding open states in the historical
snapshot. Each result retains its own execution and scope; none is independently
attested. Actual `c1(0)`/`c1(eta)` signs and first-repair zero formal closure
remain open. The next mathematical task is C-02, actual coefficient decomposition.
See the [restart checklist](NSRW_COLAB_RESTART_TASKS_2026-10-06.md) and
[claim ledger](E2A_RESOURCE_CLAIM_LEDGER.yaml) for navigation to those receipts.
