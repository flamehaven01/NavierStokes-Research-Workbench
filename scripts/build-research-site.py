"""Build the GitHub Pages site from an explicit public-file allowlist."""
import hashlib
import json
import re
import shutil
import subprocess
from decimal import Decimal, localcontext
from fractions import Fraction
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs/site"
FILES = {
    "site/index.html": "index.html",
    "site/style.css": "style.css",
    "site/citations.js": "citations.js",
    **{f"site/citations/{key}.bib": f"citations/{key}.bib" for key in ("p01", "p02", "software")},
    "site/social-preview.png": "social-preview.png",
    "site/robots.txt": "robots.txt",
    "site/sitemap.xml": "sitemap.xml",
    "site/bridge.json": "data/bridge.json",
    "examples/p2-core-scalars/mpmath-crosscheck.json": "data/mpmath-crosscheck.json",
    "site/papers/p01.html": "papers/p01.html",
    "site/papers/p02.html": "papers/p02.html",
    "research-papers/versions/P01-v0.5/P01_MassZero_AngularMismatch.pdf": "papers/P01_MassZero_AngularMismatch.pdf",
    "research-papers/versions/P02-v0.6/P02_SourceBound_ReproducibleResearch.pdf": "papers/P02_SourceBound_ReproducibleResearch.pdf",
    **{f"examples/p2-core-scalars/core-scalars-{b}.json": f"data/core-scalars-{b}.json" for b in (128, 256, 512)},
}
DOCS = (
    ("start", "Start here", "docs/NSRW_RESEARCH_GUIDE.md"),
    ("bridge", "Math to scientific code", "docs/NSRW_MATH_TO_CODE_BRIDGE.md"),
    ("scalar-method", "Exact-rational method", "docs/P2_CORE_SCALAR_METHOD_2026-10-31.md"),
    ("crosscheck", "Second-backend verification", "docs/NSRW_CORE_SCALAR_CROSSCHECK.md"),
    ("reproduce", "Reproduce the results", "research-papers/REPRODUCE.md"),
)
GENERATED = {"docs/index.html", "writing/index.html", "bridge.svg",
             *(f"docs/{slug}.html" for slug, _, _ in DOCS)}


def citation_block(key: str, prefix: str = "") -> str:
    """Use the retained official Zenodo export, not an inferred citation."""
    title = {"p01": "P01 v0.5", "p02": "P02 v0.6", "software": "Software v0.5.0"}[key]
    bib = (ROOT / f"site/citations/{key}.bib").read_text(encoding="utf-8")
    return (f'<details class="citation-details"><summary>Cite {title} · BibTeX</summary>'
            f'<div class="citation-tools"><button type="button" data-copy-citation="cite-{key}">Copy BibTeX</button>'
            f'<a href="{prefix}citations/{key}.bib" download>Download .bib</a><span role="status" aria-live="polite"></span></div>'
            f'<pre><code id="cite-{key}">{escape(bib)}</code></pre>'
            '<p class="citation-origin">Official Zenodo export · version-specific DOI. Use the all-versions link to discover later editions.</p></details>')


def bridge_svg() -> str:
    """One diagram source in NSRW; the Ledger links to this architecture."""
    data = json.loads((ROOT / "site/bridge.json").read_text(encoding="utf-8"))
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" aria-labelledby="title desc">',
           '<title id="title">From exact-real mathematics to a numerical J certificate</title>',
           '<desc id="desc">Established Lean results and implemented scalar computations feed the next coefficient and admissibility work, then a same-zero certificate, then a planned scientific diagnostic.</desc>',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="#8a9b86"/></marker></defs>',
           '<rect width="960" height="520" rx="8" fill="#f4f5ec"/>']
    nodes = {node["id"]: node for node in data["nodes"]}
    for start, end in data["edges"]:
        a, b = nodes[start], nodes[end]
        x1, y1, x2, y2 = a["x"] + 270, a["y"] + 60, b["x"], b["y"] + 60
        if a["x"] == b["x"]:
            x = a["x"] + 135
            svg.append(f'<path d="M{x} {a["y"]+120} L{x} {b["y"]}" fill="none" stroke="#8a9b86" stroke-width="2" marker-end="url(#arrow)"/>')
            continue
        svg.append(f'<path d="M{x1} {y1} C{x1+35} {y1} {x2-35} {y2} {x2} {y2}" fill="none" stroke="#8a9b86" stroke-width="2" marker-end="url(#arrow)"/>')
    for node in nodes.values():
        color = "#dfead4" if node["status"] in ("ESTABLISHED", "IMPLEMENTED") else "#fffdf7"
        x, y = node["x"], node["y"]
        svg.append(f'<rect x="{x}" y="{y}" width="270" height="120" rx="7" fill="{color}" stroke="#a7b69e"/>')
        for offset, text, size in ((25, node["status"], 11), (53, node["title"], 17), (82, node["detail"], 12)):
            svg.append(f'<text x="{x+16}" y="{y+offset}" fill="#243626" font-size="{size}" font-family="system-ui,sans-serif">{escape(text)}</text>')
    return "".join(svg) + "</svg>"


def reading_page(title: str, content: str, revision: str, active="", toc="") -> str:
    menu = "".join(f'<a {"aria-current=page" if slug == active else ""} href="../docs/{slug}.html">{escape(label)}</a>' for slug, label, _ in DOCS)
    menu += '<hr><a href="../index.html#papers">Papers &amp; citations</a><a href="../index.html#evidence">Proof records</a><a href="https://flamehaven01.github.io/Flamehaven-Verification-Ledger/eqa.html#toe-test-0061">EQA cross-check ↗</a><a href="../writing/">Research writing</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · NSRW</title><link rel="stylesheet" href="../style.css"></head><body>
<a class="skip" href="#content">Skip to document</a><header><a class="brand" href="../index.html">NSRW<span>Research library</span></a><nav aria-label="Primary"><a href="../index.html">Research</a> · <a href="../docs/">Documents</a> · <a href="../writing/">Writing</a></nav></header>
<div class="reader"><aside class="doc-nav"><nav class="doc-desktop" aria-label="Document library"><strong>Research documents</strong>{menu}</nav><details class="doc-mobile"><summary>Research documents</summary><nav aria-label="Mobile document library">{menu}</nav></details></aside>
<main id="content" class="doc-body">{content}</main><aside class="doc-toc"><nav aria-label="On this page"><strong>On this page</strong>{toc}</nav></aside></div>
<footer><p>NSRW · Equation → Proof → Code → Scientific Use</p><p>Source <a href="https://github.com/flamehaven01/NavierStokes-Research-Workbench/tree/{revision}">{revision[:8]}</a></p></footer></body></html>'''


def build_library(output: Path, revision: str) -> None:
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    routes = {path: f"{slug}.html" for slug, _, path in DOCS}
    repo = "https://github.com/flamehaven01/NavierStokes-Research-Workbench/blob/" + revision + "/"
    for slug, label, source in DOCS:
        text = (ROOT / source).read_text(encoding="utf-8")
        # Show source LaTeX as a distinct, copyable equation block when a document
        # has no MathML. Never silently drop mathematical source from the reader.
        text = re.sub(r"\\\[\s*(.*?)\s*\\\]", r"```text\n\1\n```", text, flags=re.S)
        tokens = md.parse(text)
        toc, seen = [], set()
        for i, token in enumerate(tokens):
            if token.type == "heading_open":
                heading = tokens[i + 1].content
                anchor = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-") or "section"
                while anchor in seen:
                    anchor += "-section"
                seen.add(anchor)
                token.attrSet("id", anchor)
                if token.tag in ("h2", "h3"):
                    toc.append(f'<a href="#{anchor}">{escape(heading)}</a>')
            for child in token.children or []:
                if child.type not in ("link_open", "image"):
                    continue
                attr = "href" if child.type == "link_open" else "src"
                url = child.attrGet(attr) or ""
                parts = urlsplit(url)
                if not parts.scheme and parts.path:
                    target = (ROOT / source).parent / parts.path
                    target = target.resolve().relative_to(ROOT.resolve()).as_posix()
                    link = routes.get(target, repo + target)
                    child.attrSet(attr, link + ("#" + parts.fragment if parts.fragment else ""))
        content = md.renderer.render(tokens, md.options, {})
        content += f'<p class="document-source"><a href="{repo+source}">View exact Markdown source ↗</a></p>'
        (output / f"docs/{slug}.html").write_text(reading_page(label, content, revision, slug, "".join(toc)), encoding="utf-8", newline="\n")
    cards = "".join(f'<li><a href="{slug}.html">{escape(label)}</a></li>' for slug, label, _ in DOCS)
    (output / "docs/index.html").write_text(reading_page("Research documents", '<h1>Research documents</h1><p>Follow the findings, inspect the methods, and run the computation. These guides connect the papers to the working research.</p><ul class="library-list">' + cards + '</ul>', revision), encoding="utf-8", newline="\n")
    article = "https://flamehaven.space/writing/from-a-scale-invariant-candidate-to-an-obstruction-what-changed-while-reproducing-a-navierstokes-construction/"
    writing = f'''<span class="eyebrow">RESEARCH WRITING</span><h1>Ideas, experiments<br>and what changed.</h1><p>Follow the research as it moves from mathematical questions to useful scientific code.</p><article class="essay"><span class="eyebrow">NAVIER–STOKES · RESEARCH PROCESS</span><h2>From a scale-invariant candidate to an obstruction</h2><p>What changed while reproducing a Navier–Stokes construction: the candidate ratio, the repair geometry, and the mathematical question that survived.</p><a class="primary" href="{article}">Read on Flamehaven Writing ↗</a></article><h2>Continue following the work</h2><p>Further essays appear on <a href="https://flamehaven.space/writing/">Flamehaven Writing</a>. This page curates the NSRW series; the <a href="../docs/">research library</a> provides the exact methods and reproduction guides.</p>'''
    (output / "writing").mkdir(exist_ok=True)
    (output / "writing/index.html").write_text(reading_page("Research writing", writing, revision), encoding="utf-8", newline="\n")


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


def crosscheck_summary() -> str:
    report = json.loads((ROOT / "examples/p2-core-scalars/mpmath-crosscheck.json").read_text(encoding="utf-8"))
    if report["status"] != "PASS" or len(report["records"]) != 3:
        raise ValueError("Invalid cross-check report")
    count = 0
    for bits, record in zip((128, 256, 512), report["records"], strict=True):
        raw = (ROOT / f"examples/p2-core-scalars/core-scalars-{bits}.json").read_bytes()
        if (record["input_lf_sha256"] != hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
            or record["fractional_bits"] != bits or record["status"] != "PASS"
            or record["independent_operator"] is not False
            or record["numerical_J_certificate"] is not False
            or record["scope"] != "CORE_SCALAR_ENCLOSURES_ONLY"
            or {c["quantity"] for c in record["checks"]} != {"ell", "v", "plateau_width", "weight_gap", "main_denominator"}
            or len(record["checks"]) != 5
            or any(c["status"] != "PASS" or c["relation"] != "contained" for c in record["checks"])):
            raise ValueError("Cross-check result or input identity drift")
        count += len(record["checks"])
    return f"{count} / {count}"


def build(output: Path = OUTPUT) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for source, target in FILES.items():
        dest = output / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, dest)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    (output / "docs").mkdir(exist_ok=True)
    build_library(output, revision)
    (output / "bridge.svg").write_text(bridge_svg(), encoding="utf-8", newline="\n")
    values, table = scalar_display()
    page = (output / "index.html").read_text(encoding="utf-8")
    for token, content in {
        "{{CORE_SCALAR_VALUES}}": values, "{{CORE_SCALAR_TABLE}}": table,
        "{{SITE_REVISION_SHORT}}": revision[:8],
        "{{BACKEND_CHECK_STATUS}}": crosscheck_summary(),
        **{f"{{{{CITATION_{key.upper()}}}}}": citation_block(key) for key in ("p01", "p02", "software")},
        "{{SITE_SOURCE_URL}}": "https://github.com/flamehaven01/NavierStokes-Research-Workbench/tree/" + revision,
    }.items():
        page = page.replace(token, content)
    if "{{" in page:
        raise ValueError("Unresolved site template field")
    (output / "index.html").write_text(page, encoding="utf-8", newline="\n")
    for key in ("p01", "p02"):
        path = output / f"papers/{key}.html"
        paper = path.read_text(encoding="utf-8").replace("{{CITATION}}", citation_block(key, "../"))
        if "{{" in paper:
            raise ValueError("Unresolved paper citation field")
        path.write_text(paper, encoding="utf-8", newline="\n")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual != {*FILES.values(), *GENERATED, ".nojekyll"}:
        raise ValueError("Unexpected file in public site output; use a fresh output directory")


if __name__ == "__main__":
    build()
    print("PUBLIC_SITE_ALLOWLIST_BUILD_PASS")
