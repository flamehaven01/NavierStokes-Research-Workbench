# Public research language guide

Document status: `ADOPTED`
Scope: public-facing wording policy.

## 1. Scope

Internal resource terminology and public summary terminology are not identical.

Terms such as `claim custody`, `North Pole`, `north-star map`, and
`independent lane` may be used internally when they are defined. Public
summaries should prefer observable descriptions such as evidence traceability,
research objective, research direction map, and separate research direction.

This resolves a terminology distinction rather than banning the internal terms.

## 2. Project position

NSRW is an open research-lab workbench using pinned sources, explicit
mathematical questions, reproducible checks, reviewable evidence, and explicit
limits.

It is not presented as a claimed solution, an inherited OpenAI proof, or a
general-purpose verification authority.

The source paper and formal repository remain research inputs. The project does
not inherit their authority.

## 3. Preferred public wording

| Prefer | Avoid without definition | Reason |
| --- | --- | --- |
| evidence traceability | claim custody | describes the observable record |
| required validation | hard gate | avoids implying institutional authority |
| source/check comparison | quantifier custody | names the actual comparison |
| negative control or mutation test | falsification engine | separates software testing from theorem refutation |
| secondary structural consistency check | semantic AI reviewer | keeps LLM review bounded |
| research direction | independent lane | avoids implying completed independence |
| research direction map | north-star map | clearer outside the project |
| do not invent missing evidence | slogan-only language | makes the rule operational |

Historical schema keys, identifiers, receipts, and filenames remain unchanged
when renaming would break provenance.

## 4. Status discipline

In resource documents, a sentence that promotes a bounded result should point
to a `claim_id` or receipt.

Avoid unqualified evidence verbs such as:

~~~text
verified
proved
confirmed
established
reproduced
~~~

unless the exact scope follows from the claim record.

Examples:

~~~text
CONFIRMED[claim_id=nsrw/p2/f1/mainmoment-one-pos]
HELD[NO_NUMERICAL_EVALUATOR]
UNVERIFIED[NO_COMPILED_RECEIPT_CURRENT_BYTES]
~~~

A Lean compile establishes elaboration of the requested target under the
recorded environment. It does not establish paper correctness or paper--Lean
semantic equivalence.

A numerical sample is a bounded observation, not a theorem.

## 5. Time language

Avoid unqualified `current`, `now`, `mature`, or similar state language in
reusable resources.

State claims should include `valid_as_of` or point to a dated snapshot.

Historical receipts remain historical even when later source files change.

## 6. Application language

Application ideas remain hypotheses until the corresponding TR gate executes.

Prefer:

- "candidate computational primitive";
- "possible transfer question";
- "controlled benchmark";
- "domain validation remains open";
- "unanchored hypothesis" when lineage is missing.

Avoid before evidence exists:

- "improves weather forecasting";
- "predicts cyclone tracks";
- "creates a semiconductor breakthrough";
- "validated for industrial use";
- "the theorem is directly applicable to this domain."

A rigorous mathematical origin does not transfer proof authority into an
engineering claim.

## 7. External and LLM review language

An external reviewer who has not checked the primary source/runtime may be
credited for structural findings, not mathematical confirmation.

LLM review is described as a **secondary structural consistency check** unless
the claimed evidence is supplied by a separate compiler, verifier, experiment,
or human expert review.

"Independent review" requires an actually separate trust/operational boundary;
separate roles inside one shared session are not described as independent.

## 8. Planned enforcement

The following rules are adopted for future resource linting:

- status-promoting sentences require claim_id or receipt linkage;
- source locators require a source pin;
- hand-written percentages are prohibited unless generated from a published
  formula;
- application claims without TR evidence remain hypotheses;
- style edits must not silently change claim_id, hashes, status tokens, or
  numbers;
- mutation tests should include intentionally false documentation states.

As of this document, these are documentation requirements. They are not claimed
as CI-enforced until a linter and its mutation tests exist.

## 9. Release review

Before a public release:

1. compare README, release notes, active design documents, ledger, and receipts;
2. distinguish current implementation, historical evidence, and future work;
3. check every status claim against its claim_id;
4. preserve source pins and artifact identities;
5. check application wording against TR state;
6. remove private local paths, identities, credentials, and environment details.
