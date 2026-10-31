# Reproduce the P01 formal inputs

This guide accompanies the mathematical manuscript. It describes a new reproduction,
not a claim that an independent investigator has already performed one.

## Fixed inputs

| Item | Identity |
|---|---|
| NSRW execution checkout | `3a50b5f50b034319a469b9de68f556be70fff02c` |
| Earlier dependency-base checkout | `10d5a1f517b8665137f2354746d70752f8ef67fd` |
| Upstream source | `openai/NavierStokesAndEuler` at `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| Reference execution | `nsrw-z-phase-replay-20261012T065216884451Z` |

## Linux/Colab procedure

Prerequisites: Git, Python >=3.10, the installed pinned Lean/Lake toolchain,
and network access for the pinned dependency checkouts/cache. The instructions
do not use `lake update`. Begin in an empty working directory. The output
directory `run-z` must not already exist.

```sh
git clone https://github.com/openai/NavierStokesAndEuler.git source
git -C source checkout --detach 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538
git clone https://github.com/flamehaven01/NavierStokes-Research-Workbench.git nsrw
git -C nsrw checkout --detach 3a50b5f50b034319a469b9de68f556be70fff02c
git clone ./nsrw nsrw-base
git -C nsrw-base checkout --detach 10d5a1f517b8665137f2354746d70752f8ef67fd
cd source
lake exe cache get
lake env lean --version
cd ..
python3 nsrw/scripts/run-p2-z-replay.py \
  --source-root ./source \
  --nsrw-root ./nsrw \
  --dependency-base ./nsrw-base \
  --output-dir ./run-z \
  --expected-nsrw-commit 3a50b5f50b034319a469b9de68f556be70fff02c
```

The runner checks pinned source/toolchain/dependency identities, builds
`NavierStokes.OutgoingProfile`, then compiles fourteen fresh external modules.
Cache restoration is not a clean rebuild of every upstream library file.
The replay command is not a PowerShell command and is not the Windows software
test procedure for software-only checks.

Compare the named statements, exact committed inputs, fifteen stage exits,
empty stage stderr, fourteen fresh external outputs and nineteen named axiom
surfaces. Each expected surface contains `propext`, `Classical.choice` and
`Quot.sound`, without `sorryAx`. New timings, binary hashes and timestamps may
differ from the reference execution. A completed replay does not perform
manuscript interpretation or automatically admit a broader mathematical claim.

## Distributed records

The distribution candidate includes exact committed proof/driver inputs,
two unchanged post-execution receipt snapshots, selected axiom lines and a
bounded stage summary. The receipts are separate documents, **not files claimed
to exist at the execution commit**. They refer to one shared reference execution,
not two independent replications.

The original archive is privately retained: 815996 bytes, SHA-256
`bd109a6f0db1eaaa1e6054d5ba16f8e07696434f7ffebb5527128f721267d74b`.
Raw logs, runtime metadata, compiled binaries and caches are not supplied in
the public subset. A digest of an excluded file does not provide access to it.
The selected documentary [history](supplement/DEVELOPMENT_HISTORY.md) is an
explanation of recorded incidents, not a reconstruction of missing logs.

The package manifest identifies included bytes. A separate sidecar identifies
the completed ZIP. Neither replaces an independent reproduction. No DOI or
published download URL is asserted before an actual approved deposit.

## Licensing

The authored P01 manuscript uses [CC BY 4.0](LICENSE-PAPERS.md).
NSRW code uses MIT. Upstream source is linked rather than bundled and retains
its own license. Internal review records and the deferred P03 manuscript are
not part of this distribution selection.


## Quantitative margin and normalized plateau extension

The ten later exact-real propositions use a different, separately fixed replay at `7f29ebf0e2b894bf598144628230ae09df436c3d`; do not change the qualitative replay checkout above. In another clean NSRW checkout and with the same pinned upstream environment, run the following POSIX shell commands:

```sh
git clone https://github.com/flamehaven01/NavierStokes-Research-Workbench.git nsrw-margin
git -C nsrw-margin checkout --detach 7f29ebf0e2b894bf598144628230ae09df436c3d
python3 nsrw-margin/scripts/run-p1-margin-replay.py \
  --source-root ./source \
  --nsrw-root ./nsrw-margin \
  --output-dir ./run-margin \
  --expected-nsrw-commit 7f29ebf0e2b894bf598144628230ae09df436c3d
```

The new output directory must be absent. This command builds the source target and five fresh external modules, and checks the ten named quantitative/normalization axiom surfaces. Compare with the [22 October receipt](../docs/stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md). Its post-execution document identity is separate from the execution commit. Neither the reference nor a new same-operator replay is an independent external reproduction.

## Exact-rational core-scalar experiment

This is a separate Python experiment, not a Lean replay or full source-instance certificate. At software release v0.5.0, from the repository root with Python >=3.10:

```sh
PYTHONPATH=src python3 -m nsrw.math_kernel.p2_core_scalars produce --precision 128 --output core.json
PYTHONPATH=src python3 -m nsrw.math_kernel.p2_core_scalars verify --input core.json
```

PowerShell uses `$env:PYTHONPATH = "src"` followed by the same `python -m ...` commands. Repeat with 256 or 512 fractional bits. The verifier recomputes all exact-rational bounds and rejects changed fields/inputs/scope. It shares the producer algorithm and does not independently establish source admissibility. See the [method](../docs/P2_CORE_SCALAR_METHOD_2026-10-31.md) and [public records](../examples/p2-core-scalars/).

## Published paper records - 31 October 2026

- P01 mathematics v0.5: [10.5281/zenodo.23835054](https://doi.org/10.5281/zenodo.23835054).
- P02 software case study v0.6: [10.5281/zenodo.23835112](https://doi.org/10.5281/zenodo.23835112).

These are separate preprints, linked to the [software archive](https://doi.org/10.5281/zenodo.23381778). A publication DOI is not a new proof execution or an independent validation.
