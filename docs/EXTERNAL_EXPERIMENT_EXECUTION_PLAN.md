# External experiment execution plan

Status: `E2_CONTRACT_IMPLEMENTED__INPUT_PINNING_REQUIRED__M3_BOUNDARY_PRESERVED`

This plan turns `EXTERNAL_EXPERIMENT_LANDSCAPE_HF_COLAB.md` into a bounded
execution sequence. The external lane is a numerical/control/falsification
surface; it cannot promote the forced OpenAI result, the Lean source, or the
Clay claim.

## `#map-north-star` placement

The external lane is useful only when it advances one of the map's research
questions: expose an equation-level quantity, independently reconstruct it,
kill an alternative, or produce the next proof obligation. The E2 artifact
therefore starts with a vorticity-only trajectory and no learned model.

```text
HF source + pinned sample
        ↓
2-D periodic vorticity ω
        ↓  independent FFT Poisson reconstruction
(u, v), div(u), curl(u), energy, enstrophy
        ↓
machine receipt + explicit non-claims
        ↓
E3 rollout question / M3-informed falsifier
```

This does not enter the M3 theorem path. It can inform that path only by
revealing a concrete mismatch or a quantitative diagnostic worth formalizing.

## Implemented E2 surface

`src/nsrw/external_experiments/fno_dataset_audit.py` implements:

1. a fail-closed source contract (`revision`, `file`, `forcing_scope`, domain
   lengths, dimension, representation, and periodic domain are explicit);
2. a deterministic spectral solve of `-Δψ = ω`, `u = ψ_y`, `v = -ψ_x`;
3. independent checks for finite input, zero-mean vorticity, spectral
   divergence, and vorticity reconstruction;
4. per-step energy and enstrophy metrics; and
5. a receipt whose theorem `claim_status` is always `UNVERIFIED`.

The machine contract is in `fixtures/external-e2-contract-v1.json`. It is a
design fixture until an actual HF revision, file, bounded sample, and hashes
are supplied. The module does not download data or infer missing provenance.
NumPy is a development/Colab dependency for this numerical surface; it is not
required by the base contract and receipt pipeline.

## Execution gates

### E2-G0 — admission

`GO` only if the source revision, file, source-file SHA-256, sample id, array
shape, domain lengths, and forcing scope are recorded. Otherwise
`HELD[INPUT_PINNING]`.

### E2-G1 — reconstruction

`GO` only if all four physical checks pass at a declared tolerance and the
receipt is byte-stable on replay. A nonzero mean vorticity is a visible failure,
not a silently discarded Fourier mode.

### E2-G2 — interpretation

The receipt may support “this bounded 2-D sample passed the declared
diagnostics.” It may not support a 3-D theorem, a uniform estimate, a learned
model claim, or a forced/unforced equivalence.

### E3 entry

Only after E2-G1 is green should an FNO/PINO rollout be admitted. E3 must keep
prediction metrics and physics metrics in separate receipt branches. A low L2
error is not a PDE residual or incompressibility proof.

## Four-stage research ladder

| Stage | Mechanism exposed | Required falsifier | North-star value |
|---|---|---|---|
| E1 Taylor–Green | known analytic field and derivative error | grid refinement | calibration |
| E2 HF trajectory | dataset-to-field representation loss | mean/divergence/curl mutation | independent observation |
| E3 FNO rollout | learned temporal drift | long-horizon physics failure | forecasting boundary |
| E4 forced/unforced | scope custody | omitted/merged forcing term | theorem-scope protection |

The next concrete artifact is the project-owned Colab notebook that materializes
E2-G0/E2-G1. Until then the contract is intentionally `DESIGN_ONLY` and no
external result is reported as executed.

## Reviewer protocol

The architect/reviewer lane reviews each stage against this document and
`docs/NAVIER_STOKES_NORTH_STAR_MAP.md` before a stage changes from `HELD` to
`GO`. Review output must name: the exact quantity exposed, the independent
check, the killed alternative (if any), remaining semantic debt, and the
non-claim boundary. A reviewer opinion never substitutes for a Lean build or
mathematical proof.
