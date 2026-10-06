# Equation to Artifact — vision and roadmap

Document status: `ADOPTED`
Scope: long-range program roadmap; not an execution gate.

## 1. Vision

Equation to Artifact is a Flamehaven research program for turning mathematical
and scientific claims into source-bound executable artifacts, and then testing
whether any surviving structure can become a useful computational primitive.

The program has two connected arcs:

~~~text
Equation -> Artifact
Artifact -> Application
~~~

The first arc is claim custody. The second is technological translation.

The second arc may begin only from an explicitly identified claim and artifact.
Application ambition does not widen an unverified mathematical claim.

## 2. Why code is central

Code does not acquire mathematical authority by implementation.

Its role is to convert an implicit claim surface into an inspectable object
with explicit inputs, transformations, precision, outputs, failure states,
reproduction commands, and later integration points.

A conventional translation path can require:

~~~text
paper
 -> interpretation
 -> mathematical implementation
 -> numerical implementation
 -> software interface
 -> prototype
~~~

Equation to Artifact attempts to move some of that translation earlier:

~~~text
paper
 -> source-bound executable artifact
 -> falsifiable operational surface
 -> computational primitive candidate
 -> controlled transfer
~~~

The benefit is earlier testability, including earlier rejection.

## 3. Canonical lifecycle

The R-axis is the high-level lifecycle. OE and TR are evidence/maturity axes
mapped to it in `E2A_RESOURCE_STAGE_CROSSWALK.md`.

~~~text
R0   SOURCE
     exact paper, theorem, equation, declaration, or scientific claim

R1   MODEL
     exact mathematical object, hypotheses, and expected consequence

R2   CHECK DESIGN
     independent derivation, semantic comparison, expected output,
     falsifier specification
     # falsifiers may be designed here but are not yet counted as OE-4 evidence

R3   ARTIFACT
     code, tests, manifest, pinned environment, receipt surface
     -> candidate for OE-2 after actual execution

R4   CLEAN REPRODUCTION
     operationally separate clean replay under declared admission rules
     -> candidate for OE-3

R5   FALSIFICATION
     mutation/drift/assumption failures behave as declared
     -> candidate for OE-4

R6   PRIMITIVE EXTRACTION
     bounded reusable interface
     -> TR-0

R7   RELEVANCE SCREEN
     explicit target-model correspondence and named baseline
     -> TR-1

R8   CONTROLLED TRANSFER
     toy/benchmark problem, precision and resolution stress tests
     -> TR-2

R9   COMPARATIVE BENCHMARK
     preregistered baseline, event definition, metrics, thresholds
     -> TR-3

R10  PROTOTYPE INTEGRATION
     versioned integration into a real solver or scientific workflow
     -> TR-4

R11  DOMAIN VALIDATION
     domain constraints, independent domain review, accepted baselines
     -> TR-5

R12  OPERATIONAL FEASIBILITY
     reliability, cost, monitoring, security, safety, workflow fit
     -> TR-6

R13  DEPLOYMENT
     actual operational adoption under the relevant engineering regime
~~~

A project can stop legitimately at any stage. A failed transfer can be a
valuable result if it eliminates an implausible application early.

## 4. Two long-range objectives

### Mathematical objective

Move beyond source reproduction toward at least one independent, nontrivial,
bounded mathematical result with clear source lineage and executable/formal
custody.

Legitimate outputs include a new lemma, obstruction, no-go result, stability
estimate, restricted-parameter theorem, counterexample, or independently
checked construction component.

For NSRW, a Millennium-level solution remains an aspiration, not a forecast.

### Translational objective

Convert at least one mathematically validated structure into a reusable
computational primitive and determine, under controlled comparison, whether it
adds measurable value in a real scientific or engineering domain.

A useful technology contribution does not require solving the top-level
mathematical problem.

## 5. What may transfer

The most plausible transferable object is usually smaller than the theorem.

| Mathematical/artifact structure | Candidate primitive |
| --- | --- |
| anisotropic scaling law | scale-change signal |
| normalized ratio | regime indicator |
| concentration rate | extreme-event feature |
| residual identity | simulation-integrity monitor |
| dynamic rescaling | adaptive numerical microscope |
| exact inequality | runtime invariant or guard |
| support/zero-set geometry | activation/domain condition |
| formal hypothesis set | admission precondition |
| mutation/falsifier | regression or safety test |
| evidence graph | scientific-model provenance layer |

Every row is a hypothesis until its lineage and transfer gates exist.

## 6. Two transfer branches

### Scientific primitive branch

A mathematical result produces a detector, invariant, residual, rescaling
operator, or solver component.

This branch preserves the original PDE/scientific vision but normally requires
more mathematical closure before TR-0.

### Infrastructure primitive branch

Existing artifact machinery may itself become a reusable primitive, for
example:

- evidence/provenance graph;
- source-to-artifact identity binding;
- mutation/falsifier regime;
- scientific-model regression guard.

This branch can enter TR-0 earlier if its lineage already exists. It does not
substitute for the mathematical objective and must be evaluated against existing
provenance and regression-testing baselines.

## 7. Transfer lineage and transformation boundary

Every positive application experiment must preserve:

~~~text
source claim_id
  -> mathematical result claim_id
  -> executable artifact identity
  -> primitive version
  -> domain adapter version
  -> benchmark identity
  -> observed metrics
  -> boundary / non-claims
~~~

If approximation, discretization, nondimensionalization, surrogate use, or a
domain adapter changes the object, that transformation creates a new custody
boundary and requires a new claim/resource identity.

## 8. Failure-first translation

Before building a product, search for the cheapest falsifier.

Questions include:

- Is the required quantity observable?
- Does it have dynamic range on regular as well as extreme cases?
- Is it stable under resolution and timestep changes?
- Is it robust to realistic noise?
- Does finite precision destroy the signal?
- Does it add information beyond a named baseline?
- Is it cheap enough to use?
- Does it trigger early enough to change an action?

A negative answer is recorded, not hidden.

## 9. Current NSRW route

The active mathematical route remains:

~~~text
strict L2 compile
   -> L3
   -> DeltaM < 0
   -> repair-coefficient sign
   -> first-repair zero
~~~

The dated status of those claims is not stored in this roadmap. It lives in
`CURRENT_POSITION_2026-10-05.md` and
`E2A_RESOURCE_CLAIM_LEDGER.yaml`.

This separation keeps the roadmap stable while execution status changes.

## 10. Progress representation

The program does not use hand-written completion percentages.

Different rows have different denominators, and open mathematical research has
no defensible linear completion percentage.

Progress is represented by:

- atomic claim status;
- OE level;
- evidence class;
- TR gate state;
- dated receipts;
- explicit HELD/UNVERIFIED/CONTRADICTED entries;
- negative-result records.

Any future count or percentage must be generated from the claim ledger with a
published formula and weights.

## 11. External audit as a program asset

External audit is valuable when it finds mismatches that the artifact authors
can miss: stale state, vocabulary drift, missing lineage, source-pin gaps,
self-authorizing evidence, or application claims that outrun their support.

The audit itself does not inherit authority over the theorem. If the auditor
did not inspect the primary source or reproduce the execution, the result is a
structural review, not mathematical confirmation.

## 12. Vision statement

> Equation to Artifact turns checkable mathematical and scientific claims into
> source-bound executable objects. It then asks which objects survive
> falsification, which can become reusable computational primitives, and which
> survive real scientific and engineering constraints.

The custody principle remains:

> A proof establishes the theorem. An executable artifact exposes a checkable
> surface. A transfer experiment determines whether that exposed surface has
> utility outside its original claim.
