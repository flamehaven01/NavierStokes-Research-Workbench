# Public research language guide

Status: active documentation policy

This project is written for mathematicians, formal-methods researchers,
scientific-computing researchers, and software reviewers. Public documentation
should describe observable work before introducing an internal stage name or
implementation label.

## Project position

NSRW is an open research-lab workbench. It supports a team-level research
process: pinned sources, explicit mathematical questions, reproducible checks,
reviewable evidence, and clear limits. It is not presented as a lone
researcher's claimed solution, an OpenAI derivative proof, or a general-purpose
verification authority.

The OpenAI manuscript and Lean repository are research inputs. The project may
reproduce selected surfaces, challenge assumptions, and build different future
research directions, but it does not inherit the truth or authority of those
sources.

## Preferred wording

| Prefer | Avoid in public summaries | Reason |
|---|---|---|
| evidence traceability | claim custody | describes the observable record directly |
| required validation | hard gate | avoids implying institutional or proof authority |
| source/check comparison | quantifier custody | states exactly what the implementation compares |
| negative control or mutation test | falsification engine | distinguishes software tests from theorem refutation |
| secondary structural consistency check | SPAR frame, semantic AI reviewer | names the limited function before the dependency |
| research direction | independent lane | avoids implying completed independent reproduction |
| research direction map | north-star map | clearer to readers outside the project |
| do not invent missing evidence | `ABSTAIN > FABRICATE` | plain-language policy rather than a slogan |

Schema keys, Python identifiers, historical receipts, and package names remain
unchanged when renaming them would break replay or provenance. When such a term
appears, documentation should explain its narrow operational meaning.

## Status discipline

- A software check can establish only the scope it executed.
- A Lean build establishes successful elaboration of the requested target, not
  paper correctness or paper--Lean semantic equivalence.
- A numerical sample or manufactured input is a bounded control, not a theorem.
- A historical replay establishes deterministic interpretation of a recorded
  artifact, not current source freshness.
- `HELD` and `UNVERIFIED` are valid research outcomes when evidence is missing.

## Release review

Before a public release:

1. check README, changelog, release notes, active design documents, and current
   receipts for contradictory status claims;
2. distinguish current implementation, historical records, and future work;
3. replace unexplained internal language in public summaries;
4. preserve exact schema identifiers and historical evidence hashes;
5. confirm that no local path, user identity, credential, or private environment
   detail appears in public artifacts.
