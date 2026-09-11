from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _markdown_files() -> list[Path]:
    return [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]


def test_local_markdown_links_resolve() -> None:
    missing: list[str] = []
    for document in _markdown_files():
        text = document.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if target_path and not (document.parent / target_path).resolve().exists():
                missing.append(f"{document.relative_to(ROOT)} -> {target}")
    assert not missing, "Missing local documentation links:\n" + "\n".join(missing)


def test_primary_public_pages_avoid_unexplained_internal_jargon() -> None:
    public_pages = [
        ROOT / "README.md",
        ROOT / "docs" / "NAVIER_STOKES_NORTH_STAR_MAP.md",
        ROOT / "docs" / "M4_PARAMETRIC_AUDIT_DESIGN.md",
        ROOT / "docs" / "releases" / "v0.2.2.md",
    ]
    disallowed = (
        "spar frame",
        "independent researcher",
        "independent research program",
        "hard gate",
        "claim custody",
        "quantifier custody",
    )
    violations: list[str] = []
    for document in public_pages:
        lowered = document.read_text(encoding="utf-8").lower()
        for phrase in disallowed:
            if phrase in lowered:
                violations.append(f"{document.relative_to(ROOT)}: {phrase}")
    assert not violations, "Unexplained public jargon:\n" + "\n".join(violations)
