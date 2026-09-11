from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

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
    assert receipt["stage_status"] == "HELD_LEAN_BUILD_AND_SOURCE_INSTANCE"
    assert receipt["lean_build"]["check_status"] == "ERROR"
    assert receipt["lean_build"]["build_attempted"] is False
    assert receipt["theorem_dependency_surface"]["check_status"] == "PASS"
    assert receipt["source_pressure_tail"]["check_status"] == "PASS"


@pytest.mark.parametrize(("exit_code", "expected"), [(0, "PASS"), (7, "FAIL")])
def test_m3_build_status_requires_actual_subprocess_exit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    exit_code: int,
    expected: str,
) -> None:
    root = tmp_path / "NavierStokesAndEuler"
    root.mkdir()
    monkeypatch.setattr(
        "nsrw.m3_evidence_cli.shutil.which", lambda name: f"/tools/{name}"
    )
    calls: list[tuple[object, object]] = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs.get("cwd")))
        return SimpleNamespace(returncode=exit_code, stdout="out", stderr="err")

    monkeypatch.setattr("nsrw.m3_evidence_cli.subprocess.run", fake_run)
    receipt = execute(root, timeout_seconds=17)
    assert receipt["lean_build"]["check_status"] == expected
    assert receipt["lean_build"]["build_attempted"] is True
    assert receipt["lean_build"]["exit_code"] == exit_code
    assert calls == [(["lake", "build", "+NavierStokes.OutgoingDilation"], root)]
    expected_stage = (
        "CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY"
        if exit_code == 0
        else "HELD_LEAN_BUILD_AND_SOURCE_INSTANCE"
    )
    assert receipt["stage_status"] == expected_stage
