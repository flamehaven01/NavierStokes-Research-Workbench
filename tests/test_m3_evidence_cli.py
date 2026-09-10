from __future__ import annotations

from pathlib import Path

import pytest

from nsrw.m3_evidence_cli import execute


def test_m3_evidence_execution_preserves_hold_and_records_both_surfaces(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "NavierStokesAndEuler"
    declarations = {
        "NavierStokes/ProfileHistories.lean": "def average := 0\ntheorem radialPartial_pressure : True := by trivial\n",
        "NavierStokes/SlowDivergence.lean": "def radialFlux := 0\n",
        "NavierStokes/NominalProfile.lean": "theorem pressure_canonical : True := by trivial\n",
        "NavierStokes/ProblemStatement.lean": "def candidateStatement := True\n",
        "NavierStokes/ActualCandidateAssembly.lean": "theorem selected_candidate : True := by trivial\n",
    }
    for relative, text in declarations.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    monkeypatch.setattr("nsrw.m3_evidence_cli.shutil.which", lambda name: None)
    receipt = execute(root)
    assert receipt["stage_status"] == "HELD_LEAN_TOOLCHAIN_AND_SOURCE_INSTANCE"
    assert receipt["lean_build"]["check_status"] == "ERROR"
    assert receipt["theorem_dependency_surface"]["check_status"] == "PASS"
    assert receipt["source_pressure_tail"]["check_status"] == "PASS"
