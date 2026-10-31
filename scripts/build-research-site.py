"""Build the GitHub Pages site from an explicit public-file allowlist."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs/site"
FILES = {
    "site/index.html": "index.html",
    "site/style.css": "style.css",
    "research-papers/versions/P01-v0.5/P01_MassZero_AngularMismatch.pdf": "papers/P01_MassZero_AngularMismatch.pdf",
    "research-papers/versions/P02-v0.6/P02_SourceBound_ReproducibleResearch.pdf": "papers/P02_SourceBound_ReproducibleResearch.pdf",
    **{f"examples/p2-core-scalars/core-scalars-{b}.json": f"data/core-scalars-{b}.json" for b in (128, 256, 512)},
}


def build(output: Path = OUTPUT) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for source, target in FILES.items():
        dest = output / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, dest)
    (output / ".nojekyll").write_text("", encoding="utf-8")
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual != {*FILES.values(), ".nojekyll"}:
        raise ValueError("Unexpected file in public site output; use a fresh output directory")


if __name__ == "__main__":
    build()
    print("PUBLIC_SITE_ALLOWLIST_BUILD_PASS")
