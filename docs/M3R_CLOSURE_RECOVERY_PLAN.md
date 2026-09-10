# M3R — Closure Recovery

Status: `M3R_ACTIVE__M4_HELD__E2_HELD`

M3 is not a project-wide freeze. The freeze applies to M4 promotion and the
HF/Colab E2 execution. M3R is the focused recovery lane for the two remaining
evidence blockers.

## Gates

```text
M3 implementation                         PASS
M3 tests / quality / replay                PASS
M3R-1 compiled Lean + dependency graph     REQUIRED
M3R-2 concrete TailData source instance   REQUIRED
------------------------------------------------
M3 engineering closure                    PASS possible

Paper–Lean full semantic equivalence       OPEN RESEARCH OBLIGATION
M4                                       HELD until M3R-1 and M3R-2
E2 HF/Colab                              HELD[PINNING_INCOMPLETE]
```

Full paper–Lean semantic equivalence is intentionally not a hard M4 gate. It
remains a named research obligation and must not be silently promoted by a
compiled build. M4 may open only when the declarations it uses and their
concrete source-instance parameters are compiled and evidenced.

## M3R-1 — Lean toolchain recovery

1. Read `lean-toolchain` and record the exact required version:
   `leanprover/lean4:v4.34.0-rc2`.
2. Preserve `lakefile.toml` and the pinned `lake-manifest.json`; do not update
   dependency revisions during recovery.
3. Provision the matching Lean/Lake toolchain in an authorized environment.
4. Run `lake build` for the declared default targets.
5. Run the Comparator target(s) for the Navier–Stokes declarations.
6. Export compiler output, target names, dependency/import graph, toolchain
   version, repository commit, and manifest hash.

`PASS[COMPILED]` requires a successful build and a dependency graph containing
the actual M4 prerequisites. Static declaration presence remains a separate
`SUPPORTED` observation. A missing executable is `ERROR[TOOLCHAIN_MISSING]`,
not a failed theorem.

## M3R-2 — concrete source-instance tail

1. Trace the construction path from `ActualCandidateAssembly` to the concrete
   `OutgoingProfile.Profile` / `TailData` instance.
2. Record the definitions and source locators for `h`, `outgoingAmplitude`,
   `switchRadius`, `tailEnd`, and the terminal taper boundary.
3. Classify every parameter as numerically evaluable, proposition-only, or
   noncomputable/existence-only.
4. If `amplitude`, `radius`, and `h` are evaluable, feed the exact values into
   the independent pressure-tail witness and compare the resulting integral
   and `-1/2` pressure value.
5. If they are not evaluable, produce a boundary receipt naming the first
   non-evaluable definition and retain the current parametric result as
   `SUPPORTED`, not `CONFIRMED` source-instance closure.

The existing source law is the eventual pure tail after the taper:

```text
E(X,η) = A (X/K)^(-(1/2+h))
∫_X^∞ E(s,η)^2 / s ds
  = A² (X/K)^(-2(1/2+h)) / (2(1/2+h))
Pi_tail(X,η) = -1/2 × that integral
```

The equality is only admitted for a cutoff at or beyond the source terminal
taper. A finite cutoff before that boundary is not treated as infinity.

## Current recovery evidence (2026-09-10)

- Toolchain identity is now provisioned and recorded: Lean `4.34.0-rc2`,
  Lake `5.0.0-src+6a10ac8`, Elan `4.2.4`; the repository remains pinned to
  `leanprover/lean4:v4.34.0-rc2` with no manifest update.
- `PASS[M3R-1:compiled-target]`: `lake build +NavierStokes.OutgoingDilation`
  completed successfully (`2856/2856` jobs) and produced the target
  `.olean`.
- `PASS[M3R-1:compiled-dependency]`: `lean --deps` on the compiled source
  reports direct compiled dependencies `OutgoingProfile.olean` and
  `TerminalCompensation.olean`; the transitive terminal-tail chain was also
  rebuilt successfully in targeted retries.
- `PASS[M3R-1:theorem-axioms]`: the six canonical declarations were checked
  with `#print axioms`; no `sorryAx` occurs. The reported base axioms are
  `propext`, `Classical.choice`, and `Quot.sound`.
- `ERROR[M3R-1:default-library]`: the broad default `NavierStokes` target is
  not a clean gate in this environment; parallel cache reads still produce
  intermittent missing-artifact/OOM failures. This does not invalidate the
  successful scoped M4 prerequisite target above.
- `PASS[M3R-2A:static-provenance]`: `TailData.h`, `tailStart`, `tailEnd`,
  `powerConstant`, `switchStart`, `outgoingAmplitude`, and `switchRadius`
  were traced to their source definitions.
- `HELD[M3R-2B:source-instance]`: `exists_outgoing_profile` and
  `exists_fixed_lambda` expose existential/noncomputable choices; no concrete
  numeric `TailData` amplitude/radius instance is available for evaluation.
  The parametric tail witness therefore remains `SUPPORTED`, not source-
  instance closure.
- Parametric tail witness: numerical log-coordinate quadrature passes with
  absolute error `6.233347171757941e-13`, including the `-1/2` factor.

## North-star check

M3R is justified because it closes two concrete mathematical custody gaps,
not because it adds another receipt. Every M3R artifact must answer which
quantity or dependency became observable, what independent check was applied,
and what remains outside scope. The semantic-equivalence question remains open
and visible rather than being converted into an administrative blocker.
