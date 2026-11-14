# MomentBound MB-05 — source / Lean / arithmetic correspondence review

Review date: 2026-11-13 (Asia/Bangkok). Local workspace review; one operator/trust domain.

```yaml
review_status: PASS[STATIC_SOURCE_LEAN_ARITHMETIC_CORRESPONDENCE]
execution_evidence: REPORTED_PASS[MB04_PINNED_DEVELOPMENT_COMPILE]
archive_reopen: PASS_RECORDED_BY_COLAB_SAME_TRUST_DOMAIN
archive_reopen_by_this_review: NOT_PERFORMED
formal_admission: PENDING
claim_authority: NONE
claim_status: UNVERIFIED
operational_exposure: OE-2_CANDIDATE_ONLY
independent_reproduction: false
checkpoint_replay: NOT_PERFORMED
new_lean_compile: NOT_PERFORMED
git_commit_push: NOT_PERFORMED
```

## 1. Reviewed identities

| Surface | Observed source/Lean | Python/record correspondence | Scope |
| --- | --- | --- | --- |
| Explicit L2 decay | `mb_normalizedMainMoment_zero_le_decay_one` in `P2_CoefficientScaledBounds.lean`; reconstructed from public definitions, not imported from L2's private helper | Source of the coarse main ratio | Exact real, arbitrary source `Parameters c` |
| Prefix-only row subtraction | `mb_prefix_one_eq_row_difference`: row-1 numerator minus row-0 numerator over positive `D` | Synthetic row-sign tests exercise that direction | Exact source normalized 2x2 system |
| Common positive scale | `mbCommonScale c=exp(-beta1*center0)/(A1*D)`, `mbCommonScale_pos` | JSON `positive_scale` matches the symbolic definition and records `numerically_evaluated:false` | No numerical value of `s` |
| Main coefficient | `mb_main_one_ge_coarse`: `s/(10000*lambda) <= Cmain` from source F1/L2/L3/C01 | `main_over_scale_lower = 100000000` at fixed lambda | No amplitude required |
| Prefix coefficient | `mb_prefix_one_abs_le_coarse`: `abs(Cprefix) <= s*(328+3099396717/2)` | `H0_upper=328`; `H1_upper=3099396717/2`; total `3099397373/2` | Requires source `c.P=1` and `c.m=1`; neither coefficient sign is asserted |
| Scaled q auxiliary | `mb_qStar_ge_source_coarse`: `s * Bcoarse <= qStar` | `q_over_scale_lower` is `Bcoarse`, not `qStar` itself | Exact source core `c`, `P=m=1` |
| Fixed scalar identity | `mb_fixed_coarse_eq`; `mb_fixed_coarse_pos` | Exact rational calculation of `Bcoarse > 0` matches | Requires `c.lam=1/10^12` for specialization; `eta=1/2^20` fixed in declaration |
| Actual axial coefficient | `mb_actualSecondRepairCoefficient_fixed_pos`, composed with existing C02 and main positivity | The Python v1 record **does not** contain a numeric actual `c1` | Requires a supplied `Profile F`, matching `P=m=1`, `lambda`, and **actual `F.amp(eta)>9/10`** |

The exact source construction is attributed to its upstream authors.
NSRW's new work is the scoped exact-real derived source-coefficient bridge,
not a newly certified source instance or a global Navier–Stokes proof.

## 2. Independently re-evaluated exact rational surface

Fixed tuple: `P=m=1, lambda=1/1000000000000, eta=1/1048576`.

```text
p           = 1099511627777/1152921504606846976
H0_upper    = 328
H1_upper    = 3099396717/2
main/s >=   100000000
abs(prefix)/s <= 3099397373/2
B_coarse    = 207522463005781740692370179/2305843009213693952
89998522 < B_coarse < 89998523
s numerator exponent
            = -3249999999986250000000003/500000000000
```

These identities were independently recomputed using integer/Fraction
arithmetic during this review, not by calling the repository producer.
They match `outputs/momentbound-20261112.json`,
`src/nsrw/math_kernel/p2_coefficient_bounds.py`, and the matching Lean
fixed-input equality. This checks **arithmetic correspondence** and does
not constitute independent Lean/kernel execution.

Correct interpretation:

```text
s > 0
qStar >= s*Bcoarse > 0             (conditional source c with P=m=1)
actual c1 > qStar                   (same Profile's amp(eta) > 9/10)
```

No float64 evaluation of `s`, `qStar`, actual `c1` or `J` is implied.

## 3. MB-04 development evidence reviewed

Read-only inspection of `docs/momentbound/MB04_DEVELOPMENT_2026-11-13.md`,
the two **current local source files**, and prior arithmetic/manifest records
shows:

- Lean toolchain: 4.34.0-rc2; upstream source pin
  `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`;
  manifest blob `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`.
- `P2_CoefficientScaledBounds.lean` local SHA-256:
  `7b75a32b7c9ca3023a3e7dfb47389c07af0382c48e32db4caadd82cb1f7c9719`.
- `P2_CoefficientSourceBounds.lean` local SHA-256:
  `f2e04f957e37c16ba4428e18dd4640b7662fd66051d2796836464603839e8ccf`.
- Reported fresh development run: 9/9 module stages exit 0, empty stderr;
  actual statements and `#print axioms` for 14 names, only
  `Classical.choice`, `Quot.sound`, `propext` and no `sorryAx`.
- **Three stdout tactic-linter warnings remain recorded**, not erased by
  empty stderr: source module line 81 (unneeded sequencing) and line 136
  (two redundant-ring warnings). Warnings are not compile failures.
- Failed run `mb04-development-20261113T042908724752Z`: ZIP 423359
  bytes, SHA-256 `39237c7ec3f67d5754fd29bb6d489fcb123ee4fdadc9ca0fd90a0752a7470537`.
- Failed run `mb04-development-20261113T043254679728Z`: ZIP 606533
  bytes, SHA-256 `110c78cc2fdaae5c219e50bbc2f1485e6e10e0fffefc8da0e9804d833290ae6a`.
- Successful run `mb04-development-20261113T043506238941Z`: ZIP 868816
  bytes, SHA-256 `4586cd70bb63c481e276f0bfa87aa0d723d0a2f897be6581d098d772dec4eaaf`.
- Private Drive location, reported and reviewed by original Colab runtime:
  `MyDrive/NSRW-evidence/2026-11-13/<run-id>/<run-id>.zip`.
  Original same-runtime review reports SHA-256, ZIP CRC, inputs, compiled
  artifacts and log digests matching for all three runs, with inventories
  of 35/38/39 members respectively. **This review did not independently
  redownload/reopen those remote ZIP bytes**.

The failed runs and successful run are distinct evidence; success does not
retroactively transform a failed compile into success.

## 4. Historical status is preserved

The original MB-00–03 JSON still says
`NEW_COEFFICIENT_BRIDGE_NOT_COMPILED` and
`mathematical_bridge: STATIC_DERIVATION_NOT_ADMITTED`.
That reflects its 2026-11-12 creation date. Do not rewrite it to imply
MB-04 had compiled at that time. A later *versioned*, separately byte-bound
record may refer to an admitted MB-04 bridge after the admission actually
occurs.

The development source header in
`P2_CoefficientScaledBounds.lean` also contains historical text saying it
was not compiled and that source inequalities are premises. The second
source-estimate module now discharges those coefficient-bound premises in its
source-constrained propositions. Preserve the current compiled source SHA;
record this as documentation drift rather than silently rewriting the proof.

The existing P1 receipts are unaffected. The Python verifier does not call
the producer, but shares the record-contract factory and `exp_bounds`;
this is same-operator recomputation, **not** an independently implemented
arithmetic backend, external attestation, or OE-3 reproduction.

## 5. Admission boundary and next gate

**MB-05 static correspondence review: PASS**, with the historical-v1 and
linter qualifications above. This does **not** constitute a formal claim
admission or complete P2 source-instance certificate.

Remaining gates for formal admission:

1. Freeze the two new Lean proof files, minimal execution runner and exact
   dependency identities in separately identified checkpoint(s); do not
   accidentally stage the unrelated dirty working tree.
2. Execute a new commit-bound pinned Lean replay and preserve its original
   outputs. Prior development ZIPs do not substitute for that replay.
3. Inspect all 14 **printed exact proposition signatures** and axiom sets,
   match byte hashes/archives, and issue a *separate* dated, narrow admission
   receipt only on verified evidence. Preserve original metadata's
   `NONE / UNVERIFIED` status.
4. Synchronize the appropriate atomic ledger/checklist entries **after**
   receipt acceptance, never beforehand. Keep OE-2 for same-trust-domain
   execution, not OE-3.
5. Keep `Profile F` existence at the fixed tuple, same-reset amplitude
   admissibility, combinedScale/stepBound obligations, source `J` numerical
   evaluation, numerical root, novelty and application performance outside
   this admission.

No new Lean/Python execution, formal admission, source repair, Git commit/push,
or Drive archive modification was performed during this review.
