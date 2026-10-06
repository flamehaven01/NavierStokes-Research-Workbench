# Equation to Artifact stage crosswalk

Document status: `ADOPTED`
Scope: single mapping source for R, OE, TR, NSRW M, and execution T terminology.

## 1. Why this exists

The project uses several axes for different purposes. They are not interchangeable.

- `R`: end-to-end lifecycle;
- `OE`: operational exposure of a claim/artifact;
- `TR`: application-transfer gates;
- `M`: NSRW research milestones;
- `T`: dated execution tasks;
- `A`: safety/hardening tasks.

A claim must not be promoted merely because a different axis has advanced.

## 2. Canonical mapping

| R stage | Meaning | OE/TR relation |
| --- | --- | --- |
| R0 SOURCE | pinned source and locator | OE-0 |
| R1 MODEL | represented object/hypotheses | OE-1 |
| R2 CHECK DESIGN | derivation, expected result, falsifier specification | remains OE-1 until execution |
| R3 ARTIFACT | executable artifact and first bounded run | candidate OE-2 |
| R4 CLEAN REPRODUCTION | operationally separate clean replay | candidate OE-3 |
| R5 FALSIFICATION | declared mutations/drift fail visibly | candidate OE-4 |
| R6 PRIMITIVE EXTRACTION | reusable bounded interface | TR-0 |
| R7 RELEVANCE SCREEN | target correspondence + baseline + domain review | TR-1 |
| R8 CONTROLLED TRANSFER | toy/controlled benchmark | TR-2 |
| R9 COMPARATIVE BENCHMARK | preregistered incremental-value test | TR-3 |
| R10 PROTOTYPE | real solver/workflow integration | TR-4 |
| R11 DOMAIN VALIDATION | target-domain evidence | TR-5 |
| R12 OPERATIONAL FEASIBILITY | deployment-readiness review | TR-6 |
| R13 DEPLOYMENT | actual operational use | outside TR gate numbering |

## 3. Resolved conflicts

### Falsifier ordering

R2 may define a falsifier before code exists. That is **falsifier design**, not
OE-4 evidence.

OE-4 is reached only after an executable artifact exists and the declared
mutation/drift tests actually fail as expected.

An expected mutation rejection is evidence about the artifact's detection
surface, not a counterexample to a mathematical theorem. A compile or identity
failure blocks admission of that run; it does not by itself falsify the intended
proposition.

### Operational exposure

R4 is no longer a single catch-all "operational exposure" stage.

Operational exposure is the OE axis:

~~~text
OE-0 cited
OE-1 represented
OE-2 executed
OE-3 reproduced
OE-4 falsifiable
~~~

### Comparative benchmark vs prototype

TR-3 is a separate preregistered comparative benchmark.

TR-4 is prototype integration.

Metrics such as false-positive rate, detection lead time, and equal-compute
comparison belong to TR-3 unless they are repeated later as prototype
monitoring.

## 4. NSRW M milestones

M milestones describe research packages, not generic maturity.

One M milestone can contain claims at several OE levels.

Therefore no mapping such as `M5 = OE-3` is valid.

Current M status belongs in the dated snapshot and claim ledger.

## 5. T and A tasks

T tasks are execution order.

For the current strict-L2 route:

~~~text
T0 executor observation
T1 bridge/strict separation
T2 dependency-chain preparation
T3 development compile
T4 clean authority replay
T5 receipt synchronization
T6 begin L3
~~~

These tasks move one or more claim records but are not themselves maturity
levels.

A tasks are hardening/backlog work and may run in parallel without changing a
mathematical claim.

## 6. Admission rule

The atomic claim ledger is a reading index, not the highest evidence authority.
Start there to find the claim, source locator, boundary, and dated receipt.

When documents disagree:

- mathematical meaning is checked against the exact pinned source/proposition
  and its hypotheses;
- execution facts are checked against the identified run's artifacts and
  byte-bound receipt, not a summary status in the ledger;
- the dated snapshot is a planning view; this crosswalk and stable policies
  define terminology and rules, not proof or execution results.

Keep the affected claim/run admission held while a material conflict is
unresolved. Correct the derived ledger or snapshot after comparing the evidence;
do not let a ledger entry authorize itself or erase a contradictory result.

Historical records are never rewritten to imitate current state.
