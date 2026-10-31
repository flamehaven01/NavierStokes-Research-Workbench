"""Build the GitHub Pages site from an explicit public-file allowlist."""
import json
import shutil
import subprocess
from decimal import Decimal, localcontext
from fractions import Fraction
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs/site"
FILES = {
    "site/index.html": "index.html",
    "site/style.css": "style.css",
    "site/social-preview.png": "social-preview.png",
    "site/robots.txt": "robots.txt",
    "site/sitemap.xml": "sitemap.xml",
    "site/papers/p01.html": "papers/p01.html",
    "site/papers/p02.html": "papers/p02.html",
    "research-papers/versions/P01-v0.5/P01_MassZero_AngularMismatch.pdf": "papers/P01_MassZero_AngularMismatch.pdf",
    "research-papers/versions/P02-v0.6/P02_SourceBound_ReproducibleResearch.pdf": "papers/P02_SourceBound_ReproducibleResearch.pdf",
    **{f"examples/p2-core-scalars/core-scalars-{b}.json": f"data/core-scalars-{b}.json" for b in (128, 256, 512)},
}


def scalar_display() -> tuple[str, str]:
    """Render retained rational bounds; this is display, not a new verifier."""
    fields = (("plateau_width", "Plateau width w"),
              ("weight_gap", "Weight gap G"),
              ("main_denominator", "Main denominator D"))
    records = []
    for bits in (128, 256, 512):
        record = json.loads((ROOT / f"examples/p2-core-scalars/core-scalars-{bits}.json")
                            .read_text(encoding="utf-8"))
        if record["scope"] != "CORE_SCALAR_ENCLOSURES_ONLY" or record["precision_fractional_bits"] != bits:
            raise ValueError("Core display scope or precision mismatch")
        records.append((bits, record))
    values = "<dl>"
    for key, label in fields:
        value = Fraction(records[0][1][key]["lower"])
        with localcontext() as context:
            context.prec = 12
            decimal = Decimal(value.numerator) / Decimal(value.denominator)
        values += f"<dt>{escape(label)}</dt><dd>≈ {decimal:.10E}</dd>"
    values += "</dl>"
    table = ('<div class="table-wrap"><table class="scalar-table">'
             '<caption>Exact enclosure widths from the retained JSON records</caption>'
             '<thead><tr><th>Fractional bits</th>')
    table += "".join(f"<th>{escape(label)}</th>" for _, label in fields)
    table += "</tr></thead><tbody>"
    exact = '<div class="exact-records">'
    for bits, record in records:
        table += f'<tr data-precision="{bits}"><td>{bits}</td>'
        exact += f'<details><summary>{bits}-bit exact endpoints</summary><dl>'
        for key, label in fields:
            lo, hi = (Fraction(record[key][bound]) for bound in ("lower", "upper"))
            width = hi - lo
            if lo <= 0 or width <= 0:
                raise ValueError("Invalid positive enclosure for display")
            quanta = width * (1 << bits)
            if quanta.denominator != 1:
                raise ValueError("Width is not on the declared dyadic grid")
            table += (f'<td data-quantity="{key}" data-width="{width}">'
                      f'{quanta.numerator} × 2<sup>−{bits}</sup></td>')
            exact += (f'<dt>{escape(label)}</dt><dd><code>lower: {lo}</code><br>'
                      f'<code>upper: {hi}</code></dd>')
        table += "</tr>"
        exact += "</dl></details>"
    return values, table + "</tbody></table></div>" + exact + "</div>"


def build(output: Path = OUTPUT) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for source, target in FILES.items():
        dest = output / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, dest)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    values, table = scalar_display()
    page = (output / "index.html").read_text(encoding="utf-8")
    for token, content in {
        "{{CORE_SCALAR_VALUES}}": values, "{{CORE_SCALAR_TABLE}}": table,
        "{{SITE_REVISION_SHORT}}": revision[:8],
        "{{SITE_SOURCE_URL}}": "https://github.com/flamehaven01/NavierStokes-Research-Workbench/tree/" + revision,
    }.items():
        page = page.replace(token, content)
    if "{{" in page:
        raise ValueError("Unresolved site template field")
    (output / "index.html").write_text(page, encoding="utf-8", newline="\n")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual != {*FILES.values(), ".nojekyll"}:
        raise ValueError("Unexpected file in public site output; use a fresh output directory")


if __name__ == "__main__":
    build()
    print("PUBLIC_SITE_ALLOWLIST_BUILD_PASS")
