from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def test_release_versions_and_first_manuscript_selection() -> None:
    from nsrw import __version__

    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert f'version = "{__version__}"' in project
    assert f"version: {__version__}\n" in citation
    manifest = (ROOT / "research-papers/SHA256SUMS-P01-v0.4").read_text(encoding="utf-8")
    import hashlib

    for row in manifest.splitlines():
        expected, name = row.split("  ", 1)
        assert "P01_" in name and "P02_" not in name and "P03_" not in name
        assert hashlib.sha256((ROOT / "research-papers" / name).read_bytes()).hexdigest() == expected


def test_only_selected_second_manuscript_and_no_private_strategy_are_indexed() -> None:
    result = subprocess.run(["git", "ls-files", "-z", "research-papers"], cwd=ROOT,
                            capture_output=True, check=True)
    names = result.stdout.decode("utf-8").split("\0")
    selected_p02 = {
        "research-papers/P02_SourceBound_ReproducibleResearch.md",
        "research-papers/latex/P02_SourceBound_ReproducibleResearch.tex",
        "research-papers/pdf/P02_SourceBound_ReproducibleResearch.pdf",
    }
    assert not any("/private/" in name or "P03_" in name for name in names)
    assert {name for name in names if "P02_" in name} == selected_p02 | {
        "research-papers/versions/P02-v0.6/P02_SourceBound_ReproducibleResearch." + ext
        for ext in ("md", "tex", "pdf")
    }
    import hashlib

    manifest = (ROOT / "research-papers/SHA256SUMS-P02-v0.5").read_text(encoding="utf-8")
    listed = set()
    for row in manifest.splitlines():
        expected, name = row.split("  ", 1)
        listed.add(f"research-papers/{name}")
        assert hashlib.sha256((ROOT / "research-papers" / name).read_bytes()).hexdigest() == expected
    assert listed == selected_p02


def _markdown_files() -> list[Path]:
    return [ROOT / "README.md", ROOT / "colab/README.md", ROOT / "formal/p2/README.md",
            *sorted((ROOT / "docs").rglob("*.md"))]


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
        ROOT / "docs" / "releases" / "v0.2.3.md",
        ROOT / "docs" / "stage_receipts" / "M4P_V0.2.3_LOCAL_CLOSURE.md",
        ROOT / "CHANGELOG.md",
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


def test_publication_ignore_rules_preserve_reproduction_inputs() -> None:
    local_only = {
        "colab/evidence/2026-10-13/candidate/archive.zip",
        "colab/c03-observe.py",
        "colab/c04c-replay-start.py",
        "colab/zplus-j-preserve-drive.py",
        "publication/p2-z-phase-2026-10-12-candidate/README.md",
        "scripts/build-p2-z-held-derivative.py",
    }
    public_inputs = {
        "colab/run-c02-development.py",
        "colab/run-c04-development.py",
        "colab/run-zplus-j-development.py",
        "colab/run-zplus-j-composition-development.py",
        "colab/ZPLUS_J_DEVELOPMENT_2026-10-11.ipynb",
        "scripts/run-p2-z-replay.py",
        "formal/p2/P2_ZPLUS_J_SourceComposition.lean",
        "docs/stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md",
        "docs/releases/v0.4.0.md",
        "tests/test_p2_zplus_j_development.py",
    }
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--stdin", "-z"], cwd=ROOT,
        input=("\0".join(sorted(local_only | public_inputs)) + "\0").encode("utf-8"),
        capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert set(result.stdout.decode("utf-8").rstrip("\0").split("\0")) == local_only
    assert all((ROOT / name).is_file() for name in public_inputs)


def _ignored_indexed_files(root: Path) -> set[str]:
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=root,
                             capture_output=True, check=True).stdout
    result = subprocess.run(["git", "check-ignore", "--no-index", "--stdin", "-z"],
                            cwd=root, input=tracked, capture_output=True, check=False)
    assert result.returncode in (0, 1), result.stderr
    return {name.decode("utf-8") for name in result.stdout.split(b"\0") if name}


def test_no_indexed_file_bypasses_ignore_boundary() -> None:
    assert not _ignored_indexed_files(ROOT), "Tracked/indexed files bypass the ignore policy"


def test_index_guard_detects_force_added_private_artifact(tmp_path: Path) -> None:
    root = tmp_path / "isolated-repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / ".gitignore").write_text("colab/evidence/\n", encoding="utf-8")
    raw = root / "colab/evidence/local.zip"
    raw.parent.mkdir(parents=True)
    raw.write_bytes(b"synthetic-private-artifact")
    subprocess.run(["git", "add", ".gitignore"], cwd=root, check=True)
    assert _ignored_indexed_files(root) == set()
    subprocess.run(["git", "add", "--force", "colab/evidence/local.zip"], cwd=root, check=True)
    assert _ignored_indexed_files(root) == {"colab/evidence/local.zip"}


def test_declared_z_replay_inputs_have_portable_git_blob_identity() -> None:
    spec = importlib.util.spec_from_file_location("document_z_inputs", ROOT / "scripts/run-p2-z-replay.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    paths = list(runner.PINS)
    assert all((ROOT / name).is_file() for name in runner.INPUTS)
    result = subprocess.run(["git", "hash-object", "--stdin-paths"], cwd=ROOT,
                            input=("\n".join(paths) + "\n").encode("utf-8"),
                            capture_output=True, check=True)
    hashes = result.stdout.decode("ascii").splitlines()
    assert len(hashes) == len(paths)
    assert dict(zip(paths, hashes, strict=True)) == runner.PINS


@pytest.mark.parametrize("workflow_path", sorted((ROOT / ".github/workflows").glob("*.yml")))
def test_workflow_action_references_are_immutable(workflow_path: Path) -> None:
    workflow = workflow_path.read_text(encoding="utf-8")
    actions = re.findall(r"(?m)^\s+uses:\s+([^\s#]+)", workflow)
    assert actions
    assert all(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[a-f0-9]{40}", action)
               for action in actions)


def test_ci_checkout_and_report_safety_contract() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "permissions:\n  contents: read\n" in workflow
    assert "pull_request_target:" not in workflow
    steps = re.split(r"(?m)^      - ", workflow)[1:]
    checkouts = [step for step in steps if "uses: actions/checkout@" in step]
    assert len(checkouts) == 4
    assert all("persist-credentials: false" in step for step in checkouts)
    report = next(step for step in steps if step.startswith("name: Preserve Python test reports"))
    assert "if: ${{ always() }}" in report
    assert "outputs/ci-report/junit.xml" in report
    assert "outputs/ci-report/coverage.xml" in report
    assert "include-hidden-files: false" in report
    assert "colab/evidence" not in report and "publication/" not in report


@pytest.mark.parametrize("version", ["P01-v0.5", "P02-v0.6"])
def test_current_manuscript_manifest(version: str) -> None:
    import hashlib
    rows = (ROOT / "research-papers" / f"SHA256SUMS-{version}").read_text(encoding="utf-8").splitlines()
    assert len(rows) == 3
    for row in rows:
        digest, name = row.split("  ", 1)
        assert name.startswith(f"versions/{version}/")
        assert hashlib.sha256((ROOT / "research-papers" / name).read_bytes()).hexdigest() == digest


def test_public_site_allowlist_and_relative_links(tmp_path: Path) -> None:
    from html.parser import HTMLParser
    spec = importlib.util.spec_from_file_location("research_site", ROOT / "scripts/build-research-site.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = tmp_path / "site"
    module.build(output)
    assert not any("private" in str(p) or "P03" in str(p) for p in output.rglob("*"))
    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key in ("href", "src") and value and not value.startswith(("https:", "http:", "#")):
                    assert (output / value).is_file(), value
    Links().feed((output / "index.html").read_text(encoding="utf-8"))
    (output / "unapproved.txt").write_text("synthetic unapproved output", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected file"):
        module.build(output)


def test_site_scalar_widths_match_retained_exact_records(tmp_path: Path) -> None:
    import json
    from fractions import Fraction
    from html.parser import HTMLParser

    spec = importlib.util.spec_from_file_location("site_widths", ROOT / "scripts/build-research-site.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = tmp_path / "site"
    module.build(output)
    observed = {}

    class Widths(HTMLParser):
        bits = None

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "tr" and "data-precision" in attrs:
                self.bits = int(attrs["data-precision"])
            if tag == "td" and "data-width" in attrs:
                observed[self.bits, attrs["data-quantity"]] = Fraction(attrs["data-width"])

    page = (output / "index.html").read_text(encoding="utf-8")
    Widths().feed(page)
    assert len(observed) == 9
    for bits in (128, 256, 512):
        record = json.loads((ROOT / f"examples/p2-core-scalars/core-scalars-{bits}.json")
                            .read_text(encoding="utf-8"))
        for key in ("plateau_width", "weight_gap", "main_denominator"):
            expected = Fraction(record[key]["upper"]) - Fraction(record[key]["lower"])
            assert observed[bits, key] == expected > 0
            if bits != 128:
                assert observed[bits, key] < observed[bits // 2, key]
    assert "{{" not in page
    assert "/blob/main/" not in page and "/tree/main/" not in page


def test_paper_landing_metadata_identifies_one_actual_pdf(tmp_path: Path) -> None:
    from html.parser import HTMLParser
    from urllib.parse import urlsplit

    spec = importlib.util.spec_from_file_location("site_papers", ROOT / "scripts/build-research-site.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = tmp_path / "site"
    module.build(output)

    class Metadata(HTMLParser):
        def __init__(self):
            super().__init__()
            self.fields = {}

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "meta" and attrs.get("name", "").startswith("citation_"):
                assert attrs["name"] not in self.fields
                self.fields[attrs["name"]] = attrs.get("content", "")

    for name in ("p01", "p02"):
        metadata = Metadata()
        metadata.feed((output / "papers" / (name + ".html")).read_text(encoding="utf-8"))
        fields = metadata.fields
        assert fields["citation_author"] == "Yun, Kwansub"
        assert fields["citation_doi"].startswith("10.5281/zenodo.")
        assert (output / "papers" / Path(urlsplit(fields["citation_pdf_url"]).path).name).is_file()
        assert fields["citation_publication_date"] == "2026/10/31"
