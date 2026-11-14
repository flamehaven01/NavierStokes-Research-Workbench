# MomentBound MB-00–03 — first arithmetic implementation

Date: 12 November 2026, Asia/Bangkok. Same-operator implementation and review.

## Result

The fixed-input producer generated a deterministic record and the recomputing
verifier accepted it. For P=m=1, lambda=10^-12 and eta=2^-20:

```text
p = 1099511627777/1152921504606846976
B_coarse = 207522463005781740692370179/2305843009213693952 > 0
89998522 < B_coarse < 89998523
```

This completes the first arithmetic prototype, MB-00 through MB-03. The result
is B, not numerical q or J. In the reviewed static derivation q_star >= s*B,
where s=exp(-beta1*center0)/(A1*D)>0 remains symbolic. The connecting Lean
theorems have not been implemented or compiled. Record authority remains
`NONE / UNVERIFIED`; arithmetic status is `PASS[EXACT_RATIONAL_SCALED_BOUND]`.

## Source/algebra review

The five dependency proofs in the record were checked against Git blob bytes
at `7f29ebf0e2b894bf598144628230ae09df436c3d`. Both existing P1 modules also
matched that checkpoint. Upstream source remains pinned to
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

The reviewed algebra is recorded in [design sections 3–4](IMPLEMENTATION_PLAN.md):

| Step | Checked relation |
| --- | --- |
| Prefix row subtraction | Cprefix=(E1 U1/A1-E0 U0/A0)/D, with this sign |
| Common scale | Cprefix=s*(U1-rho_actual U0) |
| L2/L3/F1 bounds | Cmain/s >= kappa/(5000 lambda), abs(Cprefix)/s <= H1+rho H0 |
| Coarse prefix constants | H0<328; H1<(5/2+12*3^9)*3^8=3099396717/2 |
| Exact decision | B=9/(100000 lambda)-abs(p)*(328+3099396717/2)>0 |

These are source and algebra checks, not a new formal admission. In particular,
the strong L2 estimate is currently a private helper; MB-04 must prove a public
version separately without changing the old proof.

## Implementation and repeatable commands

- [Producer](../../src/nsrw/math_kernel/p2_coefficient_bounds.py)
- [Verifier](../../src/nsrw/math_kernel/p2_coefficient_verify.py)
- [Tests](../../tests/test_p2_coefficient_bounds.py)

A dedicated environment was created at `D:/Sanctum/venvs/nsrw-momentbound`,
using the existing Python 3.14.10 interpreter. The broken shared environment
was not changed. Project dev dependencies were installed, including the
repository-pinned SPAR dependency. This was dependency installation, not a
SPAR manuscript review. No Windows Lean installation occurred.

From the repository root, using that environment's Python:

```powershell
python -m nsrw.math_kernel.p2_coefficient_bounds produce --output outputs/momentbound-20261112.json
python -m nsrw.math_kernel.p2_coefficient_verify --input outputs/momentbound-20261112.json
python -m pytest tests/test_p2_coefficient_bounds.py --no-cov -o cache_dir=outputs/momentbound-cache
```

Create `outputs/` if absent. Producer supporting precision defaults to 128
fractional bits for exp(1); B itself uses exact fractions without rounding.
256 and 512 are also tested, not required precision escalations for B.

The verifier imports no producer and recomputes the constants, p and B using
integer/Fraction expressions. Producer and verifier share the immutable-format
metadata factory and the existing exp_bounds primitive. The verifier requires
the exact deterministic exp(1) bounds of that primitive, not arbitrary valid
enclosures. This is a closed-format recomputation check, not an independent
arithmetic backend or external reproduction. Source hashes bind approved
dependencies; runtime verification does not execute Lean or fetch their source.

## Observed verification

- Focused tests: **87 passed**.
- Full suite: **760 passed, 3 skipped, 22 subtests passed**.
- Coverage: **90.91%**, meeting the existing 90% gate.
- New producer and verifier coverage: **98% each**.
- Modified/new Python files passed Ruff before the full suite.

Tests cover exact constants, synthetic normalized systems with both prefix
signs, violated bound assumptions, altered scale/source/scope, removed
assumptions, increased B, noncanonical fractions, duplicate JSON keys,
oversized/deep records, type confusion, deterministic CLI output and error
exit codes. Synthetic systems are not source Profile constructions.

The first focused test attempt hit Windows temporary-path limits because
pytest used the oversized adversarial payload as its test ID. Explicit short
IDs fixed the test harness; no arithmetic implementation changed for that fix.

Local ignored evidence:

- `outputs/momentbound-20261112.json`
- `outputs/momentbound-targeted-junit.xml`
- `outputs/momentbound-full-junit.xml`
- `outputs/momentbound-full-tests.log`
- `outputs/momentbound-implementation-manifest.json` (file digests and environment)

## Next action

MB-04: prove the source-to-scaled-bound connection in a separate Lean module,
including exact prefix subtraction, positive common scale, coarse constants
and the conditional actual-coefficient statement. Keep full amplitude and
source-instance obligations explicit. Later replay/admission must use new
proof and execution identities.

No previous proof, receipt, ledger or scalar example was changed. No new Lean
compile, numerical Profile construction, J certificate, benchmark, commit,
push or publication was performed in MB-00–03.
