"""Read-only checks of pinned Lean replay archives with the P1 replay layout."""

from __future__ import annotations

import hashlib
import io
import re
import zipfile
from dataclasses import dataclass, field

from nsrw.strict_json import parse_strict_json_bytes


@dataclass(frozen=True)
class ReplayPin:
    archive_sha256: str
    members: int
    execution_commit: str
    source_commit: str
    toolchain: str
    run_status: str
    declarations: dict[str, tuple[str, ...]]
    critical_signature_sha256: dict[str, str] = field(default_factory=dict)


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def inspect_declarations(text: str, names: tuple[str, ...], axioms: dict) -> dict:
    """Match each declaration and its exact recorded axiom list to the replay metadata."""
    result = {}
    for name in names:
        escaped = re.escape(name)
        signatures = re.findall(rf"^{escaped}(?=\s|\()([^\n]*(?:\n[ \t]+[^\n]*)*)", text, re.M)
        rows = re.findall(rf"^'{escaped}' depends on axioms: \[([^\n\]]*)\]$", text, re.M)
        _require(len(signatures) == 1 and len(rows) == 1, f"missing or duplicate declaration: {name}")
        observed = sorted(item.strip() for item in rows[0].split(",") if item.strip())
        _require(
            len(observed) == len(set(observed))
            and set(observed) <= {"propext", "Classical.choice", "Quot.sound"}
            and observed == axioms.get(name),
            f"unexpected axioms: {name}",
        )
        result[name] = {"signature_sha256": _sha((name + signatures[0]).encode()), "axioms": observed}
    return result


def check_lean_archive(raw: bytes, pin: ReplayPin) -> dict:
    _require(_sha(raw) == pin.archive_sha256, "archive SHA-256 differs from the receipt")
    with zipfile.ZipFile(io.BytesIO(raw)) as bundle:
        names = bundle.namelist()
        _require(len(names) == len(set(names)) == pin.members, "archive inventory count mismatch")
        _require(bundle.testzip() is None, "archive CRC mismatch")
        metadata = parse_strict_json_bytes(bundle.read("replay-metadata.json"))
        identity = metadata["pre_identity"]
        source = metadata["pre_source_identity"]
        _require(
            identity == metadata["post_identity"] and source == metadata["post_source_identity"]
            and identity["commit"] == metadata["expected_nsrw_commit"] == pin.execution_commit
            and identity["tracked_clean"] is True and source["commit"] == pin.source_commit
            and source["toolchain_file"] == pin.toolchain,
            "replay identity mismatch",
        )
        _require(
            metadata["check_status"] == pin.run_status
            and metadata["claim_authority"] == "NONE" and metadata["claim_status"] == "UNVERIFIED",
            "replay status mismatch",
        )
        expected = {"replay-metadata.json"}
        for folder, entries in (
            ("inputs", metadata["inputs"]), ("artifacts", metadata["fresh_artifacts"])
        ):
            for name, digest in entries.items():
                member = f"{folder}/{name}"
                expected.add(member)
                _require(_sha(bundle.read(member)) == digest, f"member digest mismatch: {member}")
        declarations = {}
        stages = metadata["stages"]
        _require(pin.declarations.keys() <= stages.keys(), "declaration stage missing")
        for stage, info in stages.items():
            _require(type(info["exit"]) is int and info["exit"] == 0, f"failed compile: {stage}")
            for stream in ("stdout", "stderr"):
                member = f"{stage}.{stream}.log"
                expected.add(member)
                data = bundle.read(member)
                _require(
                    len(data) == info[f"{stream}_bytes"] and _sha(data) == info[f"{stream}_sha256"]
                    and b"sorryAx" not in data and (stream == "stdout" or not data),
                    f"unexpected recorded log: {member}",
                )
                if stream == "stdout" and stage in pin.declarations:
                    declarations.update(inspect_declarations(
                        data.decode("utf-8"), pin.declarations[stage], metadata["axiom_surfaces"]
                    ))
        _require(set(names) == expected, "archive member inventory mismatch")
        _require(declarations.keys() == metadata["axiom_surfaces"].keys(), "axiom inventory mismatch")
        for name, expected_sha in pin.critical_signature_sha256.items():
            _require(
                declarations.get(name, {}).get("signature_sha256") == expected_sha,
                f"critical declaration signature differs: {name}",
            )
        return {
            "archive_members": len(names),
            "compiled_stages": len(stages),
            "execution_commit": pin.execution_commit,
            "source_commit": pin.source_commit,
            "toolchain": pin.toolchain,
            "declarations": declarations,
            "kernel_reexecuted": False,
        }
