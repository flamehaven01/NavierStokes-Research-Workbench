# Operationally exposed: from mathematical existence to inspectable execution

Document status: `ADOPTED`
Scope: Equation to Artifact resource concept; not a theorem-status label.

## 1. Purpose

Equation to Artifact starts from a practical observation: a paper can state an
equation, theorem, construction, or numerical relation while leaving much of
its operational surface implicit. Code can make part of that surface
inspectable.

In this project, **operationally exposed** means that a narrow mathematical or
scientific object has enough executable structure that a third party can supply
declared inputs, run a declared procedure, observe outputs, test failure
conditions, and trace those observations back to an identified source claim.

Operational exposure is stronger than quotation or static representation. It is
weaker than proving the whole theorem, establishing paper--code semantic
equivalence, or validating a technology.

The phrase is project terminology. It does not replace the mathematical meaning
of existence and does not imply constructivity in the proof-theoretic sense.

## 2. Four distinct layers

### 2.1 Mathematical existence

A theorem may establish:

~~~text
exists x, P(x)
~~~

without exposing a computational interface that produces a concrete numerical
witness.

The theorem and its mathematical authority belong to the original result and
its authors.

### 2.2 Representational availability

A paper formula, formal declaration, symbolic construction, or pinned source
definition may represent an object precisely enough to inspect.

Representation alone does not imply that the object is executable or
numerically available.

### 2.3 Operational exposure

A checkable surface is operationally exposed when its resource record identifies
at minimum:

- source identity and locator;
- atomic claim or mathematical object;
- hypotheses and admissible inputs;
- artifact identity or content hash;
- environment and dependency identity;
- reproduction command or bounded executable procedure;
- expected output, tolerance, or invariant;
- failure condition or falsifier;
- evidence class;
- non-claims and scope boundary.

A typical custody chain is:

~~~text
source statement
      |
      v
source-bound mathematical object
      |
      v
executable representation
      |
      v
input -> computation -> observable output
      |
      v
falsifier / drift detector / receipt
~~~

The artifact does not create theorem truth. It exposes a bounded part of the
theorem or model to execution.

### 2.4 Technological realization

A computational primitive becomes a technology only after it survives a
different class of evidence:

- relevance to a real domain;
- implementation feasibility;
- robustness to discretization and noise;
- comparison with a named baseline;
- domain-specific validation;
- operational constraints;
- deployment and maintenance.

A successful Lean compile or numerical reconstruction is not technological
validation.

## 3. No automatic inheritance of authority

Equation to Artifact uses the following non-implication rule:

~~~text
mathematical existence
    != computational witness
    != reproducibility
    != transferability
    != domain utility
    != deployment
~~~

More precisely, none of the following implications is automatic:

~~~text
proof -> executable witness
compile -> paper/Lean semantic equivalence
reproduction -> transferability
toy transfer -> domain validation
domain validation -> deployment
~~~

Authority does not flow upward merely because adjacent layers are connected.

A mathematically deep result may remain only representationally available.
Conversely, a simple diagnostic may be highly reproducible without carrying
the authority of a theorem.

## 4. Transformation creates a new custody boundary

Any transformation that materially changes the mathematical or computational
object creates a new custody boundary.

Examples include:

- approximation;
- discretization;
- nondimensionalization;
- surrogate replacement;
- precision reduction;
- coordinate or variable reinterpretation;
- domain adapter;
- changed boundary conditions;
- changed hypotheses.

The transformed object must receive its own identity, assumptions, tests,
evidence class, and claim scope. Source authority is not inherited across an
unrecorded transformation.

## 5. Why code matters

A paper can leave practical questions latent:

~~~text
Which inputs are admissible?
Which quantities are actually computable?
What precision is required?
What changes if one assumption is removed?
Where does the relation fail?
Can the quantity be monitored inside a simulation?
Can another implementation reproduce it?
~~~

Code can turn some of those questions into executable tests.

For Equation to Artifact, code is therefore more than a publication appendix.
The research process can operate on executable representations:

~~~text
theory
  -> executable representation
  -> research on the executable boundary
  -> executable result
~~~

The practical advantage is not that code makes a theorem more true.

> It makes more consequences testable earlier.

An artifact is not merely an implementation of a result. It is an interface
through which a bounded result can be inspected, challenged, composed, and,
when justified, considered for transfer.

## 6. Relation to the measurement intuition

Code can be treated as a measurement interface only in a limited operational
sense: it forces a claim to meet explicit inputs, outputs, tolerances,
dependencies, and failure states.

Quantum measurement, wave-particle duality, and the Schrödinger-cat thought
experiment have specific physical meanings. Equation to Artifact does not claim
that execution reproduces those phenomena or changes mathematical truth.

The bounded analogy is:

> A statement can remain abstract until an interface makes some consequence of
> it observable under declared conditions.

The project therefore uses **operational exposure**, not "code proves
existence."

## 7. Operational exposure levels

Operational exposure stops at falsifiable executable custody. Transfer and
deployment use a separate TR axis.

~~~text
OE-0  CITED
      Source statement and locator are identified.

OE-1  REPRESENTED
      Definitions, hypotheses, expected output, and non-claims are represented.

OE-2  EXECUTED
      A bounded implementation has executed under a declared environment and
      the exact artifact/evidence identity is recorded.

OE-3  REPRODUCED
      An operationally separate reproducer performs a clean execution and
      reproduces the bounded result under the declared admission rules.

OE-4  FALSIFIABLE
      Declared mutations, drift, or violated assumptions produce visible and
      expected failure.
~~~

These levels are not proof levels and do not encode evidence type.

Evidence class is a separate axis, for example:

~~~text
source-located derivation
reviewed-static
local clean compile
external clean compile
bounded numerical reconstruction
historical receipt
independent replay
secondary structural review
~~~

An artifact should be described by both axes, not by OE level alone.

After OE-4, a stable artifact may be admitted to `TR-0` primitive extraction
under `ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md`.

## 8. Claim-level resource rule

The registration unit is an atomic claim, not an entire document.

A document may contain confirmed, supported, held, and open statements at the
same time. It therefore cannot safely inherit a single scientific status.

Each reusable resource claim should carry:

~~~text
resource_id
version
valid_as_of
status
source_pin
claim
claim_type
gate_state
oe_level
evidence_class
receipt
non_claims
falsifier
admission_failure
reopening_condition
lineage
reverify_on
~~~

The canonical machine-readable view for the current NSRW resource set is
`E2A_RESOURCE_CLAIM_LEDGER.yaml`.

The ledger is an evidence index, not an authority above the pinned proposition
or its run-bound evidence. Its `falsifier` specifies a claim-domain contradiction
or bounded numerical failure; `admission_failure` specifies why a run cannot be
accepted; `reopening_condition` specifies what would allow held work to resume.
These are not interchangeable. A null falsifier means none is specified in that
record, not that the claim is immune to challenge. Listing a condition does not
mean it has been observed or tested.

## 9. External audit and separate-role review

External or separate-role review is valuable because it can expose:

- status drift between documents;
- missing source pins;
- conflicting stage vocabularies;
- self-authorizing evidence;
- missing lineage;
- undocumented transformations;
- unsupported application language;
- stale or non-reproducible state claims.

Its authority must also be bounded.

A reviewer who has not independently checked the source, runtime, or receipt
may establish structural consistency findings, but not the truth of the
underlying mathematical claim.

LLM review is recorded only as a secondary structural consistency check unless
a separate non-LLM evidence path supplies the actual evidence.

## 10. Navier--Stokes example

For NSRW, a pinned source may define an object and the workbench may expose one
local identity, scaling relation, moment comparison, or formal proposition:

~~~text
source definition
    -> source-bound mathematical relation
    -> executable representation
    -> bounded execution
    -> falsifier / receipt
~~~

That chain exposes a narrow surface. It does not establish the complete
Navier--Stokes theorem.

A formal existential witness may remain mathematically valid while a numerical
evaluator is unavailable. In that case the executable status remains `HELD` or
`UNVERIFIED`; a concrete witness is not invented.

## 11. Boundary

Operational exposure does **not** mean:

- the whole theorem has been verified;
- a proof has become a product;
- a source-defined construction is numerically available unless a witness is
  actually exposed;
- a mathematical singularity result improves weather prediction;
- a fluid-mechanics identity transfers automatically to semiconductor physics;
- a prototype has been validated because its mathematical origin is rigorous.

## 12. Project principle

> A proof establishes the theorem. An executable artifact exposes a checkable
> surface. A transfer experiment tests whether that surface can become a useful
> computational primitive.

Equation to Artifact does not move authority from paper to code. It makes the
boundary between them executable.
