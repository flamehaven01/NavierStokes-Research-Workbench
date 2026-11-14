# MomentBound MB-04 development compile

13 November 2026 (Asia/Bangkok). Lean 4.34.0-rc2, Colab.

The two MomentBound modules compiled in a nine-module chain from a fresh
artifact directory. The pinned upstream source build completed before this
run. All nine module commands returned exit 0 with empty stderr. The 14
named axiom outputs contain only `Classical.choice`, `Quot.sound`, and
`propext`. The run metadata reports `NONE / UNVERIFIED` for claim authority
and status.

## Compiled mathematical scope

- `mb_main_one_ge_coarse` obtains the main coefficient lower bound from the
  explicit L2 decay, L3 row comparison, and F1 main moment lower bound.
- `mb_prefix_one_abs_le_coarse` obtains the absolute prefix coefficient upper
  bound from the normalized source rows and the two prefix moment bounds
  at `P=m=1`.
- `mb_qStar_ge_source_coarse` consumes both estimates and yields
  `s*B_coarse ≤ q_star` for that source core.
- `mb_fixed_coarse_eq` and `mb_fixed_coarse_pos` establish the exact fraction
  `207522463005781740692370179/2305843009213693952` and its positivity
  at `lambda=10^-12`, `eta=2^-20`.
- `mb_actualSecondRepairCoefficient_fixed_pos` derives positivity of the
  actual second coefficient for a supplied source Profile with
  `P=m=1`, `lambda=10^-12` and `F.amp(2^-20)>9/10`.

The prior conditional module supplies the explicit L2 estimate, row
subtraction, positive common scale, coefficient identity and comparison
with the actual coefficient. Its eight declarations compile alongside
the six source estimate declarations above. Profile existence and the
amplitude condition for a concrete instance are open.

- [Conditional coefficient module](../../formal/p2/P2_CoefficientScaledBounds.lean)
- [Source estimates and fixed input result](../../formal/p2/P2_CoefficientSourceBounds.lean)

## Execution identities

- Upstream source `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`
- Manifest Git blob `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`
- Seven NSRW dependencies matched the bytes at `7f29ebf0e2b894bf598144628230ae09df436c3d`
- Final conditional module SHA-256 `7b75a32b7c9ca3023a3e7dfb47389c07af0382c48e32db4caadd82cb1f7c9719`
- Final source estimate module SHA-256 `f2e04f957e37c16ba4428e18dd4640b7662fd66051d2796836464603839e8ccf`
- Final input ZIP SHA-256 `1786cb264eb8017ea0ad05e60ffca94de5c5d8ce73db66eedbef1b74e12d3c16`

The successful run checked the source commit, pinned dependencies, tracked
clean state, source target artifact, and input hashes. Source identity and
the target artifact hash matched before and after the nine module stages.

| Colab run | Result | ZIP bytes | ZIP SHA-256 |
| --- | --- | ---: | --- |
| `mb04-development-20261113T042908724752Z` | Conditional module name resolution and row algebra errors | 423359 | `39237c7ec3f67d5754fd29bb6d489fcb123ee4fdadc9ca0fd90a0752a7470537` |
| `mb04-development-20261113T043254679728Z` | Conditional module passed. Source module exponential imports and denominator cancellation failed | 606533 | `110c78cc2fdaae5c219e50bbc2f1485e6e10e0fffefc8da0e9804d833290ae6a` |
| `mb04-development-20261113T043506238941Z` | Both MomentBound modules passed | 868816 | `4586cd70bb63c481e276f0bfa87aa0d723d0a2f897be6581d098d772dec4eaaf` |

The input bundle and development driver are in the local ignored
`outputs/` directory. Execution ZIPs were generated in Colab `/content`
and copied to private Drive under
`MyDrive/NSRW-evidence/2026-11-13/<run-id>/<run-id>.zip`.
Colab reopened all three Drive copies and checked their sizes, archive
SHA-256, ZIP CRC, and recorded hashes for inputs, artifacts and stage logs.
The copies contained 35, 38 and 39 members in run order. Both compiled
MomentBound source digests matched the final local file digests above.

The successful compiler stdout contains three tactic linter warnings in
`P2_CoefficientSourceBounds.lean`. Line 81 flags an unnecessary sequencing
operator, and line 136 emits two warnings for the same redundant `ring`.
The nine compiler exit codes are 0 and stderr is empty.

Formal admission and the combined MB-05 review remain pending. Drive
reopening was performed from the same Colab runtime.
