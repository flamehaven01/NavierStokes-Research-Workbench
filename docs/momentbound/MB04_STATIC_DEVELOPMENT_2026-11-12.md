# MomentBound MB-04 — first Lean development surface (not compiled)

Date: 2026-11-12 (Asia/Bangkok)
Status: `DEVELOPMENT_SOURCE_WRITTEN / STATIC_REVIEW_ONLY / UNVERIFIED`

## Scope

The historical MB-00–03 implementation is documented in
[`IMPLEMENTATION_REVIEW_2026-11-12.md`](IMPLEMENTATION_REVIEW_2026-11-12.md).
Its exact rational `B_coarse>0` is not numerical `q`, actual `c1`, or `J`.

Current MB-04 development file:
`formal/p2/P2_CoefficientScaledBounds.lean`

Local raw SHA-256 observed after write:
`363e41fe650d50cb66938ad3cb1d9b0d2f4d17d93ecafeedad62f284ff92a8fe`.

This file was found with an incomplete Python `UnicodeDecodeError` traceback
embedded in the Lean source. Its previous SHA-256 was
`e0b9f133c6a97ef3942ba85e687d3f217ad1048aa660cadc6bf00c36fc2d9a15`.
It was replaced with a standalone development source. No historical admitted
Lean proof, execution receipt, claim ledger, or Python MomentBound module
was edited for this repair.

## Eight candidate declarations (uncompiled)

1. `mb_normalizedMainMoment_zero_le_decay_one`: public-name re-derivation of
   the strong L2 explicit decay bound; avoids generated private helpers.
2. `mb_prefix_one_eq_row_difference`: prefix-only row subtraction with the
   *positive* row-1-minus-row-0 numerator divided by the exponential gap.
3. `mbCommonScale_pos`: exact positivity of
   `s=exp(-beta1*center0)/(A1*D)` from source row/gap positivity.
4. `mb_actualSecondRepairCoefficient_eq`: actual same-Profile C02
   decomposition, retaining the axial versus angular-reset distinction.
5. `mb_actualSecondRepairCoefficient_gt_qStar`: under the actual
   `F.amp eta>9/10`, actual c1 is strictly above the exact-real auxiliary
   `qStar` (the existing C01 main coefficient is positive).
6. `mb_qStar_ge_scaled_coarse`: from **explicit premises** on
   `Cmain >= s/(10000*lambda)` and
   `abs(Cprefix) <= s*(328+3099396717/2)`, infer
   `qStar >= s*B_coarse`.
7. `mb_actualSecondRepairCoefficient_gt_scaled_coarse`: conditional
   composition, same source Profile/core/eta, preserving the two undisclosed
   source-coefficient bounds as explicit premises.
8. `mb_actualSecondRepairCoefficient_pos_of_scaled_coarse`: with the above
   premises, the matching amplitude hypothesis and `B_coarse>0`,
   infer positivity of actual c1.

The exact fixed arithmetic tuple is still in the Python record. The Lean
definition of `mbCoarseBound c eta` is symbolic; this module does **not** prove
that the fixed tuple inhabits an admissible source Parameters/Profile, or
formalize the rational computation into a specialized Lean positivity theorem.

## Important remaining proof obligations

- Prove the two coefficient-scale inequalities from source L2/L3/F1 and
  `prefixCoefficient_le_bound`. At present these are **hypotheses**, not
  derived statements; no source-to-B formal closure has occurred.
- Establish the coarse `P=m=1` constants against exact source prefixBound
  expressions and prove a fixed-core specialization without inventing a Profile.
- Run Lean in the pinned 4.34.0-rc2/source commit environment on exact source
  bytes. Check every actual `#check` / `#print axioms` output and errors.
- Preserve failure runs and conduct later checkpoint/replay/admission as
  separately authorized steps. Original proof identities and records remain
  unchanged.

## Observed static checks, not execution results

- Current file: eight theorem declarations and eight `#print axioms` commands.
- No `sorry`, `admit`, new `axiom`, generated-private-name reference,
  traceback, or Unicode decode error text.
- No Lean compilation or numeric source-instance evaluation was performed.
- No Python regression suite was rerun for this source-only change.
- No Git commit/push, release, claim promotion, or private Drive archive was
  made for this MB-04 draft.

Next: discharge the source coefficient inequalities and compile this
development module against the pinned dependency chain. If compilation fails,
retain its actual diagnostics and fix *without weakening the statement*.
