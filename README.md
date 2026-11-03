# QIBC Plot

Quantitative image-based cytometry (QIBC) plots from CellProfiler output, in a single offline HTML file.

[**Use it online:**](https://lao-labtools.org/qibc/)
**Or offline:** download `index.html` and open it in any modern browser. No install, no server, no internet needed.

Your data is parsed in your browser and never uploaded.

## What it does

- **Load** a CellProfiler per-nucleus table (e.g. `Nuclei.csv`), or try the built-in example data.
- **Group** cells by any metadata column (condition, treatment, well…).
- **3-variable cell-cycle scatter**: integrated DNA/DAPI (x) against a mean nuclear marker intensity (y, optional log₁₀), coloured by a third channel. One panel per condition, with matched axes.
- **Dot-bar plot**: per-condition jitter of any channel with a mean line, optionally restricted to cells inside the X/Y/colour gate.
- **Control the look**: axis and colour limits (with optional squishing of out-of-range colours), colour palette, point size, opacity, outlines, and drag-to-reorder or hide conditions.
- **Export** publication-ready PNGs.

## Credit

A browser reimplementation of [qibcPlot](https://github.com/callum-jpg/qibcPlot) (R/ggplot2) by callum-jpg. Plots are drawn with [Plotly.js](https://plotly.com/javascript/) (MIT licence), which is bundled inside the file so it works offline.

## Feedback

Bug reports and suggestions are welcome as [GitHub issues](https://github.com/laolabtools/qibc-plot/issues), or by email to contact@lao-labtools.org.

More tools: https://lao-labtools.org
