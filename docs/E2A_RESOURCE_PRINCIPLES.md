# Equation to Artifact resource principles

Document status: `ADOPTED`
Scope: canonical resource charter.

## Core rules

1. **Source authority stays with the source.** A resource must identify the
   paper, formal repository, version/commit, and locator it depends on.

2. **The resource owns only its checkable surface.** Code, tests, and receipts
   do not inherit the scope of the surrounding theorem.

3. **Operational exposure is not theorem verification.** Execution makes a
   bounded consequence observable; it does not make the theorem more true.

4. **No upward inheritance of authority.**

   ~~~text
   proof != witness != reproduction != transfer != domain utility != deployment
   ~~~

5. **Transformation creates a new custody boundary.** Approximation,
   discretization, nondimensionalization, surrogate substitution, domain
   adaptation, or changed hypotheses require a new identity and scope.

6. **The registration unit is the atomic claim.** Documents are views over
   claims and may contain multiple statuses.

7. **Failure is a valid resource result.** `HELD`, `UNVERIFIED`,
   `CONTRADICTED`, and `TRANSFER_FAILED[...]` are first-class outcomes.

8. **Evidence type and operational level are separate.** A historical external
   compile, local clean compile, numerical reconstruction, static review, and
   independent replay are not flattened into one score.

9. **Time is part of status.** Reusable status claims carry `valid_as_of` or
   point to a dated receipt/snapshot.

10. **Application claims require new empirical evidence.** A rigorous theorem
    does not authorize an engineering claim.

## External audit

External audit is valuable because it can find structural defects that artifact
authors miss: stale state, vocabulary drift, unsupported status inheritance,
missing pins, missing lineage, and self-authorizing evidence.

The audit's own boundary must be recorded.

If the auditor did not inspect the primary source or replay the execution, the
audit is structural consistency evidence, not mathematical confirmation.

A separate LLM role inside the same trust domain is not independent proof
authority.

## Hallucination/slop discipline

Resource prose should be executable in spirit:

- one stateful claim per sentence where practical;
- claim_id or receipt for promoted states;
- enum status instead of vague modal language;
- source pin plus locator instead of memory-based citation;
- no hand-written progress percentage without a published generator;
- no invented witness when evidence is absent;
- application language remains a hypothesis without TR evidence;
- style edits must preserve IDs, hashes, status tokens, and numbers.

The desired enforcement target is build-failing lint plus mutation tests.

Current enforcement status: `DOCUMENTED_ONLY`.

No claim is made that these rules are already enforced by CI.

## Canonical principle

> Equation to Artifact does not move authority from paper to code. It makes the
> boundary between them executable.
