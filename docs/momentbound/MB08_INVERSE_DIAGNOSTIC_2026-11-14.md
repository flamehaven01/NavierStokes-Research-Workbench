# MB-08 inverse operator diagnostic

## P0 · Scope and acceptance

Check the original reset matrix convention against its pinned source
and exercise an exact inverse and solve check on synthetic inputs.
The reference matrix and right-hand side come from the fixture.
The candidate supplies its own matrix, inverse, determinant and solution.
A candidate with an internally consistent inverse for the wrong matrix fails.

## P1 · Design

FHVAL owns the exact two-by-two check. It uses Python integers and
`Fraction`, computes the determinant from the reference entries and
checks both products against the identity matrix. It also checks the
solution by multiplication with the reference matrix. Zero determinant
is singular. A small nonzero determinant remains an exact test case.

NSRW owns the original row convention and checks the pinned source file
identity. The reference form is `[[A, E*A], [2*B, 2*F*B]]`. The source
envelope check combines the documented moment and exponential bounds
using exact rational arithmetic. The actual source moments remain symbolic.

## P2 · Implementation

Add the exact checker in FHVAL and a project-specific runner in NSRW.
Keep the checker independent of any inverse or solution producer.
Use a fixed reference to reject coherent row swaps and removal of the
pressure factor even if each candidate has a mathematically valid inverse.

## P3 · Diagnosis

Require correct results for the normal and near-singular controls.
Require rejection of row swap, pressure factor removal, determinant sign
flip, incorrect inverse and incorrect solution. Require an explicit singular
result for zero determinant. Check the exact source envelope against the
Lean bound of 1000 and retain the diagnostic JSON under ignored outputs.

### Observed result

**GREEN for the local inverse diagnostic.** All nine cases matched their
expected results. Two correctly solved systems passed, six altered
candidates were rejected, and the singular control was reported as
singular. The tests also confirmed that the two coherent mutations become
valid solutions if the reference itself is replaced by the candidate.

- Pinned file SHA-256 matched both the checkout and the Git blob at
  `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
- The exact envelope gave `|det M| ≥ 81/4000` and
  `‖adj M‖∞ ≤ 33/5`, hence `‖M⁻¹‖∞ ≤ 8800/27 < 1000`
  given the analytic input bounds. The diagnostic applies simultaneously
  valid scalar inequalities and does not perform source quadrature.
- FHVAL targeted regression passed 53 tests, including 11 new inverse
  tests. Ruff passed for the three Python files.
- The CLI rejected a different source file with exit 2. A repeat run
  produced the same JSON, and a request to overwrite that JSON failed
  with exit 2 without changing its bytes.
- Local output `outputs/mb08-inverse-diagnostics.json` has SHA-256
  `abd6f23288696b1d75dc4fbab6fa9b9cb6c92f1382cabe9a5e9a9dfa25011308`.

The diagnostic does not execute Lean. MB-08 remains developmental.
Durable archival of the Colab ZIP and the original cutoff jet condition
remain pending. The result supplies no source reset or amplitude data.

### Reproduce locally

From the NSRW root with the existing project Python and the local FHVAL
source tree on the module path:

```powershell
$env:PYTHONPATH = 'D:/Sanctum/Fhval/src'
& 'D:/Sanctum/venvs/nsrw-momentbound/Scripts/python.exe' -B `
  scripts/check-mb08-inverse.py `
  external_sources/related-repos/openai/NavierStokesAndEuler/NavierStokes/AngularMomentReset.lean
```
