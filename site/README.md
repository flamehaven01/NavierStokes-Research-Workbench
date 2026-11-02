# NSRW research website

The site introduces NSRW's mathematical findings and the path from equations to useful scientific code. Keep the result, mechanism and research direction central. Define the scope beside the relevant statement; avoid repeating defensive disclaimers.

## Build and preview

From the repository root, with Python >=3.10 and the pinned site dependency (`python -m pip install -e ".[site]"`):

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

The public document reader is generated from the five explicit `DOCS` entries in the builder. It rewrites links to either another reader page or the exact build commit. Add a Writing essay only after its real URL exists. `site/bridge.json` is the sole diagram source; EQA links to NSRW rather than keeping a second editable architecture.

The optional verification dependency is separate from the site build. `scripts/check-core-scalars-mpmath.py` checks retained records without importing the producer. Its retained execution is linked from EQA; it is a same-operator second-backend cross-check. Published paper and software release bytes are preserved.


## Papers and citations

Keep the two-paper layout. Manuscript versions P01 v0.5 / P02 v0.6 are distinct
from software release v0.5.0 at cdce801d7c3f1991e8a0dce48aae9f825b03e9b1.
The paper PDF Git blobs match that release. Qualitative and quantitative proof
replays retain their separate historical checkpoints.

The three files in `site/citations/` are the official Zenodo BibTeX exports,
retrieved on 1 November 2026. Paper version DOIs are 23835054 / 23835112;
all-version DOIs are 23835053 / 23835111. Software v0.5.0 is 23835493 and its
all-version DOI is 23381778 (all identifiers use the 10.5281/zenodo. prefix).
The builder inserts those retained exports into the Papers section and individual
paper pages. `citations.js` only copies the selected citation after a reader click;
there is no network request. On clipboard denial it offers manual copy/download.

P02 v0.6 §7.2 already reports the three-precision scalar experiment. The mpmath
second-backend check is subsequent software work. Describe the actual recorded
invocation/elaboration/preservation incidents accurately; the scalar gap's
3.84e-18 magnitude is not binary64 underflow. Published manuscript bytes are not
modified by these website explanations.
