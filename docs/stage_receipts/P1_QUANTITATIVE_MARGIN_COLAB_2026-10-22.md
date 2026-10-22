# P1 quantitative J-margin and normalization — scoped receipt

```yaml
check_status: PASS[COMMIT_BOUND_EXTERNAL_P1_MARGIN_REPLAY]
artifact_check: PASS[LOCAL_ARCHIVE_CROSSCHECK:P1_MARGIN_FINAL_RECEIPT]
statement_review: PASS[TEN_NAMED_DECLARATIONS_EXACT_SOURCE_SCOPE]
receipt_acceptance: ACCEPTED
claim_status: CONFIRMED for exactly the ten named propositions below
task_status: COMPLETED for P1-05 scoped receipt review and local admission
reviewed_on: 2026-10-22 (Asia/Bangkok)
reviewer: Codex AI assistant in the user-operated research session
operational_exposure: OE-2
shared_trust_domain: true
independent_attestation: false
independent_reproduction: false
```

This receipt records a **subsequent, same-trust-domain review**, not a verdict
produced by the replay itself. The preserved execution metadata remains
`claim_authority: NONE / claim_status: UNVERIFIED`. Only the ten listed Lean
propositions are admitted here. The upstream construction remains attributed
to its authors; NSRW derives and formalizes these exact-real quantitative and
normalization consequences. Literature novelty is not assessed by this receipt.

## 1. Objects and exact admitted scope

Use `c : Parameters`; for Profile-typed results, `c = F.data.core`. These
explanatory aliases do not replace the full Lean statements:

```text
K1    = momentScale c 1 * shape eta ^ 2
c1    = localSecondRepairCoefficient F eta
I01   = integral over real x of x^(c.exponents 0) * bump(c.lower 1,c.upper 1,x)
Delta = (c.upper 0)^(-c.lam) - (c.lower 1)^(-c.lam)
ell   = exp(-23/20); v = exp(-17/20)
mu01  = normalizedSecondBumpMoment c
L     = c.pulseLength; beta0 = 1/2 - c.lam
```

`c1` is the actual second **axial** repair coefficient for the same Profile
and eta, not the angular-reset coefficients stored in `F.reset`. Intrinsic
conditions carried by `Parameters` and `Profile` remain in force. No extra
`eta > 0`, `eta^2 <= 1` or amplitude-bound hypothesis is added to these ten
declarations. Such assumptions in a future numerical corollary must be checked
separately, not inferred from this receipt.

All declaration names below carry the `NSRW.P2.` prefix.

### QuantitativeMargin — four propositions

Source: [P2_ZPLUS_J_QuantitativeMargin.lean](../../formal/p2/P2_ZPLUS_J_QuantitativeMargin.lean).

| Declaration | Explicit parameters and additional hypotheses | Admitted conclusion |
| --- | --- | --- |
| `secondBump_massTail_eq_full` | `c : Parameters`, `r : Real`; only `r < c.upper 0` | `repairBumpTail c 0 1 r = I01` |
| `firstRepair_weightGap_pos` | `c : Parameters`; no additional hypothesis | `0 < Delta` |
| `angularMoment_ge_firstRepair_margin` | Same `F`, `eta`, `r`; `c.lower 0 < r`, `r < c.upper 0`, `localMass F eta r = 0`, `0 < c1` | `K1*c1*I01*Delta <= localAngularMoment F eta r` |
| `firstRepair_margin_pos` | `F : Profile`, `eta : Real`; only additional hypothesis `0 < c1` | `0 < K1*c1*I01*Delta`; no radius or mass-zero assumption |

Thus, at every qualifying first-window mass zero with positive actual c1,
the same fixed Profile and eta have a strictly positive lower bound independent
of the chosen zero's location. This is not a computed value of that lower bound.

### MarginNormalization — six propositions

Source: [P2_ZPLUS_J_MarginNormalization.lean](../../formal/p2/P2_ZPLUS_J_MarginNormalization.lean).

| Declaration | Explicit parameters and additional hypotheses | Admitted conclusion |
| --- | --- | --- |
| `firstRepair_weightGap_exp_eq` | `c : Parameters`; none additional | `Delta = exp(-13 + 23*c.lam/20)*(exp(17*c.lam/10)-1)` |
| `normalizedSecondBumpMoment_eq_interval` | `c : Parameters`; none additional | The whole-line `mu01` equals the interval integral from `ell` to `v` of `z^(c.exponents 0)*bump(ell,v,z)` |
| `secondBumpWeightedMoment_eq_normalized` | `c : Parameters`; none additional | `I01 = exp(L*beta0)*mu01` |
| `normalizedSecondBumpMoment_eq_rowMoment` | `c : Parameters`; none additional | `mu01 = exp(-beta0)*rowMoment(c.exponents 0)` |
| `normalizedSecondBumpMoment_ge_plateau` | `c : Parameters`; none additional | `(v-ell)/4 <= mu01` |
| `angularMoment_ge_plateau_margin` | Same `F`, `eta`, `r`; `c.lower 0 < r`, `r < c.upper 0`, `localMass F eta r = 0`, `0 < c1` | `K1*c1*(exp(L*beta0)*((v-ell)/4))*Delta <= localAngularMoment F eta r` |

The four normalization equalities and the plateau moment bound do not inherit
the mass-zero or c1 hypotheses of the last row. The exact source cutoff is 1
on the central quarter of the normalized window. Positive bases below 1 and
the nonpositive exponent give `z^a0 >= 1` there; nonnegative interval-integral
monotonicity yields the conservative width bound. This is not quadrature or
an implementation of floating-point `expm1`.

## 2. Exact execution identity

| Field | Identity |
| --- | --- |
| proof-only checkpoint | `fba27381bcfda3af6f03e2fbae82f6db016ca534` |
| execution checkpoint | `7f29ebf0e2b894bf598144628230ae09df436c3d` |
| upstream source | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| manifest executor SHA-256 | `5ec1dc8e009008d0efb9601cd38f6ba54e753fd538b0e5f8c3e6c5ec72ee1e09` |
| Lean | `leanprover/lean4:v4.34.0-rc2` |
| Lean commit | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| run | `nsrw-p1-margin-replay-20261021T181509633115Z` |
| execution UTC | `2026-10-21T18:15:11.261274+00:00` to `2026-10-21T18:16:26.762401+00:00` |

| Execution input | Executor raw SHA-256 | Git blob SHA-1 |
| --- | --- | --- |
| `P2_Z01_LocalMassIdentities.lean` | `ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267` | `9d6a9a2196b8383fc17b38585e39a80188e3bfcd` |
| `P2_Z02_BoundaryMassSigns.lean` | `7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c` | `a4681a313cbebcbacbf49962484725cbafe896a2` |
| `P2_ZPLUS_J_FirstRepairAngularMoment.lean` | `2af3c68a73530a97421b3bd971bae5e63bbfb60c1abb7f40361d6d347e875d4a` | `11ccd687f7157c7a1bb5529843344ce04373d7af` |
| `P2_ZPLUS_J_QuantitativeMargin.lean` | `7a504d7c9cde6d76f2d0e826572fbbebeae905166802adc3e7b0d9b844e534b6` | `16e0f2d48f0205db7a7d3bca9c1ab9262e7b925a` |
| `P2_ZPLUS_J_MarginNormalization.lean` | `058ad35fca4228ea29773cef7c118dce7414745451f7f20361ca159d9a68ab8b` | `b3d8d48f9cd808a101540fff91f4314f921f6a0e` |
| `colab/run-c02-development.py` (source identity helper only) | `540f0aadd7add25bc0cfae2d852009e68c23cb13537ec03c4e5bce1ba085a278` | `518de06530c4c7c56edafdf571e5fb2ef0f808b3` |
| `scripts/run-p1-margin-replay.py` | `b04723f0d6555345fb2651b1c82d27a9e5aa9e5023d60e0a3bc5bacc7ffe4d87` | `79f9ba6420fb1908248decd55844fbb81d1fea80` |

All seven archived input bytes matched `git show` at the execution checkpoint
and current local proof/runner bytes during this review. Test files and one-off
observers/preservation/review helpers are not additional mathematical inputs.
Later documentation must not replace the execution pin.

## 3. Replay and evidence inspection

The command was `python3 scripts/run-p1-margin-replay.py` from the clean detached
checkout, with `--source-root /content/NavierStokesAndEuler`, `--nsrw-root`
pointing to that checkout, `--output-dir` pointing to the new run directory,
and `--expected-nsrw-commit 7f29ebf0e2b894bf598144628230ae09df436c3d`.
Exact expanded commands and stage timings are in archived metadata.

```text
source +NavierStokes.OutgoingProfile
 -> fresh Z01 -> fresh Z02 -> fresh conditional Z+J
 -> fresh QuantitativeMargin -> fresh MarginNormalization
```

Six stages exited 0 and all six stderr files were empty. Five fresh external
artifacts were produced; each archived artifact was rehashed. Ten actual
compiler declaration outputs were read and compared with the fixed Lean source,
not just counted. Each target axiom set was exactly
`[propext, Classical.choice, Quot.sound]`; `sorryAx` was absent from all logs.

**Reviewed warning:** the imported conditional Z+J module's stdout contains
the existing line 123:34 linter warning, `Used tac1 <;> tac2 where (tac1; tac2)
would suffice`. It does not change the named statements or add an axiom.
Empty stderr is not a claim of warning-free compilation. No proof was edited
to remove the warning for this admission.

Source/NSRW pre/post identities, tracked-clean observations, all eleven pinned
dependency revisions and the source target hash matched. The observed
`OutgoingProfile.olean` SHA-256 stayed
`444300e42a8bc6bc27d224cf9fe0dfe407c073041757fe506cd9f1eca086921c`.
That source artifact is a pre/post observation, not an archived authority input.
The pinned source/cache was reused; this was not a cold full-library rebuild.
F1--C04 and source-facing quantitative J composition were not replayed here.

## 4. Preservation and final receipt acceptance

The original private Drive destination is
`MyDrive/NSRW-evidence/2026-10-22/nsrw-p1-margin-replay-20261021T181509633115Z/`.
Its original ZIP is
`nsrw-p1-margin-replay-20261021T181509633115Z-replay-evidence.zip`.

| Record | Size / SHA-256 |
| --- | --- |
| original ZIP | 583281 bytes; `9163d2ee67a4cab03c152151d1df7c3e4990306c6d2fa184b52d63e556aa52a5` |
| original replay metadata | `cf92bac7c368b79368f0d2f2be9bea847b2a9ed79fe535081debd053f734c55b` |
| original Drive archive-review JSON | `2ebc4da3f1021c74eba36ffd610fc8ba883843484483b2db7a1e4b69d4cf6922` |
| final local archive-review JSON | `ccf0b410937742244a32e9683e92da03c330fbd31e4dc2c6cc8a8316fe450e61` |

The earlier Drive copy was reopened in the execution session. At this final
receipt stage, the new Colab review cell did not yield an observable result;
that attempt is not credited as verification. Instead, the **same private ZIP**
was fetched through the connected Drive file API into the Git-ignored D:
`colab/evidence/2026-10-22/p1-margin-final-admission-review/` directory. Its
size and SHA-256 matched the original. No public link or sharing change was made.

The bounded local review did not import the replay runner. It checked ZIP CRC,
safe/unique paths and no symlink members, exact 25-member inventory, seven
archived raw hashes and Git blobs against exact committed bytes, five artifact
hashes, twelve log sizes/hashes, six exits/stderr, ten declaration/axiom outputs,
metadata digest, and pre/post identity. It reread the ZIP after inspection and
confirmed its original digest. Exact UTF-8 declaration outputs are retained in
`final-receipt-archive-review-20261022T041520313162Z.json` beside the local ZIP.
The review time is UTC 2026-10-22, on the same Bangkok calendar date.

An initial local verifier completed and saved its checks but then hit a Windows
console encoding error while printing a real-number symbol. Its review JSON
was retained separately. Only console preview encoding was corrected; the next
read-only verifier invocation completed with exit 0 and a separate timestamped
review. This was **not** a Lean retry, proof repair, changed archive or mixed run.

The reviewer accepts precisely the ten scopes in section 1, based on the
fixed source statements and this directly inspected preserved execution.
The ledger indexes each declaration separately under this one receipt.
The original replay metadata remains `NONE / UNVERIFIED` byte-for-byte; this
document records the subsequent admission, not a metadata self-promotion.
Execution, user-operated UI, connector retrieval and AI-assisted review share
one operator/trust domain. They do not constitute independent reproduction,
human expert attestation or OE-3. **OE-2** is retained.

## 5. Unchanged boundaries and next research task

This receipt does not admit a numerical q>0, computed J margin, explicit
evaluable source Profile, certified interval arithmetic/expm1 or quadrature,
discharged combinedScale/selected stepBound/amplitude assumptions for an
instance, computed root/epsilon, first/unique/simple zero, quantitative
source-facing Profile.J wrapper, Q pole/limit, paper--Lean equivalence,
literature novelty, upstream theorem verification, application performance
or a Navier--Stokes solution.

P1's ten exact-real quantitative/normalization propositions are closed in this
named scope. Next is the unresolved P0 numerical-admissibility dependency map
and P2's first bounded coefficient/margin calculation, not another replay.
Existing Z-core/Z+J receipts and their original scopes remain unchanged.
No compile, installation, original evidence mutation, commit/push, tag/release,
Zenodo upload or external publication was performed for this receipt review.

Supporting history: [execution record](../../colab/P1_MARGIN_COMMIT_BOUND_REPLAY_2026-10-22.md),
[quantitative development](../../colab/P1_QUANTITATIVE_MARGIN_DEVELOPMENT_2026-10-22.md),
[normalization development](../../colab/P1_MARGIN_NORMALIZATION_DEVELOPMENT_2026-10-22.md).
