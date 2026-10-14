# P2 Z-03 conditional IVT development — 2026-10-10

This is a development execution record, not a commit-bound receipt or claim admission.

```yaml
implementation: WRITTEN[CONDITIONAL_LOCAL_MASS_INTERIOR_ZERO]
driver_controls: PASS[FOCUSED_PYTEST:13_TESTS]
lint: PASS[RUFF:Z03_DRIVER_LAUNCHER_AND_TESTS]
lean_compile: PASS[LOCAL_PROOF_COMPILE:P2_Z03]
claim_authority: NONE
claim_status: UNVERIFIED
Z04: DEFERRED[USER_WILL_SUPPLY_ADDITIONAL_TASKS]
```

## Scope

[The proof](../formal/p2/P2_Z03_ConditionalInteriorZero.lean) imports only
`P2_Z02_BoundaryMassSigns`. Three named theorem targets:

- `massMoment_continuous`: the source mass primitive is continuous in y for fixed F, eta.
- `localMass_continuousOn_firstRepair`: the same local mass is continuous on `[l0,u0]`.
- `exists_firstRepair_zero_of_secondCoeff_pos`: eta > 0 and actual second axial
  coefficient > 0 imply an r strictly inside `(l0,u0)` with localMass = 0.

The last theorem excludes both endpoints explicitly using the strict boundary
signs. It does not assert that this is the first or unique zero.

C04 is not imported or replayed. No existential epsilon, uniform/numerical
radius, Profile.M coordinate conversion, J behavior, nonremovable singularity,
upstream verification, paper equivalence or independent novelty is supplied.
Z04 composition is not started, per explicit user instruction.

## Source-native route

The connected VM's source commit was read as
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`. Direct source-file reading confirmed:

```text
massMoment = 4 * eta + integral 0..y of exp(t) * axial(t,eta)
axial_radial_contDiff: fixed c, amp, eta gives radial ContDiff
```

Pinned mathlib inspection confirmed `intervalIntegral.continuous_primitive`
consumes interval integrability for every a,b, and `intermediate_value_Icc'`
maps `[f(b), f(a)]` into `f '' [a,b]`. No radial partial integral was rederived.
Continuity of log is restricted to the positive first-window interval.

## Exact initial execution

```text
run: nsrw-z03-development-20261010T115139Z
helper commit: 10d5a1f517b8665137f2354746d70752f8ef67fd
proof SHA-256: 5e174ab2281ad0b20b8bc684977bcd0bfa5ecc4f79351ac60cb56ed99d043d40
Z01 SHA-256: ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267
Z02 SHA-256: 7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c
driver SHA-256: 314eb92a6ad787a993653e7a36b667e5afd42e8fdfd1792b104a441fdcd83fc3
chain: source OutgoingProfile -> fresh Z01 -> fresh Z02 -> fresh Z03
```

[Runner](run-z03-development.py) is public. The launcher (`z03-development-start.py`)
and observer (`z03-development-observe.py`) are local-only helpers, not distributed.
The runner preserves
raw binary logs, committed source-identity helper bytes, exact proof/dependency
inputs, fresh artifacts, source pre/post identity and target artifact hashes.
It preserves failed archives and never promotes claim status.

The first focused test run found a Windows cp949 decoding defect in the test's
Lean-source read. Explicit UTF-8 fixed that test only; 13 focused tests then
passed. These synthetic checks are not Lean evidence.

No Windows install, dependency update, commit, push, tag or release is authorized
or performed by this development step. Successful/failed archives are preserved
under `colab/evidence/2026-10-10/<unique-run>/` after execution.

## Successful development execution and preservation

The initial proof compiled without Lean source repair. The run finished at
`2026-10-10T11:53:06.661609+00:00`. Source, fresh Z01, fresh Z02 and fresh Z03
all exited 0 with empty stderr. Each of Z03's three named axiom surfaces is
exactly `[propext, Classical.choice, Quot.sound]`; `sorryAx` is absent.
The successful proof bytes still have the SHA recorded above.

```text
check_status: PASS[LOCAL_PROOF_COMPILE:P2_Z03]
artifact_check: PASS[LOCAL_ARCHIVE_INPUT_LOG_ARTIFACT_CROSSCHECK]
claim_authority: NONE
claim_status: UNVERIFIED
archive: nsrw-z03-development-20261010T115139Z-evidence.zip
archive bytes: 168292
archive SHA-256: 465bd6f081307cd975bdbc7757bc0157526339f98939932e672380bd11e5638e
local store: colab/evidence/2026-10-10/nsrw-z03-development-20261010T115139Z/
```

The archive was transferred through explicit Colab output and its hash
crosschecked before local extraction. All 17 entries were path-checked. Local
review recomputed five input hashes, three fresh artifact hashes and eight log
hashes against metadata. Source pre/post identities and `OutgoingProfile.olean`
pre/post hashes match. Source cache was reused, not a full clean-library rebuild.
Execution and preservation review share one trust domain, not independent attestation.

The actual theorem is conditional: eta > 0 and second axial coefficient > 0
imply an interior local mass zero. It is not yet the unconditional per-Profile
small-positive-eta conclusion. No Z04 module was created or run. Further Z04
assembly/replay/receipt work waits for the user's additional tasks. No claim
admission or commit/push has been performed.
