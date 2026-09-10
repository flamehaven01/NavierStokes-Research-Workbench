# M3 Evidence Execution Addendum — 2026-09-09

Status: `HELD_LEAN_TOOLCHAIN_AND_SOURCE_INSTANCE__M4_HELD`

## Purpose

This addendum records the post-review M3 evidence execution without modifying the original session handoff file. The handoff remains preserved at SHA-256 `353ce46db32a9d0110258b29b3899b329213e5f8ce967ab4b0ec31ccac9e66ba`.

This is claim custody, not proof authority. The local executable and static checks strengthen the inspectable surface while the global Navier–Stokes theorem claim remains `UNVERIFIED`.

## Executed evidence

### Lean / Lake build

Status: `ERROR[TOOLCHAIN_MISSING]`

- `lake` not available on PATH.
- `lean` not available on PATH.
- no toolchain installation was performed;
- no formal source file was modified;
- therefore no compiled Lean dependency graph, successful build, or proof-validity claim exists from this execution.

### Static theorem dependency surface

Status: `PASS[STATIC_SOURCE]`

- required declaration surface: `6/6` present;
- evidence authority: static formal-source inspection only;
- this does not establish a compiled dependency graph;
- this does not establish Lean proof validity;
- this does not establish paper–Lean semantic equivalence.

### Canonical pressure tail

Status: `PASS[PARAMETRIC_SOURCE_TAIL]`

The independent numerical check used the source structures/declarations associated with:

- `canonicalKernel`;
- `Pi_canonical`;
- `powerTail`;
- `E_tail_factorization`.

A log-coordinate integration reproduced the parametric source pressure tail with absolute error:

`6.233347171757941e-13`

The `-1/2` pressure coefficient was also reproduced.

Boundary:

The concrete noncomputable `TailData` amplitude/radius were not evaluated by Lean. Therefore the parametric identity is not promoted to a concrete source-instance closure.

Source-instance status: `HELD[PARAMETERS_NOT_EVALUATED_BY_LEAN]`.

## Fresh local verification

- pytest: `151 passed`;
- coverage: `93.71%` against the configured 90% floor;
- Ruff: `PASS`;
- compileall: `PASS`;
- slop diagnostic: `clean`;
- slop runtime coverage: `23/23` files analyzed.

These results establish the current local software/diagnostic surface only. They do not establish Theorem 4.6, the global Navier–Stokes claim, or paper–Lean semantic equivalence.

## Evidence receipt

Canonical evidence receipt SHA-256:

`3253664E2EA3A13C9678BBC7629130473309708CDA93AB574ED1CE8090985AD5`

Detailed execution report was produced outside the workbench at:

`<local-session-output>/NSRW-M3-Evidence-Execution-Report.md`

That external path was session-local execution provenance; this public addendum
does not independently assert access to the original local workspace artifact.

## Gate result

Final M3 gate:

`HELD_LEAN_TOOLCHAIN_AND_SOURCE_INSTANCE`

Reason:

1. local M3 code/test/quality gates pass;
2. static formal-source dependency surface is present;
3. the parametric canonical pressure tail is independently reproduced;
4. Lean/Lake compilation is unavailable because the toolchain is missing;
5. concrete noncomputable source-instance `TailData` parameters have not been evaluated by Lean;
6. paper–Lean semantic equivalence remains unverified.

M4 remains `HELD`.

## External HF / Colab lane

The Colab + Hugging Face lane is a separate experiment gate and does not bypass M3.

Current E2 status: `HELD[PINNING_INCOMPLETE]`.

The actual HF/Colab execution has not started because the following custody fields are not yet pinned:

- Hugging Face repository revision/commit;
- exact file or shard;
- sample/trajectory id;
- source/download hash.

No external dataset/model result should be admitted into the workbench until those fields are fixed in the E2 contract.

## Next transition

Do not enter M4 until one of the following occurs:

- Lean/Lake is available in an authorized pinned environment and the required formal build/dependency evidence is produced; and
- the concrete source-instance tail parameters are resolved or their continued noncomputability is documented as an intentional hard boundary with an accepted alternative witness.

The external E2 lane may proceed independently once its source pinning contract is complete, but its results remain `EXTERNAL_REPRODUCIBLE_NUMERICAL_EXPERIMENT` evidence and cannot promote the theorem claim.
