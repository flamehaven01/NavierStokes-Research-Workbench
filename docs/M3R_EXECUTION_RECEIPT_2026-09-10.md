# M3R Execution Receipt — 2026-09-10

Status: `M3R-1_PASS__M3R-2A_PASS__M3R-2B_HELD__M4_HELD`

## Scope

This receipt records the authorized Lean/Lake closure recovery for the
Navier–Stokes workbench. It does not claim a full default-library build, a
paper–Lean semantic equivalence, or a Navier–Stokes solution.

## Toolchain and source identity

- Repository: `openai/NavierStokesAndEuler`
- Commit: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`
- `lean-toolchain`: `leanprover/lean4:v4.34.0-rc2`
- Lean: `4.34.0-rc2` (`6a10ac8c22beadecabdbb0919c2b50214762f91d`)
- Lake: `5.0.0-src+6a10ac8`
- Elan: `4.2.4`
- `lake-manifest.json` remained pinned; no dependency update was performed.

## M3R-1 compiled closure

`lake build +NavierStokes.OutgoingDilation` completed with `EXIT=0` and
`2856/2856` jobs. The resulting target is:

```text
.lake/build/lib/lean/NavierStokes/OutgoingDilation.olean
SHA-256: E47FA3AFCA76ED83021C1F030E4FE3ACE43586CA03341EA4B2CAF42A913F344D
```

`lake env lean --deps NavierStokes/OutgoingDilation.lean` returned the direct
compiled dependencies:

```text
OutgoingProfile.olean
TerminalCompensation.olean
```

The target's terminal-tail chain was independently rebuilt in targeted runs:
`OutgoingSchedule`, `OutgoingTail`, `HeatTailEdit`, `ReleaseMoments`,
`CorrectedPulseAmplitude`, `SchedulePressure`, `ParametricRephase`,
`OutgoingProfile`, and `TerminalCompensation` all returned `EXIT=0` on their
successful retries.

The six canonical theorem declarations were checked with `#print axioms`:
`canonicalKernel_scaling`, `canonicalKernel_integral`,
`canonicalKernel_integrable`, `Pi_canonical`, `E_tail_factorization`, and
`eventual_power`. Every result contained only `propext`, `Classical.choice`,
and `Quot.sound`; no `sorryAx` was reported.

Raw output is preserved at
`outputs/m3r-theorem-axioms.txt`.

The broad default `lake build NavierStokes` remains
`ERROR[ENV_IO/OOM]` because parallel cache reads intermittently fail on
unrelated modules. It is retained as a separate negative observation and is
not conflated with the successful scoped target closure.

## M3R-2 source-instance closure

`TailData` is defined with explicit fields `core`, `h`, `h_pos`, and
`h_small` (`OutgoingTail.lean:103-107`), and `tailDataOfCore` sets `h :=
c.lam / 4` (`OutgoingTail.lean:820-824`). However, the actual profile path
uses existential choices in `exists_outgoing_profile` and
`exists_fixed_lambda` (`OutgoingProfile.lean:640-665`). The downstream
`switchStart` and `outgoingAmplitude` are explicitly `noncomputable`, and
`switchRadius` is derived from them. Therefore no concrete source-instance
numeric evaluation is admitted.

Result: `PASS[M3R-2A:static-provenance]`,
`HELD[M3R-2B:NONCOMPUTABLE_SOURCE_INSTANCE]`.

The independent parametric pressure-tail witness remains supported with
absolute integral error `6.233347171757941e-13`, including the `-1/2` factor;
it is not promoted to a concrete source-instance result.

## Transition

```text
M3R-1 compiled target/dependency    PASS
M3R-2A source provenance            PASS
M3R-2B concrete TailData instance   HELD
M3 engineering closure              HELD
M4                                 HELD
E2 HF/Colab                         HELD[PINNING_INCOMPLETE]
Paper–Lean semantic equivalence     OPEN RESEARCH OBLIGATION
```

Next research action is to expose or formally characterize the first
non-evaluable existential parameter; do not fabricate a numeric witness.
