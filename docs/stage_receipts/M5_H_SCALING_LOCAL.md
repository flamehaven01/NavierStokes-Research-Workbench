# M5 `H_scaling` local vertical-slice receipt

Status: `PASS[LOCAL_SOURCE_DERIVED_VERTICAL_SLICE]__REVIEWER_REPLAY_NOT_EXECUTED[RUNTIME_MISMATCH]`

Date: 2026-09-12

## Scope

This receipt covers one source-derived mathematical declaration only:
`NavierStokes.OutgoingDilation.H_scaling`. It is not a Lean proof
verification, an informal-paper verification, or a Navier--Stokes theorem
claim.

## Input binding

| Item | Value |
|---|---|
| Formal source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| Lean4Export commit | `cacf989bd75f608700820f6afc595f32e7a99a4d` |
| Raw export SHA-256 | `129f7dee6cf93f3588c4cceb13d55cb88345f39b525bfbbd58031eb0f7cd0148` |
| Raw export bytes | `237875864` |
| Raw export records | `4408528` |
| Raw export storage | external local artifact; not committed |
| Normalized fixture | `fixtures/m5/h_scaling.normalized.json` |
| Normalized fixture SHA-256 | `466a52a2e266ffcfe580f0b183526b8154a294f4c020969bb88e1dff0647f543` |
| Canonical normalized semantic SHA-256 | `5f7773b0de7a5776b40a44ac9065be9f80b19929a94cf0930345383ed262e677` |

## Implementation and execution binding

The repository base commit identifies the reviewed repository lineage. The M5
files below were uncommitted when this local receipt was regenerated, so this
receipt binds their content hashes rather than presenting them as release
artifacts.

| Item | Value |
|---|---|
| Repository base commit | `75d0c1fc974f6fcec255c5ab38848717ceedcddb` |
| Worktree state | uncommitted M5 worktree; bound by the hashes below |
| `src/nsrw/m5/lean_export.py` | `cc751e58954d27f19416f713a5e74c6e900a5bf9f85e0c0d68a5e142f38aa2df` |
| `src/nsrw/m5/h_scaling.py` | `2b97448bc6929781a3cbeccdbce9d718cd893a3e12a4c44ddae0d0e60e3ad604` |
| `src/nsrw/schema_admission.py` | `58e2802dd20c761c632e5f423acc43450cb478b1c2f3e60b54eb07a519a95d32` |
| `contracts/lean-declaration-normalized-v1.schema.json` | `88406268ca4f321ea86d990194baf9ffa078943445a723e11e98b40e1eec7729` |
| `tests/test_m5_lean_export.py` | `7b66722771063ad2467fec0bd757a3a66356b6ef50030db3cb5a83af08aee080` |
| `tests/test_m5_h_scaling.py` | `bb2bd536f64f92aba8edc8e175b945b9c0ac8c6db3952e2e6cc19172b32cd788` |
| `pyproject.toml` | `5afd2d689f7d02910e0914bc5ad601ed2fe7c80369453785b6c77227905ad97a` |
| Python runtime | `CPython 3.14.3` |
| pytest | `9.0.2` |
| Operating-system family | `nt` |

The full-suite command was `python -m pytest`. The raw-export integration
command was `python -m pytest --no-cov tests/test_m5_lean_export.py::test_actual_h_scaling_export_when_explicitly_provided`, with the admitted raw
export selected through the `NSRW_M5_RAW_EXPORT` environment variable. No
absolute local path is part of this public receipt.

## Source-derived extraction

- The reader streams NDJSON and records only Lean names and expression byte
  offsets during its first pass.
- It follows theorem type root `4127204` by offset; theorem proof value ID
  `4127601` is retained as provenance but never dereferenced.
- Reachable type nodes: `78`.
- Export-decoded outer binder sequence: `F`, `XR`, `hXR`, `p`.
- Normalization status: `PASS`; `losses: []`.
- Normalizing the second byte-identical raw export produced canonical semantic
  bytes identical to the committed normalized fixture.
- The normalizer does not accept a Lean source-file path and has no
  pretty-printed-source fallback.

## Closure patches after separate-role review

1. The calculator now schema-admits the complete normalized record and binds
   the exact source/export fields, root ID, proof-value ID, binder sequence,
   78-node count, empty loss list, and canonical semantic SHA-256 before any
   numerical evaluation. A same-name/same-binder expression-body mutation is
   a regression test and must fail this binding.
2. The normalized writer now emits UTF-8 bytes with LF line endings. The
   pre-patch uncommitted CRLF file hash is superseded; the current fixture has
   no CRLF bytes and the canonical semantic digest is unchanged.

## Bounded independent reconstruction

| Item | Value |
|---|---|
| Evidence class | `BOUNDED_SOURCE_DERIVED_IDENTITY_RECONSTRUCTION` |
| Numeric backend | `decimal.Decimal` |
| Precision | 80 decimal digits |
| Tolerance | `1E-60` |
| Profiles | `polynomial_even`, `polynomial_mixed` |
| Samples | 144 |
| Maximum absolute error | `3E-71` |
| `M5-H-001` factor mutation | detected; maximum error `353554490.14431850728182262436540759268267405676412012387129682936617940741002878` |
| `M5-H-002` argument mutation | detected; maximum error `18122377696.821377611948818447845663082326055065685556216846432673432852795582989` |

The Python left side uses `dilated_e`; the right side uses `base_h` and does
not call the left-side implementation. Both preserve Lean-compatible real
square-root behavior at negative first-coordinate inputs. `XR <= 0` is
rejected because it lies outside the theorem hypothesis.

The acceptance authority is the predicate `maximum_absolute_error <= 1E-60`,
not the final digits of an error diagnostic, which may vary slightly across
Decimal/Python runtimes.

## Checks completed locally

```text
synthetic streaming/opaque/duplicate tests   PASS
committed normalized-fixture reconstruction  PASS
external raw-export integration               PASS
normalized replay across raw run 1 and run 2  PASS
H_scaling primary comparison                  PASS
two required mutations                        PASS
schema admission                              PASS
same-name/same-binder body mutation           REJECTED
LF-only normalized fixture writer             PASS
full Python suite                              PASS[237 passed, 1 skipped; 90.67%]
```

## Gate boundary

A separately operated ChatGPT MCP review inspected the source pins, raw digest
binding, decoded type projection, fixture, calculator binding, and mutation
closures. It confirmed the two closure patches: a same-name/same-binder
theorem-body mutation cannot reach calculation, and normalized fixture bytes
are LF-only. This is a `SEPARATE_ROLE_REVIEW[SHARED_TRUST_DOMAIN]`, not
independent proof authority.

That reviewer environment used a Python runtime without `pytest`; therefore
its full-suite replay is recorded as
`NOT_EXECUTED[REVIEWER_RUNTIME_MISMATCH]`, not as a test failure. It prevents
an `INDEPENDENT_REPLAY` claim, but does not invalidate the locally executed,
content-hash-bound vertical slice above.

Accordingly, this receipt closes only the first local source-derived vertical
slice. Broader M5 declaration coverage remains open, and this result does not
propose a release or a universal mathematical claim.
