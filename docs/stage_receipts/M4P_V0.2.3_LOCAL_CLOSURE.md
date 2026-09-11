# M4-P v0.2.3 local closure receipt

Date: `2026-09-11`

Base implementation commit: `447e86347a150bfa98e3bc5c6a61bc07c1c6223c`

Task status: `COMPLETED[LOCAL_AUDIT_PATCH]`

Release status: `HELD[EXACT_COMMIT_HOSTED_LIVE_PENDING]`

Claim status: `UNVERIFIED[NAVIER_STOKES_THEOREM]`

## Closed findings

| Finding | Local result |
|---|---|
| M3 process status disagreed with receipt | `PASS[EXIT_0_1_2_BOUND]` |
| Hosted class was caller-described | `PASS[RUNTIME_DERIVED]` |
| Schema and runtime admission diverged | `PASS[SCHEMA_FIRST_ADMISSION]` |
| Compiled receipt fields were partly unchecked | `PASS[LIVE_V2_SCHEMA]` |
| Support/Cone parent semantics were implicit | `PASS[EXPLICIT_POLICY]` |
| Mutation inputs existed only as Python transforms | `PASS[14_HASHED_GOLDEN_JSON]` |
| Exact rational limit was aggregate | `PASS[256_DIGITS_PER_COMPONENT]` |
| LIVE dependency bytes were producer-bound only | `PASS[INDEPENDENT_REHASH]` |
| README mixed present and future tense | `PASS[SEPARATED]` |

## Local verification

```text
pytest                         PASS[224]
coverage                       PASS[92.05% >= 90%]
ruff                           PASS
compileall                     PASS
git diff --check               PASS
v3 deterministic replay       PASS[BYTE_IDENTICAL]
v3 applicable mutations       PASS[13/13]
v3 live-only mutation          NOT_APPLICABLE[LOCAL_REPLAY]
```

The two deterministic outputs share SHA-256:

`027C241911F8957EF709CA0241216CE30E1DBB657CF9FACFA9648206E73842DF`

## Code-quality heuristic scan

The configured rule-based heuristic scan reports:

```text
overall status                 clean
weighted deficit score         0.529417111659642
Python files analyzed          49
critical findings              0
findings in changed runtime     0
ML scoring                     disabled
```

The six remaining heuristic findings are pre-existing: two high, two medium,
and two low findings across an external-experiment module and tests. They are
not represented as zero findings, and no ML cleanliness claim is made.

## Key local identities

```text
v3 pilot
  EF5253DF328C683535CEC09533E8D78B083F91A0C5BDDA94BEE42BD67071F2C1

14-case golden mutation corpus index
  DB5AE33E7B12D06EEFF20F19018D56EAE4EE08EFB133BC634873CC5EA40FB58F

v3 obligation schema
  A65E3497B9B67429C0DD520DBE63DFCF6929707B183C4C9451B4CCF27C381798

LIVE compiled-evidence v2 schema
  2FE8E551CCE3AECE36CE265AD92DC916FD9E4F07B47105FEAA2982F2AA2DD0CD
```

## Remaining release gate

Local replay cannot grant hosted same-run authority. The exact committed
v0.2.3 candidate must still pass GitHub Actions and its downloaded artifact
must confirm the source revision, toolchain, target records, `.olean` hashes,
dependency hashes, provenance binding, and 14 applicable live mutations.

This receipt does not establish a source numerical witness, paper--Lean
semantic equivalence, a new analytic theorem, or a Navier--Stokes solution.
