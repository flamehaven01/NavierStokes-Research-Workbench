from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import nsrw.lean_receipt as lean_receipt


def test_compiled_receipt_record_and_atomic_publication(tmp_path: Path) -> None:
    olean = tmp_path / "target.olean"
    deps = tmp_path / "deps.txt"
    olean.write_bytes(b"olean")
    deps.write_text("A\nB\n", encoding="utf-8")
    record = lean_receipt.build_target_record("+Example.Target", olean, deps)
    receipt = lean_receipt.build_compiled_receipt(
        "a" * 40,
        "leanprover/lean4:v4.34.0-rc2",
        {"+Example.Target": record},
        "b" * 64,
        "c" * 64,
    )
    destination = tmp_path / "nested" / "receipt.json"
    payload = lean_receipt.write_compiled_receipt(receipt, destination)
    assert destination.read_bytes() == payload
    assert destination.read_bytes().endswith(b"\n")
    assert not list(destination.parent.glob(".*.receipt.json.*"))


def test_live_target_build_uses_declared_root_and_timeout(monkeypatch, tmp_path: Path) -> None:
    observed: dict[str, object] = {}

    def fake_run(*args: object, **kwargs: object) -> object:
        observed["args"] = args
        observed.update(kwargs)
        if args[0][0] == "git":
            return SimpleNamespace(returncode=0, stdout="")
        artifact = tmp_path / ".lake" / "build" / "lib" / "lean" / "Example" / "Target.olean"
        artifact.parent.mkdir(parents=True)
        artifact.write_bytes(b"fresh")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(lean_receipt.subprocess, "run", fake_run)
    result = lean_receipt.verify_live_target(tmp_path, "+Example.Target", timeout_seconds=12)
    assert result.returncode == 0
    assert observed["cwd"] == tmp_path
    assert observed["timeout"] == 12
    assert observed["args"] == (["lake", "build", "+Example.Target"],)
