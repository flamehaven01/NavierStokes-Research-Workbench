# Typeset the manuscripts

The P01 and P02 `.tex` files are standalone academic articles with embedded references.
No extra figures, bibliography database or external source file is required.
The corresponding exported PDFs are in `../pdf/`.

Tested with Tectonic 0.17.0 on Windows. From the distribution root, with a
working Tectonic installation and TeX resource bundle:

```sh
tectonic research-papers/latex/P01_MassZero_AngularMismatch.tex
tectonic research-papers/latex/P02_SourceBound_ReproducibleResearch.tex
```

Use `--outdir` to place regenerated files outside the selected distribution.
After warming the required resources, `--only-cached` avoids network retrieval.
Other compatible LaTeX engines may also be used with the listed packages.
New PDF creation dates and byte hashes need not match the retained typeset files.
Compare the content and record the identity of each regenerated output.

These are manuscript typesetting instructions, not the Lean reproduction
procedure in `../REPRODUCE.md`. The article format does not assert arXiv
submission, journal acceptance, or publication approval.
