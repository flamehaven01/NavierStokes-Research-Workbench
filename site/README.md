# NSRW research website

The site introduces NSRW's mathematical findings and the path from equations to useful scientific code. Keep the result, mechanism and research direction central. Define the scope beside the relevant statement; avoid repeating defensive disclaimers.

## Build and preview

From the repository root, with Python >=3.10:

```text
python scripts/build-research-site.py
python -m http.server 8765 --directory outputs/site
```

The explicit file allowlist copies public paper PDFs, retained scalar JSON and site assets only. The builder renders scalar values and exact interval widths from those JSON records, and inserts the actual build commit into the footer. Approximate decimal values are reading aids; expandable rational endpoints and widths preserve the exact bounds.

The site uses native MathML and local/system fonts. No runtime math library, external font service or client-side script is required. Paper landing pages carry one paper's citation metadata each. Visible author spelling remains Yun Kwansub; the structured family/given names are Yun / Kwansub, matching the approved citation record. Do not invent an ORCID.

Pinned links distinguish the Z execution, later quantitative execution, receipt-document revisions and software release. The GitHub repository root is explicitly a latest-code link. A site deployment does not change the historical v0.5.0 tag, paper bytes or mathematical admission.

## Checks

```text
python -m pytest tests/test_docs.py --no-cov
```

Inspect desktop and narrow-screen layouts, mobile navigation, MathML, contained table scrolling, exact-endpoint expanders, paper links and the roadmap. Before deployment, compare displayed interval widths with the retained JSON and preserve existing paper hashes. After deployment, inspect the public URL and verify its source commit footer.
