from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import nsrw.lean_receipt as lean_receipt


def _clear_hosted_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "GITHUB_ACTIONS",
        "GITHUB_WORKFLOW",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_ATTEMPT",
        "RUNNER_OS",
    ):
        monkeypatch.delenv(name, raising=False)


def test_compiled_receipt_record_and_atomic_publication(tmp_path: Path) -> None:
    olean = tmp_path / "target.olean"
    deps = tmp_path / "deps.txt"
    olean.write_bytes(b"olean")
    deps.write_text("A\nB\n", encoding="utf-8")
    record = lean_receipt.build_target_record(
        "+Example.Target",
        olean,
        deps,
        recorded_olean_path=Path(".lake/build/lib/lean/Example/Target.olean"),
        recorded_dependency_path=Path("outputs/deps/target.txt"),
    )
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
    result, artifact = lean_receipt.verify_live_target(
        tmp_path, "+Example.Target", timeout_seconds=12
    )
    assert result.returncode == 0
    assert artifact.name == "Target.olean"
    assert observed["cwd"] == tmp_path
    assert observed["timeout"] == 12
    assert observed["args"] == (["lake", "build", "+Example.Target"],)


def test_execute_build_request_discovers_artifact_and_canonicalizes_deps(
    monkeypatch, tmp_path: Path
) -> None:
    _clear_hosted_runtime(monkeypatch)
    source_root = tmp_path / "lean"
    source = source_root / "Example" / "Target.lean"
    source.parent.mkdir(parents=True)
    source.write_text("theorem x : True := by trivial\n", encoding="utf-8")
    (source_root / "lean-toolchain").write_text("leanprover/lean4:v4.34.0-rc2\n")
    request = tmp_path / "request.json"
    request.write_text(
        json.dumps(
            {
                "schema_id": "flamehaven.nsrw-lean-build-request.v1",
                "formal_source_commit": "a" * 40,
                "toolchain": "leanprover/lean4:v4.34.0-rc2",
                "targets": [
                    {
                        "target": "+Example.Target",
                        "module_source": "Example/Target.lean",
                        "dependency_output": "target-deps.txt",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    def fake_run(args, **kwargs):
        if args[:2] == ["git", "rev-parse"]:
            return SimpleNamespace(returncode=0, stdout="a" * 40 + "\n", stderr="")
        if args[:2] == ["git", "status"]:
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        if args[:2] == ["lake", "build"]:
            artifact = source_root / ".lake" / "custom" / "Example" / "Target.olean"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"compiled")
            return SimpleNamespace(returncode=0, stdout="built", stderr="")
        if args[:4] == ["lake", "env", "lean", "--deps"]:
            return SimpleNamespace(
                returncode=0,
                stdout=f"{source_root.as_posix()}/B.olean\r\n{source_root.as_posix()}/A.olean\r\n",
                stderr="",
            )
        raise AssertionError(args)

    monkeypatch.setattr(lean_receipt.subprocess, "run", fake_run)
    monkeypatch.chdir(tmp_path)
    receipt = lean_receipt.execute_build_request(
        request,
        Path("lean"),
        Path("deps"),
        evidence_root=Path("."),
        timeout_seconds=20,
    )
    record = receipt["targets"]["+Example.Target"]
    assert record["olean_path"] == ".lake/custom/Example/Target.olean"
    assert (tmp_path / "deps" / "target-deps.txt").read_text(encoding="utf-8") == (
        "./A.olean\n./B.olean\n"
    )
    assert receipt["compiled_evidence_mode"] == "LIVE_ARTIFACT"
    assert receipt["build_cleanliness_class"] == "ISOLATED_CLEAN_BUILD"


def test_hosted_authority_is_runtime_derived(monkeypatch) -> None:
    hosted = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_WORKFLOW": "CI",
        "GITHUB_RUN_ID": "123",
        "GITHUB_RUN_ATTEMPT": "1",
        "RUNNER_OS": "Linux",
    }
    for name in hosted:
        monkeypatch.delenv(name, raising=False)
    assert lean_receipt._working_directory_class() == "ISOLATED_CLEAN_BUILD"
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    assert lean_receipt._working_directory_class() == "ISOLATED_CLEAN_BUILD"
    for name, value in hosted.items():
        monkeypatch.setenv(name, value)
    assert lean_receipt._working_directory_class() == "HOSTED_CLEAN_CHECKOUT"
    first = lean_receipt.build_compiled_receipt(
        "a" * 40, "toolchain", {}, "b" * 64, "c" * 64
    )
    assert first["build_cleanliness_class"] == "HOSTED_CLEAN_CHECKOUT"
    monkeypatch.setenv("GITHUB_RUN_ID", "456")
    second = lean_receipt.build_compiled_receipt(
        "a" * 40, "toolchain", {}, "b" * 64, "c" * 64
    )
    assert lean_receipt.canonical_json_bytes(first) == lean_receipt.canonical_json_bytes(
        second
    )


def test_provenance_rejects_authority_and_hash_contradictions(monkeypatch) -> None:
    for name in (
        "GITHUB_ACTIONS",
        "GITHUB_WORKFLOW",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_ATTEMPT",
        "RUNNER_OS",
    ):
        monkeypatch.delenv(name, raising=False)
    receipt = lean_receipt.build_compiled_receipt(
        "a" * 40,
        "toolchain",
        {
            "+Example.Target": {
                "target": "+Example.Target",
                "exit_code": 0,
                "olean_path": ".lake/Example/Target.olean",
                "olean_sha256": "b" * 64,
                "dependency_surface_path": "outputs/deps.txt",
                "dependency_surface_sha256": "c" * 64,
            }
        },
        "d" * 64,
        "e" * 64,
    )
    receipt["build_cleanliness_class"] = "HOSTED_CLEAN_CHECKOUT"
    receipt["command_spec"]["working_directory_class"] = "HOSTED_CLEAN_CHECKOUT"
    provenance = lean_receipt.build_provenance_envelope(
        lean_receipt.canonical_json_bytes(receipt) + b"\n"
    )
    with pytest.raises(ValueError, match="authority contradict"):
        lean_receipt.validate_provenance_consistency(receipt, provenance)
    receipt["build_cleanliness_class"] = "ISOLATED_CLEAN_BUILD"
    receipt["command_spec"]["working_directory_class"] = "ISOLATED_CLEAN_BUILD"
    provenance["canonical_receipt_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="does not bind"):
        lean_receipt.validate_provenance_consistency(receipt, provenance)


def test_live_manifest_and_provenance_bind_receipt(monkeypatch, tmp_path: Path) -> None:
    template = {
        "compiled_evidence_mode": "RECEIPT_REPLAY",
        "source_binding": {
            "input_bytes_sha256": "0" * 64,
            "canonical_manifest_sha256": "0" * 64,
            "compiled_targets": {
                "+Example.Target": {
                    "receipt_path": "old.json",
                    "receipt_sha256": "0" * 64,
                    "olean_path": "old.olean",
                    "olean_sha256": "0" * 64,
                }
            },
        },
    }
    receipt = lean_receipt.build_compiled_receipt(
        "a" * 40,
        "toolchain",
        {
            "+Example.Target": {
                "target": "+Example.Target",
                "exit_code": 0,
                "olean_path": ".lake/observed/Example/Target.olean",
                "olean_sha256": "b" * 64,
                "dependency_surface_path": "deps/target.txt",
                "dependency_surface_sha256": "c" * 64,
            }
        },
        "d" * 64,
        "e" * 64,
    )
    live = lean_receipt.build_live_manifest(template, receipt, Path("receipt.json"))
    assert live["compiled_evidence_mode"] == "LIVE_ARTIFACT"
    assert live["source_binding"]["compiled_targets"]["+Example.Target"]["olean_path"] == (
        ".lake/observed/Example/Target.olean"
    )
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_WORKFLOW", "CI")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "2")
    monkeypatch.setenv("RUNNER_OS", "Linux")
    envelope = lean_receipt.build_provenance_envelope(b"receipt\n")
    assert envelope["provider"] == "GITHUB_ACTIONS"
    assert envelope["attempt"] == 2
    assert len(envelope["canonical_receipt_sha256"]) == 64


def test_discovery_and_cli_fail_closed(monkeypatch, tmp_path: Path) -> None:
    try:
        lean_receipt.discover_olean(tmp_path, "+Example.Target")
    except RuntimeError as exc:
        assert "found 0" in str(exc)
    else:
        raise AssertionError("missing artifact must fail")
    stale = tmp_path / "receipt.json"
    stale.write_text("stale", encoding="utf-8")
    monkeypatch.setattr(
        lean_receipt,
        "execute_build_request",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "nsrw-lean-receipt",
            "--request",
            str(tmp_path / "request.json"),
            "--source-root",
            str(tmp_path),
            "--dependency-dir",
            str(tmp_path / "deps"),
            "--evidence-root",
            str(tmp_path),
            "--output",
            str(stale),
        ],
    )
    assert lean_receipt.main() == 2
    assert not stale.exists()


def test_build_request_paths_and_target_names_fail_closed(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="escapes"):
        lean_receipt._safe_child(tmp_path, "../outside.lean")
    with pytest.raises(ValueError, match="invalid Lean target"):
        lean_receipt._module_artifact_suffix("+../Outside")


def test_cli_removes_partial_outputs_after_late_failure(monkeypatch, tmp_path: Path) -> None:
    receipt = lean_receipt.build_compiled_receipt(
        "a" * 40,
        "toolchain",
        {},
        "b" * 64,
        "c" * 64,
    )
    template = tmp_path / "template.json"
    template.write_text("[]", encoding="utf-8")
    output = tmp_path / "receipt.json"
    live = tmp_path / "live.json"
    monkeypatch.setattr(lean_receipt, "execute_build_request", lambda *args, **kwargs: receipt)
    monkeypatch.setattr(
        "sys.argv",
        [
            "nsrw-lean-receipt",
            "--request",
            str(tmp_path / "request.json"),
            "--source-root",
            str(tmp_path),
            "--dependency-dir",
            str(tmp_path / "deps"),
            "--evidence-root",
            str(tmp_path),
            "--output",
            str(output),
            "--manifest-template",
            str(template),
            "--live-manifest-output",
            str(live),
        ],
    )
    assert lean_receipt.main() == 2
    assert not output.exists()
    assert not live.exists()
