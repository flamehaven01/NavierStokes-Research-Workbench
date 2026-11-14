"""Record the observed implementation files and runtime for registered checks."""

from __future__ import annotations

import hashlib
import importlib.util
import platform
import sys
import zlib
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

COMMON = ("nsrw", "nsrw.research_verification_cli", "nsrw.research_verification")
IMPLEMENTATIONS = {
    "mb08-inverse": ("nsrw.mb08_inverse_diagnostic", "fhval.exact_inverse"),
    "mb06-ratio": ("nsrw.mb06_ratio_crosscheck", "mpmath", "mpmath.ctx_iv", "mpmath.libmp.libmpi"),
    "forced-shear": (
        "nsrw.math_kernel.manufactured", "nsrw.math_kernel.operators",
        "nsrw.math_kernel.types", "nsrw.strict_json",
    ),
    "p1-lean-margin": ("nsrw.lean_archive_verification", "nsrw.strict_json"),
}


def implementation_identity(check_id: str) -> dict:
    files = {}
    missing = []
    for name in (*COMMON, *IMPLEMENTATIONS[check_id]):
        try:
            spec = importlib.util.find_spec(name)
            if spec is None or spec.origin is None:
                raise ModuleNotFoundError(name)
            raw = Path(spec.origin).read_bytes()
        except (ImportError, FileNotFoundError):
            missing.append(name)
        else:
            files[name] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

    packages = {}
    for name in {"mb06-ratio": ("mpmath",), "mb08-inverse": ("flamehaven-validator",)}.get(
        check_id, ()
    ):
        try:
            installed = distribution(name)
        except PackageNotFoundError:
            packages[name] = {"version": None}
        else:
            record = installed.read_text("RECORD")
            packages[name] = {
                "version": installed.version,
                "record_sha256": hashlib.sha256(record.encode()).hexdigest() if record else None,
            }
    return {
        "implementation_files": files,
        "unavailable_implementation_files": missing,
        "dependencies": packages,
        "runtime": {
            "implementation": sys.implementation.name,
            "python": platform.python_version(),
            "python_build": platform.python_build(),
            "system": platform.system(),
            "architecture": platform.machine(),
            "zlib": zlib.ZLIB_RUNTIME_VERSION,
        },
    }
