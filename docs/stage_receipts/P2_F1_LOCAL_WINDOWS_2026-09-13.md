# P2 F1 local Windows execution receipt — 2026-09-13

`receipt_status: EXECUTED`

```text
check_status: PASS[PINNED_SOURCE_TOOLCHAIN:external_P2_F1_module]
claim_status: CONFIRMED for one named P2-F1 proposition only
```

This is a dated, local execution record. It establishes the recorded compile
result for the named external module under the identities below. It is not a
claim about the source theorem, the manuscript, the complete P2 analysis, or
the Navier--Stokes problem.

## Confirmed proposition scope

The recorded exit-zero compilation confirms only:

```text
0 < NavierStokes.OutgoingSchedule.mainMoment c (1 : Fin 2)
```

The module also compiles a lower bound
`1 / (5000 * c.lam) <= mainMoment c (1 : Fin 2)`, used internally to obtain
positivity. This receipt promotes only the positivity proposition above. It
does not establish the L2 normalized comparison, `DeltaM < 0`, a repair
coefficient sign, a first-repair interior zero, the paper's theorem, or the
Navier--Stokes problem.

## Identity and custody

| Field | Recorded value |
| --- | --- |
| Source repository | `https://github.com/openai/NavierStokesAndEuler` |
| Source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Source tracked-tree status before and after | `clean` |
| Lean toolchain | `Lean 4.34.0-rc2` (commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`) |
| Manifest committed Git blob SHA-1 | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| NSRW commit | `5876e3bb27d48299cb963f5a8f809a8b29852302` |
| NSRW tracked-tree status before and after | `clean` |
| Proof module | `formal/p2/P2_F1_MainMomentPositivity.lean` |
| Proof SHA-256 | `df9f605fa7ad9fa2842f54ae2d67b6a9b1773849d72c695192ae1bebe2f01206` |

The manifest Git blob is the portable source-admission identity. Runtime raw
hashes are executor observations and are not promoted to portable authority.

## Execution record

```text
executor: local Windows toolchain run
source target: lake build +NavierStokes.PulseAmplitude
source target exit: 0
external proof exit: 0
source stderr: empty
proof stderr: empty
```

| Output | SHA-256 |
| --- | --- |
| Source stdout | `1943f4a705d0cfc75b50aaa6490e1328e91e6294d2054c04859f8edac4674dd8` |
| Source stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Proof stdout | `92470e3d294a933195daa329cdcc9a8200f161c021276b4ca13435536c19ca18` |
| Proof stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Axiom-surface observation

Captured `#print axioms` output:

```text
'NSRW.P2.mainMoment_one_lower' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'NSRW.P2.mainMoment_one_pos' depends on axioms:
  [propext, Classical.choice, Quot.sound]
```

`sorryAx` was absent from the captured surface. This is an
introduced-placeholder/axiom-surface observation for the named compiled
declarations only; it is not a semantic audit of their imported proof chain.

## Boundary

The source and external proof were rebuilt in one clean execution chain at the
recorded NSRW commit. The receipt is local compiled evidence. It is not an
independent executor result, hosted CI result, full-library build, or paper--Lean
semantic-equivalence result.
