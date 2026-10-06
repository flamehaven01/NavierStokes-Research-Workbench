# Negative and held result register

Document status: `SNAPSHOT`
Valid as of: `2026-10-05`

This register makes negative, held, and not-executed outcomes visible. It does
not replace the claim ledger or execution receipts.

| claim_id | state | reason | reopening condition |
| --- | --- | --- | --- |
| `nsrw/m4s/source-instance` | `HELD` | no pinned numerical evaluator for the source witness | source-pinned evaluator becomes available |
| `nsrw/e2/vorticity-reconstruction` | `HELD` | source revision/file/sample/hash admission incomplete | all admission identities supplied |
| `nsrw/p2/l2/strict-normalized` | `UNVERIFIED` | current strict-L2 bytes have no compile receipt | successful pinned compile of exact bytes |
| `nsrw/p2/l3/template-ratio` | `UNVERIFIED` | `OPEN[NOT_IMPLEMENTED]` | proof or counterexample |
| `nsrw/m5/h-scaling-reconstruction` | `NOT_EXECUTED[REVIEWER_RUNTIME_MISMATCH]` for independent replay only | separately operated reviewer runtime lacked pytest | independent clean replay with admitted runtime |

## Rule

A negative result is retained when later work succeeds.

A later PASS creates a new dated state or receipt. It does not erase the earlier
failure, hold, or not-executed record.

Subsequent update, `2026-10-06`: strict L2 and L3 now have separate admitted
[strict-L2](stage_receipts/P2_L2_COLAB_2026-10-06.md) and
[L3](stage_receipts/P2_L3_COLAB_2026-10-06.md) compiled receipts. Their 10/5
not-executed rows above are historical, not the current state. D and main-only
C01 have also compiled; actual coefficient signs and first-repair zero formal
closure remain open. Current claim records are indexed in
[the ledger](E2A_RESOURCE_CLAIM_LEDGER.yaml).

Transfer failures use the same policy and are added here with their TR reason
codes.

## Mathematical negative findings — added 2026-10-06

The table above preserves the 10/5 operational snapshot. The findings below
index the existing [P2 obstruction study](M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md),
not a new compile or independent mathematical reproduction.

| candidate/hypothesis | scoped result | evidence and limitation |
| --- | --- | --- |
| `Q = J / (M H)` as a globally admissible radial ratio | `claim_status: FALSIFIED` for that global-use proposal | P2-A: pinned `OutgoingDilation.after_pulse` gives `M = J = 0` for `XR > 0`, `X > 0`, `pulseEndRadius <= X`. The ratio's required nonzero denominator fails. This is not a claim that the source theorem is false. |
| pulse endpoint is the first mass zero | `claim_status: FALSIFIED` as stated | P2-C2/C3: for local radius `upper(1) < r < exp(pulseLength)`, support vanishes; exact endpoint cancellation makes `M_pulse = 0` throughout that nonempty terminal interval. This is a source-located algebraic consequence, not a newly compiled NSRW theorem. |
| small-positive-eta first-repair interior zero | `claim_status: SUPPORTED`; formal closure open | P2-C4a/C4b comparison, coefficient-continuity and tail argument. It is not promoted by the preceding negative findings or the L1/F1/L2-A receipts. |

Here `Q` is the prospective quotient **restricted to `M H != 0`**, as defined
in the study. Lean's totalized real division does not remove that admissibility
condition or make the quotient a useful global invariant.

Reopening the ratio proposal requires an explicitly restricted domain or a
different quantity; a later compile does not remove these denominator zeros.
The rejected endpoint-first-zero wording stays rejected even if a sharper
description of the actual zero set is later proved.

Compiler errors, missing dependencies, hash mismatches, and unavailable runtimes
are execution/admission outcomes, not mathematical counterexamples. A later
successful run does not erase them or automatically refute the intended claim.
