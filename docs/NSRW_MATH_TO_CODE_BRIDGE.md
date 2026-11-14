# From Lean results to a numerical moment certificate

Snapshot: 31 October 2026; next work reassessed on 12 November 2026. See the
[current position and executable next tasks](CURRENT_POSITION_2026-11-02.md).
This is the canonical public architecture explanation.
The NSRW repository owns executable code, mathematical definitions and this
roadmap. Flamehaven Verification Ledger publishes a referenced execution record.

## Established mathematical branch

The pinned outgoing Profile supplies the source M and J objects. Z-core and
Z+J connect a first-window mass zero to positive angular history at that same
point. The quantitative branch supplies a root-location-independent local J
margin and a normalized plateau lower bound.

These are exact-real Lean results. Their receipt links and exact checkpoints
are in the [research guide](NSRW_RESEARCH_GUIDE.md) and
[reproduction instructions](../research-papers/REPRODUCE.md).

## Implemented computational branch

The Fraction producer encloses five core scalars at 128, 256 and 512 fractional
bits: two normalized endpoints, plateau width, weight gap and main denominator.

A separate mpmath interval checker uses direct exponential differences and
checks containment inside the retained rational bounds. It imports no producer
code. The [cross-check method](NSRW_CORE_SCALAR_CROSSCHECK.md) describes the
algorithm, precision and rejection behavior.

The machine-readable [architecture map](../site/bridge.json) drives the website
diagram. **Established**, **implemented**, **next** and **planned** describe
different kinds of work; the arrows identify research inputs rather than
automatic logical implications.

## Next: coefficients and source admissibility

The next calculation needs justified lower C_main and upper abs(C_prefix)
bounds sufficient for a positive coefficient lower bound q. Existing explicit
inequalities are the first route; validated quadrature is needed only where
those bounds do not suffice. Preserve exact positive scale factors instead of
evaluating huge or tiny exponentials directly.

Core-dependent calculation can proceed while the selected-constant and
reset/amplitude assumptions remain explicit. Applying q to the actual source
coefficient requires those assumptions. A complete evaluable Profile is a
further construction task.

Source Profile, restricted source-family model and manufactured numerical
controls remain distinct model classes. A scalar enclosure does not construct
a ResetWitness. An evaluable restricted model can be useful in its own right,
but must be labeled as such.

## Next: conditional margin, then a same-zero certificate

The first composed output combines q with the quantitative theorem's plateau
and gap factors. It states the remaining source hypotheses and distinguishes
evaluated bounds from symbolic positive factors. A fully numerical J bound
requires all its factors to be bounded; a source-Profile.J quantitative claim
also requires the local-to-source conversion.

The later explicit-instance certificate combines:

1. A specified evaluable model and verified parameter assumptions.
2. Strict opposite mass signs at the ends of a first-window interval.
3. Continuity and a valid positive second repair coefficient bound.
4. A computed positive J lower bound that applies to the exact mass zero.
5. A separately checkable certificate with recorded input and error bounds.

The existing scalar records provide building blocks for this calculation. They
are not yet a numerical J certificate or a root bracket.

## Planned: useful scientific operations

Candidate operations include certified cancellation/denominator diagnostics and
reusable normalized bound evaluators. Research workflow diagnostics form a
parallel transfer route. Select a real workflow, baseline and measured utility
criterion before claiming practical benefit. The mathematical and computational
results already obtained are the starting material for that experiment.

The [P0-P4 plan](NSRW_POST_Z_COMPUTATIONAL_BRIDGE_PLAN_2026-10-21.md#7-p0-p4-execution-proposal-and-ai-checklist)
recommends practical branch P4-B after the coefficient milestone. A separately
justified explicit diagnostic model need not wait for the full source Profile.
Compare against equally informed standard methods, including analytic bounds
available to both sides. Mathematical preservation branch P4-A remains deferred.

## Where each part lives

| Asset | Canonical location | Publication role |
| --- | --- | --- |
| Lean statements, producer, second checker, tests | NSRW | Executable source and reproducible inputs |
| Architecture map and research documents | NSRW | Website navigation and bridge diagram |
| Cross-check execution snapshot | NSRW, referenced by Ledger | Hashed inputs and observed outcomes |
| EQA report and API record | Flamehaven Verification Ledger | Cross-project discovery and inspection |
| Essays and ongoing research narrative | Flamehaven Writing | Readable explanations linked from NSRW |

Static links and a retained execution snapshot keep the two sites usable without
a runtime API dependency. The Ledger API offers the same record to other consumers.
