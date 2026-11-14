# MB-07 ratio and denominator diagnostic

14 November 2026. The internal run used the frozen contract's four
calibration inputs, eight held-out inputs, two thresholds, three warm-ups
and twenty measured trials per method and input. Each case had a 120-second
subprocess budget. Timings exclude startup, reference computation and the
separate traced allocation sample. The run used Windows 11 build 22631,
Intel64 family 6 model 158, CPython 3.14.10 and mpmath 1.3.0. The reference
constructed inputs from exact rational numerators and denominators and
agreed on every threshold decision at 768 and 1024 working bits.
[Frozen contract](MB07_DIAGNOSTIC_BENCHMARK_CONTRACT_2026-11-13.md)
· [Runner](../../scripts/run-mb07-diagnostic.py)

| Method | Decisions or estimates issued / 16 | Contradictions | Unresolved | Median of case medians, µs | Highest case p95, µs | Highest traced peak, bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| float64 `exp(x)-1` | 6 estimates | 1 | 10 | 16.60 | 50.10 | 776 |
| float64 `expm1(x)` | 4 estimates | 0 | 12 | 19.95 | 99.80 | 958 |
| Analytic rational bracket | 0 certified | 0 | 16 | 22.23 | 45.90 | 1,180 |
| Fraction interval | 12 certified | 0 | 4 | 268.43 | 1,061.60 | 3,692 |

Direct subtraction produced five zero denominators and a wrong upper
threshold estimate at `lambda = 2^-52`. The stable float path had positive
denominators throughout, with threshold ties after rounding on six inputs.
All eight analytic brackets and all seven returned Fraction brackets
contained the reference. All seven rejection controls passed. No case timed
out.

The Fraction method resolved both thresholds at `2^-7`, `2^-10`,
`2^-52` and `2^-60` with 128 fractional bits, at `2^-120` with 256,
and at `2^-160` with 512. At `2^-400`, the 512-bit denominator lower
bound was positive, but the ratio interval was too wide for either
threshold. At `2^-520`, the lower denominator bound was zero at all
three allowed precisions.

The observed improvement is 12 additional certified threshold decisions
over the tested analytic bracket, at higher measured cost. The workload
measures factor arithmetic and threshold separation. Utility in a
scientific workflow remains unmeasured. A tighter analytic enclosure using
the first-order term of the ratio and a remainder bound was outside this
frozen comparison.

Local evidence in `outputs/`:

| File | SHA-256 |
| --- | --- |
| `mb07-manifest-20261114.json` | `ede5d96f791eb577b19874af2881d8d2b149cc890504be13ecb9e210e265ee44` |
| `mb07-result-20261114.json` | `cda6ce8abafd8f9db82a118de8e16f4b84b8997f452b2e90577a8c9376790ad0` |

The record includes the per-case interval endpoints, widths, both threshold
decisions, precision attempts, conversion errors, reference comparisons and
all timing samples. The fixed-tuple product with `B_coarse` appears only
on the `lambda = 10^-12` calibration row.
