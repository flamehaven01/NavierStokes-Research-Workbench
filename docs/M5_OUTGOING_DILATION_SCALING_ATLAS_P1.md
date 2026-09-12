# M5 P1 `OutgoingDilation` scaling atlas

Status: `P1_A_CLOSED[FAIL_CLOSED_DIGEST_ADMISSION]__P1_STATIC_PASS[LOCAL_REVIEWED_METADATA]__P1_SOURCE_ATLAS_HELD[LEDGER_NOT_INDEPENDENTLY_PINNED]`

This contract extends the M5 `H_scaling` vertical slice with a fixed ten-law
scaling family. It is not a general Lean parser, a proof verifier, or a new
Navier--Stokes result.

## Fixed mathematical surface

The reviewed-static family is drawn from `NavierStokes.OutgoingDilation` at
formal-source commit `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`:

```text
H_scaling                 1/2
powerH_scaling            1/2
energyDensity_scaling     0
canonicalKernel_scaling   -1
M_scaling                 1
I_scaling                 3/2
J_scaling                 3/2
S_scaling                 1
totalS_scaling            1
renormalizedI_scaling     3/2
```

The listed exponents are reviewed static metadata. They are **not** parsed
automatically from Lean theorem bodies. Exact `Fraction` arithmetic identifies
only bounded degree-zero candidates, including `J/(M*H)`, `I/(M*H)`, `M/S`,
and `XR * canonicalKernel` at the stated coordinate conditions.

The resulting P2 question is:

> For `J/(M*H)` at a common scaled radial coordinate, do support, zero-set, or
> cone and moment conditions prevent this degree-zero candidate from becoming
> a useful bound?

This does not establish an invariant, a cone estimate, a selected-source
witness, or any theorem about Navier--Stokes regularity or blowup.

## P1-A digest-authority closure

Candidate digests are useful review material but cannot authorize production
admission. `build_dilation_atlas()` has no caller-supplied digest parameter.
It first requires a committed ledger at
`fixtures/m5/outgoing_dilation_atlas_digests.json` and a physical SHA-256 of
that exact file pinned in `PINNED_ATLAS_DIGEST_LEDGER_SHA256`.

Until a reviewed ledger is pinned, production returns:

```text
HELD[LEDGER_NOT_INDEPENDENTLY_PINNED]
```

The regression surface includes a same-name, same-raw-hash type-projection
mutation followed by attacker recomputation of candidate digests. It cannot
open production admission. A pre-mutation ledger still detects the changed
semantic projection at the internal validator boundary.

## Remaining source gate

The previous four-law attempt produced a `289,992,704`-byte truncated NDJSON
artifact after exporter capacity exhaustion. It is a
`FAILED_EXECUTION_ARTIFACT`, not source evidence; the normalizer rejects it at
the incomplete JSON record.

The required next execution is on an adequate-memory clean environment:

1. export four selected declarations in one raw NDJSON file;
2. require exit `0`, empty stderr, a complete final record, all declarations,
   no normalization losses, and one raw SHA-256;
3. repeat for all ten declarations in one raw file;
4. review the ten normalized records and generate a candidate digest ledger;
5. commit the ledger with lowercase 64-hex `raw_sha256` and per-declaration
   semantic digests, then pin the ledger file's SHA-256 in code;
6. rerun production atlas admission and conduct a separate closure review.

Do not silently switch to multiple raw exports. That would require an explicit
contract amendment after two adequate-memory, resource-only failed attempts.

## Release boundary

This P1 checkpoint releases code and documentation for the closed digest
authority boundary and local static analysis only. It does not release a
source-bound ten-law atlas. The external raw export is not vendored.
