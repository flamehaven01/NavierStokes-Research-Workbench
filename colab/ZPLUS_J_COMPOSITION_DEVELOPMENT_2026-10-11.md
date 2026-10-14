# Z+J source composition — development record, 2026-10-11

check_status: PASS[LOCAL_PROOF_COMPILE:P2_ZPLUS_J_COMPOSITION]
claim_authority: NONE
claim_status: UNVERIFIED
independent_attestation: false

This is a development execution record, not a commit-bound receipt. The existing
Z04-core and conditional angular proof bytes were not modified for composition.

## Exact compiled surface

`formal/p2/P2_ZPLUS_J_SourceComposition.lean` adds three named propositions:

1. `NSRW.P2.localAngularMoment_eq_profileJ`: for `1 <= r`, the local angular
   moment equals source `F.J eta (exp(pulseStart) * r)`.
2. `NSRW.P2.profileJ_pos_of_firstRepair_mass_zero`: an interior first-window
   source mass zero together with positive actual second coefficient implies
   source J positivity at that same point.
3. `NSRW.P2.profileMJ_firstRepair_zero_small_positive`: for every fixed source
   `Profile F`, there exists a Profile-dependent positive epsilon such that each
   `0 < eta < epsilon` has one `r` strictly in the first repair window with
   `F.M eta X = 0` and `0 < F.J eta X`, where `X = exp(pulseStart) * r`.

The final proof uses one C04 epsilon and the same F/eta/r/X throughout. It does
not combine independently chosen existential witnesses.

Not claimed: a uniform or numerical epsilon, root finder, first/unique zero,
simple zero, Q pole/limit, paper equivalence, upstream theorem verification,
literature novelty, practical solver or a Navier–Stokes Millennium solution.

## Frozen execution inputs

| Input | Executor SHA-256 |
| --- | --- |
| composition proof | `c3444fbe43c633ef1a0be0987cb42ab8264d4a92da81cf961ee647409c16bd89` |
| development driver | `64eb25d0cc5d2c19463746d1843facf8620ee65c4e853b3eec8cb6b1d09950d9` |
| frozen transport notebook | `48e06e828956e8e907d81c16d1cd7f527b4d9ba9a0986ed6dd2665b6fe42ca11` |

Pinned source: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
Lean: `4.34.0-rc2`. Manifest blob:
`f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`.
Committed dependency base: `10d5a1f517b8665137f2354746d70752f8ef67fd`.
The source cache was reused, not a full clean library rebuild.

## One new execution

Run: `nsrw-zplus-j-composition-development-20261011T144300398298Z`.
Finished UTC: `2026-10-11T14:45:28.775605+00:00`.

```text
source / +NavierStokes.OutgoingProfile
  -> fresh F1 -> L2 -> L3 -> D -> C01 -> C02 -> C03 -> C04
  -> fresh Z01 -> Z02 -> Z03 -> Z04-core -> conditional Z+J
  -> fresh source composition
```

All 15 stages exited 0 with empty stderr. Fourteen fresh external `.olean`
artifacts were generated. The three final named axiom surfaces each contained
exactly `propext`, `Classical.choice`, `Quot.sound`; `sorryAx` was absent.
Source identity, dependency-base observation and source target artifact were
unchanged pre/post. These observations do not independently audit imported
mathematical semantics.

Archive: `nsrw-zplus-j-composition-development-20261011T144300398298Z-evidence.zip`.
Size: `807617` bytes.
SHA-256: `0268a15966db153997bcad83eec2b79581f2bfa973bd1b0bda90ddb8d7007a72`.
The approved private Drive copy was fetched to
`colab/evidence/2026-10-11/nsrw-zplus-j-composition-development-20261011T144300398298Z/`
on D:. Size/SHA match. The bounded local ZIP check verified CRCs, member safety,
60 recorded member digests, 15 stages, 14 fresh artifacts and three final named
axiom surfaces against raw output. Source/base/target pre/post observations match.
`PASS[LOCAL_ARCHIVE_CROSSCHECK:ZPLUS_DEVELOPMENT]` is a preservation check in the
same trust domain, not an independent attestation or claim admission.

## Local controls and next gate

Activated `D:/Sanctum/venv/Scripts/Activate.ps1`; 24 focused synthetic tests and
Ruff passed. These tests validate driver controls, not Lean compilation.

Next: preserve this archive, freeze exact Git identities, use a fresh clean
checkout for one full-DAG replay, then review Z-core and Z+J as separate named
claims. An execution record continues to report NONE/UNVERIFIED; only scoped
receipt review may admit claims. No numerical or derivative strengthening is
required to close this phase.
