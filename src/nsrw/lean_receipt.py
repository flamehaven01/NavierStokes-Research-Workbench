"""Deterministic compiled-evidence receipts and atomic publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .strict_json import canonical_json_bytes, evidence_digests, load_strict_json

SCHEMA_ID = "flamehaven.nsrw-lean-compiled-evidence.v1"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def build_target_record(
    target: str,
    olean_path: Path,
    dependency_surface_path: Path,
    *,
    exit_code: int = 0,
    recorded_olean_path: Path | None = None,
) -> dict[str, Any]:
    return {
        "target": target,
        "exit_code": exit_code,
        "olean_path": (recorded_olean_path or olean_path).as_posix(),
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


def _atomic_write(destination: Path, payload: bytes) -> bytes:
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


def write_compiled_receipt(receipt: Mapping[str, Any], destination: Path) -> bytes:
    """Atomically publish a canonical receipt and return the published bytes."""

    return _atomic_write(destination, canonical_json_bytes(dict(receipt)) + b"\n")


def _module_artifact_suffix(target: str) -> str:
    module = target.removeprefix("+")
    if re.fullmatch(r"[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+", module) is None:
        raise ValueError(f"invalid Lean target: {target}")
    return module.replace(".", "/") + ".olean"


def discover_olean(lean_root: Path, target: str) -> Path:
    """Find the unique built module artifact without assuming a Lake layout prefix."""

    suffix = _module_artifact_suffix(target)
    candidates = [
        path
        for path in (lean_root / ".lake").rglob("*.olean")
        if path.as_posix().endswith(suffix)
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one observed .olean for {target}, found {len(candidates)}"
        )
    return candidates[0]


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
) -> tuple[subprocess.CompletedProcess[str], Path]:
    """Run the declared target build in the caller's clean execution context."""

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    assert_clean_checkout(lean_root)
    try:
        discover_olean(lean_root, target)
    except RuntimeError as exc:
        if "found 0" not in str(exc):
            raise
    else:
        raise RuntimeError("target artifact exists before live build; use an isolated clean build")
    process = subprocess.run(
        ["lake", "build", target],
        cwd=lean_root,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_seconds,
    )
    if process.returncode != 0:
        return process, Path()
    artifact = discover_olean(lean_root, target)
    return process, artifact


def _canonical_dependency_bytes(stdout: str, lean_root: Path) -> bytes:
    root = lean_root.resolve().as_posix().rstrip("/")
    lines = {
        line.strip().replace("\\", "/").replace(root, ".")
        for line in stdout.replace("\r\n", "\n").split("\n")
        if line.strip()
    }
    return ("\n".join(sorted(lines)) + "\n").encode("utf-8")


def _git_head(lean_root: Path) -> str:
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=lean_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("unable to read Lean checkout commit")
    return process.stdout.strip()


def _validate_build_request(
    request: Any, lean_root: Path
) -> tuple[str, str, list[dict[str, Any]]]:
    if not isinstance(request, dict) or request.get("schema_id") != "flamehaven.nsrw-lean-build-request.v1":
        raise ValueError("Lean build request is invalid")
    commit = str(request.get("formal_source_commit", ""))
    toolchain = str(request.get("toolchain", ""))
    targets = request.get("targets")
    if _git_head(lean_root).lower() != commit.lower():
        raise RuntimeError("Lean checkout commit does not match build request")
    pinned_toolchain = (lean_root / "lean-toolchain").read_text(encoding="utf-8").strip()
    if pinned_toolchain != toolchain:
        raise RuntimeError("Lean toolchain does not match build request")
    if not isinstance(targets, list) or not targets:
        raise ValueError("Lean build request has no targets")
    if not all(isinstance(item, dict) for item in targets):
        raise ValueError("Lean target request is malformed")
    target_names = [str(item.get("target", "")) for item in targets]
    if len(target_names) != len(set(target_names)):
        raise ValueError("Lean build request contains duplicate targets")
    return commit, toolchain, targets


def _safe_child(root: Path, relative: object) -> Path:
    path = Path(str(relative))
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Lean build request path escapes its declared root")
    candidate = (root / path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("Lean build request path escapes its declared root") from exc
    return candidate


def _build_requested_target(
    item: dict[str, Any],
    lean_root: Path,
    dependency_dir: Path,
    timeout_seconds: int,
) -> tuple[str, Mapping[str, Any]]:
    target = str(item.get("target", ""))
    _module_artifact_suffix(target)
    source = _safe_child(lean_root, item.get("module_source", ""))
    dependency_path = dependency_dir / str(item.get("dependency_output", ""))
    if not source.is_file() or dependency_path.parent.resolve() != dependency_dir.resolve():
        raise ValueError(f"Lean target request paths are invalid for {target}")
    process, artifact = verify_live_target(
        lean_root, target, timeout_seconds=timeout_seconds
    )
    if process.returncode != 0:
        raise RuntimeError(f"Lean target build failed for {target}: exit {process.returncode}")
    dependency_process = subprocess.run(
        ["lake", "env", "lean", "--deps", source.relative_to(lean_root).as_posix()],
        cwd=lean_root,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_seconds,
    )
    if dependency_process.returncode != 0:
        raise RuntimeError(f"Lean dependency extraction failed for {target}")
    _atomic_write(
        dependency_path,
        _canonical_dependency_bytes(dependency_process.stdout, lean_root),
    )
    record = build_target_record(
        target,
        artifact,
        dependency_path,
        exit_code=process.returncode,
        recorded_olean_path=artifact.relative_to(lean_root),
    )
    return target, record


def execute_build_request(
    request_path: Path,
    lean_root: Path,
    dependency_dir: Path,
    *,
    timeout_seconds: int = 900,
    working_directory_class: str = "HOSTED_CLEAN_CHECKOUT",
) -> dict[str, Any]:
    request, raw = load_strict_json(request_path)
    commit, toolchain, targets = _validate_build_request(request, lean_root)
    dependency_dir.mkdir(parents=True, exist_ok=True)
    records = dict(
        _build_requested_target(item, lean_root, dependency_dir, timeout_seconds)
        for item in targets
    )
    digests = evidence_digests(raw, request)
    return build_compiled_receipt(
        commit,
        toolchain,
        records,
        digests["input_bytes_sha256"],
        digests["canonical_manifest_sha256"],
        compiled_evidence_mode="LIVE_ARTIFACT",
        timeout_seconds=timeout_seconds,
        working_directory_class=working_directory_class,
    )


def build_live_manifest(
    template: Mapping[str, Any], receipt: Mapping[str, Any], receipt_path: Path
) -> dict[str, Any]:
    result = json.loads(json.dumps(template))
    result["compiled_evidence_mode"] = "LIVE_ARTIFACT"
    binding = result["source_binding"]
    binding.pop("migration_receipt_path", None)
    binding.pop("migration_receipt_sha256", None)
    binding["input_bytes_sha256"] = receipt["input_bytes_sha256"]
    binding["canonical_manifest_sha256"] = receipt["canonical_manifest_sha256"]
    receipt_hash = hashlib.sha256(canonical_json_bytes(dict(receipt)) + b"\n").hexdigest().upper()
    for target, record in binding["compiled_targets"].items():
        evidence = receipt["targets"][target]
        record["receipt_path"] = receipt_path.as_posix()
        record["receipt_sha256"] = receipt_hash
        record["olean_path"] = evidence["olean_path"]
        record["olean_sha256"] = evidence["olean_sha256"]
    return result


def build_provenance_envelope(receipt_bytes: bytes) -> dict[str, Any]:
    return {
        "schema_id": "flamehaven.nsrw-lean-execution-provenance.v1",
        "provider": "GITHUB_ACTIONS" if os.environ.get("GITHUB_ACTIONS") == "true" else "LOCAL",
        "workflow": os.environ.get("GITHUB_WORKFLOW", "LOCAL_UNHOSTED"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "UNHOSTED"),
        "attempt": int(os.environ.get("GITHUB_RUN_ATTEMPT", "1")),
        "platform": os.environ.get("RUNNER_OS", os.name),
        "canonical_receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest().upper(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--dependency-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-template", type=Path)
    parser.add_argument("--live-manifest-output", type=Path)
    parser.add_argument("--provenance-output", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    destinations = (args.output, args.live_manifest_output, args.provenance_output)
    for path in destinations:
        if path is not None:
            path.unlink(missing_ok=True)
    try:
        receipt = execute_build_request(
            args.request,
            args.source_root,
            args.dependency_dir,
            timeout_seconds=args.timeout_seconds,
        )
        receipt_bytes = write_compiled_receipt(receipt, args.output)
        if args.manifest_template and args.live_manifest_output:
            template, _ = load_strict_json(args.manifest_template)
            if not isinstance(template, dict):
                raise ValueError("live manifest template is not an object")
            live_manifest = build_live_manifest(template, receipt, args.output)
            _atomic_write(
                args.live_manifest_output,
                canonical_json_bytes(live_manifest) + b"\n",
            )
        if args.provenance_output:
            _atomic_write(
                args.provenance_output,
                canonical_json_bytes(build_provenance_envelope(receipt_bytes)) + b"\n",
            )
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        for path in destinations:
            if path is not None:
                path.unlink(missing_ok=True)
        print(f"lean receipt generation failed: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
