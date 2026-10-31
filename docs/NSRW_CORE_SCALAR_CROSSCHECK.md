# Core scalars: a separate interval-arithmetic check

The retained scalar JSON can now be checked through two calculation paths.
The producer uses exact Fraction series, a bounded remainder and factored
expm1 expressions. The second checker uses **mpmath 1.3.0 interval arithmetic**
and the original exponential differences. No NSRW producer module is imported.

## What is checked

For lambda = 1/10^12, the second implementation encloses:

- ell = exp(-23/20), v = exp(-17/20);
- w = (v - ell)/4;
- G = exp(-13 + 57 lambda/20) - exp(-13 + 23 lambda/20);
- D = exp(1 - 2 lambda) - exp(1 - 4 lambda).

It then requires each complete computed interval to lie inside the claimed
rational endpoints. Agreement of approximate midpoints is insufficient.
The independent backend runs at **b + 192 working bits**, where b is the
record's 128, 256 or 512 fractional bits. All input rationals enter through
integer interval division, never through binary64 floats.

## Run it

With Python >=3.10 and the optional verification dependency installed:

```sh
python -m pip install -e '.[verification]'
python scripts/check-core-scalars-mpmath.py examples/p2-core-scalars/core-scalars-128.json examples/p2-core-scalars/core-scalars-256.json examples/p2-core-scalars/core-scalars-512.json --output crosscheck.json
```

The dependency is pinned to mpmath==1.3.0. On PowerShell the same Python command
works; activate the repository's configured environment first. The generated
report binds every result to the executor's raw input SHA-256 and a portable
LF-normalized input SHA-256, and records the working
precision, backend and checked quantities.

The LF identity is stable across Git checkouts with different line endings.
The raw identity preserves the original executor observation; the site checks
the LF identity rather than confusing line-ending changes with numeric drift.

## Rejection behavior

The checker rejects changed input tuples, missing assumptions, changed source
identities, promoted scope, duplicate keys, unexpected fields, malformed bounds,
zero-width intervals and a claimed interval that fails full containment.
The symbolic I01 lower expression must remain bound to the plateau lower endpoint.

Mutation tests shift otherwise valid dyadic intervals, remove contract fields
and attempt to promote the scalar result to a numerical J certificate. They
exercise the actual checker and CLI exit behavior.

## Interpreting the result

A PASS is a **second-backend scalar cross-check**. The algorithm and arithmetic
implementation differ from the producer. The run is performed by the same
operator, so it does not constitute separately operated external reproduction.
It checks five scalar enclosures, not a source Profile or a numerical J value.

mpmath documents its interval context as experimental. This checker uses only
integer/rational interval operations, exp and endpoint comparisons in the pinned
version; indeterminate comparisons reject. The result is software-backed
interval checking, not a Lean proof of mpmath itself.

## Inspect the retained run

[Retained report](../examples/p2-core-scalars/mpmath-crosscheck.json) contains
three records and fifteen containment checks. The
[Flamehaven EQA entry](https://flamehaven01.github.io/Flamehaven-Verification-Ledger/eqa.html#toe-test-0061)
links this execution to the wider research ledger. The NSRW repository remains
the canonical location for the executable checker and its tests.

Reference: [mpmath interval context documentation](https://mpmath.org/doc/current/contexts.html#arbitrary-precision-interval-arithmetic-iv).
