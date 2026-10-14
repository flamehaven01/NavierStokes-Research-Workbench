# P2 Z-02 development preparation — 2026-10-10

This is a development execution and interruption record, not a commit-bound receipt.

```yaml
implementation: WRITTEN[CONDITIONAL_SOURCE_BOUNDARY_SIGNS]
driver_controls: PASS[FOCUSED_PYTEST:12_TESTS]
lint: PASS[RUFF:Z02_DRIVER_AND_TESTS]
lean_compile: PASS[LOCAL_PROOF_COMPILE:P2_Z02]
claim_authority: NONE
claim_status: UNVERIFIED
task_status: COMPLETED[Z02_DEVELOPMENT_COMPILE_AND_LOCAL_PRESERVATION]
```

## Exact scope

[Z02 proof](../formal/p2/P2_Z02_BoundaryMassSigns.lean) imports only
[Z01](../formal/p2/P2_Z01_LocalMassIdentities.lean). Its source dependency is
`NavierStokes.OutgoingProfile`. The intended development chain is:

```text
pinned source build (+NavierStokes.OutgoingProfile)
  → fresh P2_Z01_LocalMassIdentities.olean
  → fresh P2_Z02_BoundaryMassSigns.olean
```

The F1/L2/L3/D/C01/C02/C03/C04 external chain is not executed. C04 is not
imported. `localSecondRepairCoefficient` is a definitional alias of the actual
source `LocalizedMomentRepair.coefficients ... (debt ... F.amp eta) 1`, not the
angular-reset coefficient family. `localMass` names source `massMoment` at
`pulseStart + log r`; no conversion factor is inserted.

Eight named statements compiled in the successful development run below;
none is admitted as a commit-bound claim in this record:

- `prefixM_pos`
- `radialPulse_before_first_lower`
- `localMass_lower_pos` (explicit `eta > 0`)
- `secondBumpWeightedMoment_pos`
- `upperTail_radialPulse_eq`
- `secondBumpWeightedMoment_tail_eq`
- `localMass_upper_eq_second_tail`
- `localMass_upper_neg_of_secondCoeff_pos` (explicit actual second-coefficient positivity)

The upper formula is the intended source-native bridge:
`M(u0) = -(momentScale * shape) * (actual second coefficient * full second-bump moment)`.
Z02 does not supply coefficient positivity; it consumes that hypothesis.
No IVT, zero existence, uniqueness, first-zero, per-Profile epsilon, uniform
epsilon, numerical radius, paper equivalence or upstream verification is admitted.

## Source inspection

Direct read-only GitHub file retrieval at source commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` confirmed the signatures used for
the implementation. This is source inspection, not Lean execution or an
independent mathematical review.

- [OutgoingSchedule](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean):
  support ordering, correction reduction, moment prefactor positivity and
  `correction_interval_exact`'s support-localization pattern.
- [LocalizedMomentRepair](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/LocalizedMomentRepair.lean):
  open bump support, repair sum and actual matrix definition.
- [OutgoingPulseBounds](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean):
  `actual_matrix_entry` and `rowMoment_pos`.
- [OutgoingProfile](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingProfile.lean),
  [CorrectedPulseAmplitude](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/CorrectedPulseAmplitude.lean),
  [PulseAmplitude](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/PulseAmplitude.lean):
  actual amplitude alias/positivity and nonnegative main pulse.

## Initial interruption (before the execution below)

The connected notebook displayed runtime resources, but crashed while an
observation cell was being added. Opening a recovery tab then timed out and
displayed `ERR_TIMED_OUT`. Current source checkout/toolchain identities were
not re-observed from the VM, and no Z02 compile was launched. There is therefore
no Z02 Lean log, exit code, fresh `.olean`, or execution ZIP to admit.
The browser error must not be classified as a mathematical failure or cache
failure. No runtime reset, Windows installation or `lake update` was performed.

Once Colab access is restored:

1. Observe the current VM, source commit, manifest blob, installed toolchain and
   the existing helper checkout; restore only if actually needed and authorized.
2. Upload exact Z01/Z02 source bytes and [the Z02 driver](run-z02-development.py).
   Preserve Z01 SHA `ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267`.
   Obtain the current Z02 raw SHA directly from the local file before upload.
3. Execute the driver once in a new run directory, using `--source`, `--base`,
   `--dependency`, `--proof`, `--output`, and `--proof-sha256`. `--base` must be
   the existing exact `10d5a1f517b8665137f2354746d70752f8ef67fd` helper checkout.
4. Inspect source/Z01/Z02 exit codes, raw stderr and all named axiom outputs;
   retain successful or failed archive under `colab/evidence/<date>/<run>/`.
5. Only a successful actual development run may change the compile status to
   `PASS[LOCAL_PROOF_COMPILE:P2_Z02]`. Claim admission remains separate.

The focused Python tests inspect driver input/output protection and named axiom
parsing, not the Lean proofs. Existing Z01 evidence and all unrelated dirty
documents remain preserved. No commit, push, receipt, tag or release was created.

## Actual launch and second browser interruption

The live VM observation at `2026-10-10T10:28:58Z` showed no source checkout or
elan. Approved Colab-only pinned restoration then completed successfully at
`10:36:59Z`. No Windows installation, `lake update`, proof change, or claim
admission was performed. The existing C04C-named restoration helper was reused
only for environment bootstrap; no C04 proof/replay was executed.

Restoration evidence is locally preserved under
`colab/evidence/2026-10-10/nsrw-z02-environment-20261010T103054Z/`.
The ZIP has 22,005 bytes and SHA-256
`68122e4350609de3e9365b9a76ee3a8037e6f09c2db5e446bea362fcd51e735c`,
crosschecked against the displayed Colab archive hash. Its 34 entries were
path-checked before extraction. This confirms archive preservation, not Lean
proof compilation.

The development runner was actually launched once:

```text
run: /content/nsrw-z02-development-20261010T103659Z
observed launch PID: 6436 (historical observation, not a current liveness claim)
helper checkout: /content/nsrw-c04c-clean-10d5a1f-20261010T103054Z
helper commit: 10d5a1f517b8665137f2354746d70752f8ef67fd
Z01 SHA-256: ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267
Z02 SHA-256: c76e07f4e46f84d571bc9db6ba1ee0c18e0f3a1d50925883cfda44c5666c5629
driver SHA-256: 2ca5341038702b1f49df2f8702a2220428eb40c0d7f2e348f33af491881ac578
claim_authority: NONE
claim_status: UNVERIFIED
```

The locally retained one-run launcher (`z02-development-start.py`, not distributed) records the exact observed
restoration paths and input hashes. The notebook waited for restoration exit 0
before executing it. It is an operational helper, not a mathematical dependency.

The last successful observation showed the source stage still running, stderr
0 bytes, and successful builds through `OutgoingPulseBounds` (78 seconds).
No source-stage final exit, Z01/Z02 exit, axiom output or development archive
was observed or downloaded. The in-app page then crashed; a same-browser
recovery-tab attempt also timed out. This does not establish that the VM or
its compile process stopped, nor that compilation failed mathematically.

**Next action is observation of this existing run, not another launch.** Reopen
the notebook without resetting/deleting the runtime, inspect this exact run's
`run-metadata.json`, launcher logs and source/Z01/Z02 logs, and preserve its
eventual ZIP before deciding whether repair or a new run is necessary. Do not
rerun the restoration or launch cell merely to recover the page. Z03 and claim
admission remain deferred.

## Reobservation, minimal repair and successful separate run

After the user reopened Colab, the original run was observed to have finished
with source exit 0, Z01 exit 0 and Z02 exit 1. Its failure boundary was
`Z02_LEAN_COMPILE`. Lean reported three implementation errors: an extra binder
in `integral_nonneg_of_forall`, use of that global-positivity API where interval
membership was needed, and an unreduced function application blocking rewrite.
The failed output's `sorryAx` entries are diagnostic consequences of failed
elaboration, not admissible proof evidence. Empty stderr did not make this run
successful; the errors were in stdout and the exit code was nonzero.

The original 67,192-byte ZIP was preserved and path-checked before extraction:

```text
local directory: colab/evidence/2026-10-10/nsrw-z02-development-20261010T103659Z/
archive SHA-256: ae9f37b0f472615b7d685b12c27e5dc4b02f35a10fffe04dcd803b6e5eebcf45
```

The pinned mathlib source confirmed `integral_nonneg` takes the interval-bound
hypothesis. Only the three proof application sites were repaired. Z01 and the
development driver bytes were unchanged. A new run, not a renamed or overwritten
failure, compiled the repaired bytes:

```text
run: nsrw-z02-development-20261010T112430Z
finished UTC: 2026-10-10T11:25:54.341931+00:00
Z02 proof SHA-256: 7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c
Z01 proof SHA-256: ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267
driver SHA-256: 2ca5341038702b1f49df2f8702a2220428eb40c0d7f2e348f33af491881ac578
source / fresh Z01 / fresh Z02 exits: 0 / 0 / 0
all three stderr logs: empty
Z02 named axiom surfaces: 8 / 8, [propext, Classical.choice, Quot.sound]
sorryAx: absent in successful proof output
check_status: PASS[LOCAL_PROOF_COMPILE:P2_Z02]
claim_authority: NONE
claim_status: UNVERIFIED
```

The 146,366-byte successful ZIP is preserved separately:

```text
local directory: colab/evidence/2026-10-10/nsrw-z02-development-20261010T112430Z/
archive SHA-256: 3606dd047c0d579bfe1325f29cd0ecd8f568531c28b04de8ad7b9f29675f78d6
```

Both archive hashes were crosschecked against explicit Colab output. The
successful archive's 13 entries were path-checked before extraction; all four
input hashes, two fresh external artifact hashes and six log hashes were
recomputed locally against metadata. Source pre/post identity and source-target
artifact hashes match. Source build reused this VM's cache; it was not a new
full-library rebuild. Execution and preservation review share one trust domain.

The notebook page was reloaded once to recover stalled UI input; the runtime
was not reset. The local retry launcher (`z02-development-retry.py`, not distributed) is an operational
helper only. Its local import ordering was lint-cleaned after the launch;
the immutable archive's driver/proof/dependency inputs were not changed.

Z02 now supplies the conditional coefficient-to-mass sign bridge at development
compile scope. Z03 continuity/IVT is the next research obligation, not performed
here. No mass-zero existence, C04-to-Z composition, claim admission, commit,
push, tag or release was performed.
