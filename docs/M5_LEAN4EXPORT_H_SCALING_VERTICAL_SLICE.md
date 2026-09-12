# M5 Lean export compatibility and `H_scaling` vertical slice

Status: `M5_1_PASS[LOCAL_COMPATIBILITY_SPIKE]__M5_2_PASS[LOCAL_SOURCE_DERIVED_VERTICAL_SLICE]__REVIEWER_REPLAY_NOT_EXECUTED[RUNTIME_MISMATCH]`

This is the execution contract for the first M5 source-derived mathematical
slice. It is intentionally narrower than a general Lean normalization system.

## Acceptance principle

M5 begins successfully when one real Lean declaration is carried from pinned
source, through Lean-native export and minimal loss-aware normalization, into
an independent mathematical reconstruction with a bounded reproducible
receipt. Schema count, graph size, and declaration count are not success
criteria.

```text
pinned Lean source + pinned toolchain
            |
            v
pinned Lean-native export
            |
            v
minimal loss-aware normalization
            |
            v
independent mathematical reconstruction
            |
            v
bounded reproducible receipt
```

The source remains authoritative for what Lean states. Raw export is a
source-derived transport artifact; normalization and Python evaluation have
progressively narrower authority.

## 1. Exact source and exporter

| Item | Pinned identity |
|---|---|
| Formal repository | `openai/NavierStokesAndEuler` |
| Formal source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Source worktree at execution | clean |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| Lean Git hash reported by export | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Source module | `NavierStokes.OutgoingDilation` |
| Declaration | `NavierStokes.OutgoingDilation.H_scaling` |
| Source file SHA-256 | `be46401810940d1021c2f2ccf0ce00bdffef82d413f2146742564d15c5516438` |
| Source manifest SHA-256 | `d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f` |
| Exporter repository | `leanprover/lean4export` |
| Exporter commit | `cacf989bd75f608700820f6afc595f32e7a99a4d` |
| Exporter selection rule | revision already pinned by the formal source's `lake-manifest.json` |
| Export format | NDJSON `3.1.0` |
| Exporter binary SHA-256 | `a638952892fede28e6b530243dc4f15a5d0fddd988f3f2494ded812249315234` |
| Upstream license | Apache License 2.0; exporter code and raw output are not vendored here |

The manifest-pinned exporter is used instead of an arbitrary current release.
Exporter and formal source require the same Lean toolchain.

## 2. M5-1 compatibility result

The exporter was built from its existing dependency checkout without editing
either upstream repository. Build result: exit `0`, 6 of 6 jobs.

Equivalent invocation from the pinned formal-source root:

```text
lake env .lake/packages/lean4export/.lake/build/bin/lean4export \
  NavierStokes.OutgoingDilation -- \
  NavierStokes.OutgoingDilation.H_scaling > H_scaling.ndjson
```

The command was run twice in the same local environment:

| Run | Exit | Stderr bytes | Elapsed | Output bytes | SHA-256 |
|---:|---:|---:|---:|---:|---|
| 1 | 0 | 0 | 302.489 s | 237,875,864 | `129f7dee6cf93f3588c4cceb13d55cb88345f39b525bfbbd58031eb0f7cd0148` |
| 2 | 0 | 0 | 77.713 s | 237,875,864 | `129f7dee6cf93f3588c4cceb13d55cb88345f39b525bfbbd58031eb0f7cd0148` |

Observed output:

- byte-identical across the two runs;
- 4,408,528 NDJSON records;
- metadata reports exporter `3.1.0`, format `3.1.0`, and Lean
  `4.34.0-rc2`;
- the final theorem record names declaration ID `240819`, type expression ID
  `4127204`, and value expression ID `4127601`;
- name records resolve ID `240819` to
  `NavierStokes.OutgoingDilation.H_scaling`.

Decision: `DETERMINISTIC_BUT_LARGE`. The 237.9 MB raw output is not a Git
fixture. It remains an external local artifact; this document retains its
digest and bounded observations. A future hosted run may publish it only as a
run artifact with retention policy and provenance, not as source authority.
The local artifact is not protected or independently attested, so its digest
supports this local compatibility observation only.

The elapsed times are observations from one machine, not performance claims.
The first/warm-run difference is not interpreted further.

## 3. M5-2 declaration surface

The pinned source states:

```text
H F XR p = Real.sqrt XR * F.H (p.1 / XR, p.2)
```

under the explicit hypothesis `0 < XR`. Its nearby definitions are:

```text
E F XR p = F.E (p.1 / XR, p.2)
H F XR p = Real.sqrt (2 * p.1) * E F XR p
F.H p     = Real.sqrt (2 * p.1) * F.E p
```

The independent executable surface is therefore limited to reconstructing
both sides from these definitions and checking the scaling identity. It does
not reproduce the Lean proof term and does not establish the theorem
independently for all profiles.

### Minimal normalized record

Only the following information may enter the first normalized record:

- formal source commit, module, and fully qualified declaration name;
- declaration kind;
- ordered binder sequence and exported `binderInfo`;
- elaborated theorem type and only the expression subgraph needed by that type;
- referenced constants in that retained subgraph;
- exporter commit, Lean identity, export-format version, raw digest, and
  normalized digest;
- explicit loss records.

An unsupported expression constructor is preserved as `OPAQUE_EXPR` with its
original expression ID and constructor name. If an opaque node lies on the
equation-critical type subtree, the slice is held; it must not be guessed from
pretty-printed source. No generalized obligation schema or paper crosswalk is
part of this slice.

### Independent reconstruction

The implementation must define its own left and right expressions from the
source definitions. It must not call one side from the other. The bounded test
domain must include:

- more than one independently defined profile function `E`;
- positive `XR` values at separated scales;
- negative, zero, and positive first coordinates `p.1`;
- multiple second coordinates `p.2`;
- Lean-compatible real square root behavior, including zero for negative
  arguments;
- explicit rejection of `XR <= 0`, because those values are outside the
  theorem hypothesis.

High-precision sampled comparison must record precision and tolerance. A
separate algebraic check may be added, but a finite grid remains a bounded
reconstruction rather than a universal proof.

At minimum, mutations that change the `sqrt XR` factor or remove the
`p.1 / XR` argument scaling must be rejected by the executable comparison.

## 4. Gates and non-claims

M5-2 closes only if all of the following hold:

1. the raw digest and export metadata match this pinned M5-1 input;
2. the target declaration and ordered binders are decoded from NDJSON rather
   than scraped from Lean source text;
3. every omitted or unsupported expression is explicit and none lies on the
   equation-critical type subtree;
4. the normalized record is deterministic and schema-valid;
5. the independent left/right implementations pass the declared bounded
   domain and the two required mutations fail;
6. a deterministic receipt binds source, raw export, normalized record, code,
   domain, precision, tolerance, and results.

Current local implementation result:

```text
M5-1 exporter compatibility       PASS[LOCAL_COMPATIBILITY_SPIKE]
M5-2 normalized declaration       PASS[LOCAL_SOURCE_DERIVED_VERTICAL_SLICE]
M5-2 independent reconstruction   PASS[LOCAL_SOURCE_DERIVED_VERTICAL_SLICE]
M5 first vertical slice           PASS[LOCAL_SOURCE_DERIVED_VERTICAL_SLICE]
M5 reviewer-operated full replay  NOT_EXECUTED[REVIEWER_RUNTIME_MISMATCH]
M5 P1 static scaling analysis     PASS[LOCAL_REVIEWED_METADATA]
M5 P1 source-bound atlas          HELD[LEDGER_NOT_INDEPENDENTLY_PINNED]
M5 broader source coverage        OPEN
```

See `docs/stage_receipts/M5_H_SCALING_LOCAL.md` for the bounded local receipt.
That receipt binds the implementation, tests, project configuration, runtime,
raw export, normalized record, domain, precision, tolerance, and results by
content identity. The reviewer-runtime boundary prevents a claim of
independent replay.
This result does not independently verify the Lean theorem, the OpenAI
manuscript, a selected blowup candidate, or the Navier--Stokes millennium
problem. It establishes only that the pinned declaration can be exported
reproducibly in the observed local environment and defines the next bounded
mathematical reconstruction.

The P1 atlas extension is defined separately in
`docs/M5_OUTGOING_DILATION_SCALING_ATLAS_P1.md`. It adds only reviewed static
metadata and exact exponent algebra at this point. The pending same-raw export
and ledger gate must not be inferred from this one-declaration receipt.
