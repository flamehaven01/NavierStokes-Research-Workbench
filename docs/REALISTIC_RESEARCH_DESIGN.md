# Realistic Research Design From the Current Navier--Stokes Verification Structure

Status: `PROPOSED`

## 1. Realistic objective

The next objective should not be stated as "solve Navier--Stokes again." The realistic objective is to reduce the largest remaining uncertainty between four distinct artifacts:

1. the primary PDF;
2. the lossy Markdown transport;
3. the Lean formal source at the pinned commit;
4. the executable workbench receipts.

The workbench already answers identity, scope, locator, mutation, and graph-integrity questions. It does not yet answer whether the Lean project builds in a pinned environment, whether each formal predicate matches the corresponding paper hypothesis, or whether the critical analytic estimates are independently correct. Those are the next useful targets.

## 2. What we can credibly achieve

### Track A -- Reproducible formal build

Goal: produce a build receipt for the pinned OpenAI commit in an isolated, documented Lean environment.

Deliverables:

- exact Lean/Lake toolchain version and dependency lock identity;
- clean build log and exit status;
- imported axiom inventory for the two top-level breakdown declarations;
- declaration dependency graph generated from the build, not inferred only from filenames;
- deterministic rebuild check on a second clean workspace.

Success means `CONFIRMED[build:<commit,toolchain>]`. It does not mean the paper and Lean statement are semantically equivalent.

### Track B -- Paper-to-Lean semantic alignment

Goal: convert the current locator crosswalk into an obligation-by-obligation comparison.

For each critical theorem or proposition, record:

- paper statement from the PDF page image, not only the damaged Markdown;
- Lean declaration and all explicit/implicit parameters;
- hypothesis correspondence;
- conclusion correspondence;
- strengthened, weakened, omitted, or representation-only differences;
- reviewer status and unresolved question.

Start with the smallest high-value spine:

1. Theorem 1.1 and the forced (C)/(D) boundary;
2. Theorem 3.1 reduction;
3. Theorem 4.6 construction theorem;
4. Proposition 8.3 all-order correction;
5. Propositions 9.6 and 9.9 localization/forcing;
6. Proposition 10.1 and Corollary 10.6;
7. `selected_candidate` and the two comparator breakdown theorems.

Success means a measured coverage ratio and a list of unresolved semantic bridges. It is not a binary proof-validity badge.

### Track C -- Independent checking of bounded subclaims

Goal: independently reconstruct selected high-risk local lemmas without attempting the complete 167-page argument at once.

Good first candidates are claims with compact inputs and observable outputs:

- scaling identities used by the self-similar ansatz;
- divergence-free and support properties of localized fields;
- energy and vorticity-norm transformations under rescaling;
- algebraic properties of the oscillatory covariance/stress construction;
- bookkeeping invariants in the all-order correction step.

Each candidate should have three implementations where practical:

- a direct mathematical derivation;
- a small symbolic or numerical diagnostic;
- a Lean theorem or executable checker.

Agreement increases confidence in the bounded subclaim. Numerical agreement remains diagnostic and cannot prove an infinite-dimensional estimate.

### Track D -- Adversarial falsification

Goal: search for the cheapest counterexample to the architecture before investing in complete reformalization.

Extend the current five mutations with:

- parameter-sign and scaling-exponent mutations;
- compact-support versus rapid-decay substitution;
- periodic versus whole-space domain substitution;
- pointwise versus time-integrated BKM quantity substitution;
- forcing regularity or support weakening;
- removal of a dependency edge from the critical proof graph;
- replacement of a proved declaration by an axiom or opaque assumption;
- source-version and locator drift.

Every surviving mutation becomes a defect in the workbench or a missing mathematical discriminator. A killed mutation is evidence about the checker, not evidence that the theorem is true.

## 3. Research questions worth attempting

### RQ1 -- Which bridges carry most of the proof risk?

Measure graph fan-in, theorem dependency depth, statement complexity, source-loss exposure, and semantic-review status. Use these measurements to rank review effort. The expected output is a risk-ranked obligation list, not an automated correctness score.

### RQ2 -- How robust is the construction to its exact hypotheses?

Construct a hypothesis sensitivity table. Vary one condition at a time and record where the paper or Lean graph first fails. Promising dimensions include forcing support, smoothness, spatial domain, symmetry assumptions, scale separation, and error-order requirements.

This can reveal which assumptions are structurally essential and which may be artifacts of the chosen construction. Any proposed weakening remains a conjecture until analytically proved.

### RQ3 -- Can a critical analytic module be independently minimized?

Select one module, such as oscillatory stress realization or localization, and build a minimal theorem contract containing only its definitions, assumptions, conclusion, and dependencies. Reprove or refute that isolated contract. This is far more realistic than immediately reproducing the complete proof.

### RQ4 -- Does the formal graph contain hidden authority shortcuts?

Audit for axioms, trusted opaque declarations, classical-choice dependencies, imported results whose hypotheses exceed the paper statement, and checks that are only static text matches. The output should distinguish ordinary foundational axioms from project-specific unproved assumptions.

### RQ5 -- Can the architecture generate a genuinely new bounded result?

Only after Tracks A--D are stable, test modest extensions:

- a quantitative stability lemma for one constructed component;
- a sharper explicit constant in one localization or energy estimate;
- a reusable formal library lemma extracted from the proof;
- a formally checked statement about a restricted parameter family.

These are credible research contributions even if they do not extend the top-level blowup theorem.

## 4. Proposed execution phases and gates

### Phase R0 -- Source recovery index

- Render only the PDF pages needed by the critical spine.
- Register every display equation with page, bounding box, image hash, OCR status, and manual transcription status.
- Never fill missing formulas from model memory.

Gate: all critical statements are either recovered from the PDF image or explicitly `UNKNOWN`.

### Phase R1 -- Lean build reproducibility

- Establish the exact toolchain in an isolated environment after separate installation authorization.
- Build from a clean checkout at the pinned commit.
- capture top-level declarations, axioms, and dependency data.

Gate: two clean rebuilds agree and no source file changed.

### Phase R2 -- Semantic spine audit

- Complete the seven-item paper-to-Lean spine.
- Require two fields for every bridge: correspondence evidence and remaining falsifier.
- Do not use declaration-name similarity as semantic evidence.

Gate: 100% of spine obligations are reviewed; unresolved items remain `PARTIAL` or `UNVERIFIED`.

### Phase R3 -- Independent bounded reconstruction

- Choose one high-risk but compact module.
- Write an independent theorem contract and negative fixtures.
- Implement symbolic/numerical diagnostics and a formal proof attempt.

Gate: the bounded module is either independently supported, falsified, or held with a precise missing lemma.

### Phase R4 -- Adversarial review

- Run the expanded mutation bank.
- Introduce source drift, graph-edge loss, and authority-forgery cases.
- Obtain an independent mathematical review for any proposed semantic PASS.

Gate: no blocking mutation survives and no self-attested status can become authoritative.

### Phase R5 -- Publishable research package

- Publish only claims supported by the completed phases.
- Separate build reproducibility, semantic alignment, bounded reproof, and novel result sections.
- Include all negative results and unresolved falsifiers.

Gate: release status remains `HELD` until provenance, licensing, independent review, and publication authority are complete.

## 5. Recommended first experiment

The best first research experiment is a minimal semantic/build audit of Proposition 10.1 and `selected_candidate`.

Why this pair:

- it lies near the end of the paper construction and has high downstream impact;
- it connects the analytic construction to the formal witness used by the comparator theorem;
- the current graph already identifies it as a convergent dependency point;
- a mismatch here would invalidate broad downstream confidence early;
- a successful bounded reconstruction would create reusable tooling for the remaining spine.

Concrete output:

1. exact PDF statement image and transcription;
2. Lean signature with expanded implicit assumptions;
3. dependency and axiom report;
4. hypothesis/conclusion comparison table;
5. at least five targeted mutations;
6. an independent derivation or a precise list of missing lemmas;
7. a receipt whose strongest possible status is scoped to this pair.

## 6. Stop conditions

Pause the research rather than widening claims if any of these occurs:

- the PDF statement cannot be recovered reliably;
- the pinned Lean project cannot be rebuilt;
- a formal declaration uses materially different hypotheses;
- a required result is axiomatized or externally trusted without a recorded boundary;
- a blocking mutation survives;
- numerical evidence is being used to replace an analytic estimate;
- a single reviewer or the workbench itself is the only authority for semantic equivalence.

The practical near-term target is therefore an independently inspectable build and semantic audit, followed by one bounded subproof. A new top-level Navier--Stokes result is a long-horizon possibility, not the next-stage deliverable.
