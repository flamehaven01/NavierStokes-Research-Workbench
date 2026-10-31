# Core-scalar numerical observation - 31 October 2026

Code checkpoint: `adbaeeb82df3bdb9d6d6ea5a041fadc8f35f1b9b`. Python 3.14.3 on Windows; exact Fraction arithmetic. Same operator and verifier algorithm, not independent reproduction.

| Fractional bits | Producer time (seconds, one observation) | Recomputed result |
|---|---:|---|
| 128 | 0.00985 | ACCEPT, core scalars only |
| 256 | 0.01528 | ACCEPT, core scalars only |
| 512 | 0.03256 | ACCEPT, core scalars only |

The single-run timings are observations, not performance guarantees. The local complete suite reported **645 passed, 3 skipped, 22 subtests**, coverage **90.53%**. The 55 focused scalar tests include separate tighter-series enclosure comparisons and actual CLI rejection controls.

Public deterministic outputs are in [examples](../examples/p2-core-scalars/). The [method](P2_CORE_SCALAR_METHOD_2026-10-31.md) defines error bounds and the absolute dyadic precision grid. The main denominator has strictly positive lower endpoint. Its algebraic factorization is checked separately from the ten earlier Lean admissions.

The scaled second-bump expression is a lower bound, not a full I01 enclosure or an evaluated logarithm. Affine coefficients, numerical q>0, ResetWitness/K, selected constants, an explicit source Profile, a root and a numerical J certificate remain unresolved. No original Lean file, receipt or execution metadata was changed.
