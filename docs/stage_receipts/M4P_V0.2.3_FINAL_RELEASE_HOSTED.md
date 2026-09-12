# M4-P v0.2.3 final release hosted evidence

Date: `2026-09-12`

Tagged commit: `1120b77c5533f012a31fadd3a9185e68d939f3e0`

Tag: `v0.2.3`

Workflow run: [GitHub Actions 34666375341](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/runs/34666375341)

Check status: `PASS[FINAL_RELEASE_HOSTED_LIVE_SCOPED]`

Claim status: `UNVERIFIED[NAVIER_STOKES_THEOREM]`

## Observed execution

```text
Python matrix                  PASS[4/4]
contract/replay validation     PASS
pinned Lean targets            PASS[3/3]
compiled evidence mode         LIVE_ARTIFACT
build cleanliness              HOSTED_CLEAN_CHECKOUT
M4 live receipt                PASS[COMPLETED]
live mutations rejected        PASS[14/14]
artifact upload                PASS
```

The run checked out formal source commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, installed
`leanprover/lean4:v4.34.0-rc2`, and built the three declared targets in the
same clean hosted job that generated and consumed the LIVE evidence. The
provenance envelope records provider `GITHUB_ACTIONS`, workflow `CI`, run
`34666375341`, attempt `1`, and platform `Linux`.

## Downloaded artifact identities

GitHub artifact `scoped-lean-target-evidence`:

```text
artifact id                    10288683221
artifact archive SHA-256       FD4C2D1B14851DAFCD9BEF7C365DB8F6F679757569A7158E14A97CCDBC8E7AAC
canonical compiled receipt     CD95D66A9396A067168F2748A68A4C0D6FE14DFB2DA9F0B08B1604E0AA4DB391
execution provenance           90FDFC8ACD04C1597EF4384C2DAC4F99048BAB4C9BFA858F7078A7CE9CBD1212
live v3 manifest               230080690DEF05FD6D07926B1A276567CC5292DAA63A86515FFD73B2185958BD
live M4 receipt                F42B15ACC3BC6130B0B23DD5CD925FF6EB10231CBE8741752E33C4CDE717E84D
```

Target-specific compiled and dependency identities:

| Target | `.olean` SHA-256 | Dependency-file SHA-256 |
|---|---|---|
| `+NavierStokes.NominalConeAssembly` | `1E7049B2B8A6BE3B802EE42C856A06DEE40F4331E14E161A495A8A9B6D515A3D` | `45B3488E57FA6DC2D167AA53491AC3063A1326E180736CBC4A2795DBF9FCE630` |
| `+NavierStokes.OutgoingCone` | `DA5C2E0CC8C2932346945022706F01379314A8134504BD8A766069C7C03E67A4` | `836DD12D1C908FE1D55AC6B92B5E930B0D44AE98C4C95C0316B571CD72DE493A` |
| `+NavierStokes.OutgoingDilation` | `E47FA3AFCA76ED83021C1F030E4FE3ACE43586CA03341EA4B2CAF42A913F344D` | `B5FF4C9977E29012869D2B2FB84B8EF224B4D2D56F23B3CF10D6324AC9B48BA7` |

After download, the compiled receipt, provenance envelope, and live manifest
were independently admitted through their declared JSON Schemas. Each uploaded
dependency file was re-hashed and matched its receipt record. The provenance
receipt digest matched the downloaded canonical receipt bytes. The canonical
compiled receipt and mathematical-control artifacts were byte-identical to the
preceding release-candidate run; only run-specific provenance changed.

## Boundary

This is direct hosted evidence for the tagged software, source-binding, and
three Lean target surfaces. It does not establish the manuscript's correctness,
paper--Lean semantic equivalence, a computable selected-source witness, or a
solution to the Navier--Stokes Millennium problem. M4-P remains parametric;
M4-S remains `HELD[NONCOMPUTABLE_SOURCE_INSTANCE]`.
