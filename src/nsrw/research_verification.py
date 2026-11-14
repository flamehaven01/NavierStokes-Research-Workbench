"""Run explicit research checks against named, byte-bound inputs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"
    ENV_BLOCKED = "ENV_BLOCKED"
    NOT_RUN = "NOT_RUN"
    ERROR = "ERROR"


@dataclass(frozen=True)
class Finding:
    status: Status
    details: dict[str, Any]


@dataclass(frozen=True)
class Verification:
    check_id: str
    revision: str
    target: str
    method: str
    domain: str
    evidence_class: str
    inputs: tuple[str, ...]
    evaluate: Callable[[Mapping[str, bytes]], Finding]


def run_verification(check: Verification, evidence: Mapping[str, bytes]) -> dict[str, Any]:
    """Pin supplied bytes before invoking an evaluator; never hash mutated inputs."""
    try:
        # Match bytes exactly: str and writable buffers must not be coerced.
        if not isinstance(evidence, Mapping):
            raise TypeError("evidence must be a mapping")
        if any(type(name) is not str or type(raw) is not bytes for name, raw in evidence.items()):
            raise TypeError("evidence names must be str and values must be bytes")
        snapshot = dict(evidence)
        input_digests = {
            name: {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
            for name, raw in sorted(snapshot.items())
        }
    except (TypeError, ValueError) as exc:
        return {
            "format": "nsrw-research-verification-v1",
            "check_id": check.check_id,
            "revision": check.revision,
            "target": check.target,
            "domain": check.domain,
            "method": check.method,
            "evidence_class": check.evidence_class,
            "status": Status.ERROR.value,
            "inputs": {},
            "details": {"reason": f"invalid input evidence: {exc}"},
            "claim_authority": "NONE",
            "claim_status": "UNVERIFIED",
        }

    missing = sorted(set(check.inputs) - snapshot.keys())
    unexpected = sorted(snapshot.keys() - set(check.inputs))
    if unexpected:
        finding = Finding(Status.FAIL, {"unexpected_inputs": unexpected})
    elif missing:
        finding = Finding(Status.NOT_RUN, {"missing_inputs": missing})
    else:
        try:
            # Prevent accidental/eager modification of the evidence mapping.
            # The raw values are exact immutable bytes.
            finding = check.evaluate(MappingProxyType(snapshot))
        except (ImportError, FileNotFoundError) as exc:
            finding = Finding(Status.ENV_BLOCKED, {"reason": str(exc)})
        except Exception as exc:
            finding = Finding(Status.ERROR, {"reason": f"{type(exc).__name__}: {exc}"})
        if (
            not isinstance(finding, Finding)
            or not isinstance(finding.status, Status)
            or not isinstance(finding.details, dict)
        ):
            finding = Finding(Status.ERROR, {"reason": "invalid checker result"})
        else:
            try:
                # Freeze the report's validated JSON details independently from
                # any mutable object retained by the evaluator.
                details_json = json.dumps(finding.details, allow_nan=False, sort_keys=True)
                finding = Finding(finding.status, json.loads(details_json))
            except (ValueError, TypeError) as exc:
                finding = Finding(Status.ERROR, {"reason": f"invalid report details: {exc}"})
    return {
        "format": "nsrw-research-verification-v1",
        "check_id": check.check_id,
        "revision": check.revision,
        "target": check.target,
        "domain": check.domain,
        "method": check.method,
        "evidence_class": check.evidence_class,
        "status": finding.status.value,
        "inputs": input_digests,
        "details": finding.details,
        "claim_authority": "NONE",
        "claim_status": "UNVERIFIED",
    }
