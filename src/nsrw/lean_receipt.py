"""Deterministic compiled-evidence receipts and atomic publication."""

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .strict_json import canonical_json_bytes

SCHEMA_ID = "flamehaven.nsrw-lean-compiled-evidence.v1"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def build_target_record(
    target: str,
    olean_path: Path,
    dependency_surface_path: Path,
    *,
    exit_code: int = 0,
) -> dict[str, Any]:
    return {
        "target": target,
        "exit_code": exit_code,
        "olean_path": olean_path.as_posix(),
        "olean_sha256": _sha256(olean_path),
        "dependency_surface_sha256": _sha256(dependency_surface_path),
    }


def build_compiled_receipt(
    formal_source_commit: str,
    toolchain: str,
    targets: Mapping[str, Mapping[str, Any]],
    input_bytes_sha256: str,
    canonical_manifest_sha256: str,
    *,
    compiled_evidence_mode: str = "LIVE_ARTIFACT",
    command_spec_id: str = "lake-scoped-target-build-v1",
    timeout_seconds: int = 900,
    working_directory_class: str = "ISOLATED_CLEAN_BUILD",
) -> dict[str, Any]:
    return {
        "schema_id": SCHEMA_ID,
        "formal_source_commit": formal_source_commit,
        "toolchain": toolchain,
        "compiled_evidence_mode": compiled_evidence_mode,
        "command_spec_id": command_spec_id,
        "command_spec": {
            "argv": ["lake", "build", "<declared-target>"],
            "timeout_seconds": timeout_seconds,
            "working_directory_class": working_directory_class,
        },
        "build_cleanliness_class": working_directory_class,
        "input_bytes_sha256": input_bytes_sha256,
        "canonical_manifest_sha256": canonical_manifest_sha256,
        "dependency_surface_profile": "NSRW-DEPS-LF-SORTED-V1",
        "canonicalization_profile": "NSRW-CANONICAL-JSON-1",
        "targets": {key: dict(targets[key]) for key in sorted(targets)},
    }


def write_compiled_receipt(receipt: Mapping[str, Any], destination: Path) -> bytes:
    """Atomically publish a canonical receipt and return the published bytes."""

    payload = canonical_json_bytes(dict(receipt)) + b"\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return payload


def expected_olean_path(lean_root: Path, target: str) -> Path:
    return lean_root / ".lake" / "build" / "lib" / "lean" / (
        target.removeprefix("+").replace(".", "/") + ".olean"
    )


def assert_clean_checkout(lean_root: Path) -> None:
    process = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=lean_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("unable to establish clean Lean checkout")
    if process.stdout.strip():
        raise RuntimeError("Lean checkout has tracked changes")


def verify_live_target(
    lean_root: Path,
    target: str,
    *,
    timeout_seconds: int = 900,
) -> subprocess.CompletedProcess[str]:
    """Run the declared target build in the caller's clean execution context."""

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    assert_clean_checkout(lean_root)
    artifact = expected_olean_path(lean_root, target)
    if artifact.exists():
        raise RuntimeError("target artifact exists before live build; use an isolated clean build")
    process = subprocess.run(
        ["lake", "build", target],
        cwd=lean_root,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_seconds,
    )
    if process.returncode == 0 and not artifact.is_file():
        raise RuntimeError("successful live build did not produce the expected .olean")
    return process
