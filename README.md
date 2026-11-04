# QIBC Plot

**Quantitative image-based cytometry (QIBC) plots from CellProfiler output, in a single offline HTML file.**

[![License: PolyForm Noncommercial 1.0.0](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-orange.svg)](LICENSE)
[![Free for academic use](https://img.shields.io/badge/academic%20use-free-brightgreen.svg)](#license)
[![No install](https://img.shields.io/badge/install-none-brightgreen.svg)](#getting-started)
[![Data stays local](https://img.shields.io/badge/data-never%20uploaded-brightgreen.svg)](#privacy)

QIBC Plot turns a CellProfiler per-nucleus table into the two standard QIBC figures: a cell-cycle scatter of total DNA against a nuclear marker, coloured by a third channel, and a per-condition dot-bar plot. It needs no R, no ggplot2 and no proprietary analysis software, just a browser.

**[→ Open the live app](https://lao-labtools.org/qibc/)**  ·  **[Download the file](index.html)**  ·  **[Report a bug](https://github.com/laolabtools/qibc-plot/issues)**  ·  **[More Lao LabTools](https://lao-labtools.org)**

## Why this exists

QIBC extracts single-cell measurements from thousands of nuclei per condition and plots them so that cell-cycle position and marker intensity can be read together. The plots were long tied to proprietary microscope and visualisation software. [qibcPlot](https://github.com/callum-jpg/qibcPlot) by callum-jpg showed how to make them from CellProfiler output with R and ggplot2. This app does the same thing in the browser, interactively, so you can tune axes, gates and colours and export the figure without writing code.

## Privacy

Your files are read by JavaScript in your own browser. Nothing is uploaded, there is no server, no account and no tracking, and once the page has loaded it keeps working with the network disconnected. That makes it safe for unpublished data and for data you are not allowed to put in a cloud service.

The hosted copy on [lao-labtools.org](https://lao-labtools.org) is covered by the site's [privacy policy](https://lao-labtools.org/privacy.html). A downloaded copy opened from your own disk makes no connection to the site at all.

## Getting started

There is nothing to install.

- **Online:** open **[lao-labtools.org/qibc](https://lao-labtools.org/qibc/)**.
- **Offline:** download [`index.html`](index.html) (open it on GitHub and press the download button) and double-click it. It opens in Chrome, Edge, Safari or Firefox and runs from your disk.

Press **Load example data (Nuclei.csv)** to see a finished analysis, or choose your own CellProfiler CSV.

## How to use

The left panel runs top to bottom in the order you normally work.

1. **Data.** Load a CellProfiler *per-object* table exported for your nuclei (typically `Nuclei.csv`), then pick the **grouping (metadata) column** that names each condition, for example `Metadata_FolderName` or a treatment column.
2. **Channels.**
   - **X axis:** total DNA, i.e. the *integrated* DAPI/Hoechst intensity.
   - **Y axis:** the *mean* intensity of your nuclear marker, optionally on a log₁₀ scale.
   - **Point colour:** a third channel. Each axis has an editable title.
3. **Axis and colour limits.** Set X, Y and colour ranges by hand or press **auto**. Out-of-range colour values can be *squished* to the limit so outliers do not wash out the scale. The same limits act as a gate, and each panel reports how many cells fall inside it.
4. **Appearance.** Colour palette (including Viridis), point size, opacity and an optional grey outline.
5. **Conditions.** Drag to reorder, untick to hide.
6. **Dot-bar plot.** Choose a channel and limits. Each condition is shown as jittered single cells with a mean line, optionally using only cells inside the X/Y/colour gate.

Press **Update plots**, then **Download PNG(s)**, or use the camera icon on any plot.

## Input format

A comma-separated table with one row per nucleus, as written by CellProfiler's *ExportToSpreadsheet* module. The app needs:

- at least one metadata column that identifies the condition;
- an integrated-intensity column for DNA;
- mean-intensity columns for the markers you want to plot.

Column names are read from the header, so any CellProfiler naming works. The [qibcPlot repository](https://github.com/callum-jpg/qibcPlot/tree/master/cellprofiler-pipeline) provides an example CellProfiler pipeline that produces a suitable table.

## Limitations

- The app plots and summarises measurements; it does not segment images. Measurement quality is set by your CellProfiler pipeline (segmentation, illumination correction, background).
- Very large tables (several hundred thousand nuclei) are limited by browser memory and drawing speed.
- Export is PNG. For vector figures, export the underlying table and replot.

## Building from source

There is no build step. `index.html` *is* the source: the app's own code is plain JavaScript at the end of the file, readable with View Source, and Plotly.js is inlined above it so the page works offline.

| file | contents |
|---|---|
| `index.html` | the complete app: markup, styles, bundled Plotly.js v3.6.0, app code and the example dataset |

## Reporting bugs and requesting features

Please use **[GitHub Issues](https://github.com/laolabtools/qibc-plot/issues)** for bugs, wrong results and feature requests. A useful report includes:

- what you did, what you expected and what happened instead;
- your browser and operating system;
- a screenshot, and if you can, a few rows of your CSV so the problem can be reproduced (remove anything confidential first).

If you would rather not post publicly, email [contact@lao-labtools.org](mailto:contact@lao-labtools.org).

## Citing

If this tool contributed to published work, please cite it as:

> Lao L. *QIBC Plot: browser-based quantitative image-based cytometry plotting*. 2026. https://github.com/laolabtools/qibc-plot

Please also cite the methods and resources it is built on (listed below), in particular qibcPlot, the original QIBC method and CellProfiler.

## Acknowledgements and references

**Where it comes from.** QIBC Plot is a browser reimplementation of **[qibcPlot](https://github.com/callum-jpg/qibcPlot)** by **callum-jpg**: R/ggplot2 scripts, an example CellProfiler pipeline and an example dataset for making QIBC 3-variable scatter and dot-bar plots. The plot designs, the choice of DNA integrated intensity vs. marker mean intensity coloured by a third channel, and the blue per-condition mean line all follow qibcPlot. No R code was copied; the app was written independently in JavaScript.

**Example data.** The built-in example (`Nuclei.csv`, 3,563 nuclei) is the example dataset distributed in the [qibcPlot repository](https://github.com/callum-jpg/qibcPlot/tree/master/example-data). It is included only to demonstrate the app; all rights in it remain with its author.

**Method.**
- Toledo LI *et al.* ATR prohibits replication catastrophe by preventing global exhaustion of RPA. *Cell* 155, 1088–1103 (2013). [doi:10.1016/j.cell.2013.10.043](https://doi.org/10.1016/j.cell.2013.10.043). This paper introduced QIBC.
- Stirling DR *et al.* CellProfiler 4: improvements in speed, utility and usability. *BMC Bioinformatics* 22, 433 (2021). [doi:10.1186/s12859-021-04344-9](https://doi.org/10.1186/s12859-021-04344-9). The source of the per-nucleus measurements.

**Software.**
- [Plotly.js](https://plotly.com/javascript/) v3.6.0, © Plotly, Inc., MIT licence. Bundled in the file for offline use.
- The Viridis colour map: Stéfan van der Walt and Nathaniel Smith, designed for matplotlib (CC0).

## License

**Free for academic and other non-commercial use** under the [PolyForm Noncommercial License 1.0.0](LICENSE).

In plain terms (the licence text is what counts): you may use, copy, modify and share this software for research, teaching, study and any other non-commercial purpose, including at universities, hospitals, non-profit research institutes and government laboratories. **Commercial use**, such as use by or for a company, in industry R&D, contract research or a paid service, is not covered and needs a separate licence. Contact [contact@lao-labtools.org](mailto:contact@lao-labtools.org).

**Third-party code.** Plotly.js v3.6.0 (MIT) and the components it bundles keep their own licences; their notices are preserved inside `index.html`.

**Example data.** The bundled `Nuclei.csv` example belongs to the author of qibcPlot and is not covered by this licence.

## Disclaimer

This is an independent research tool. It is provided as is, without warranty of any kind. Cross-check key numbers against established software before you publish them. It is for research use only. It is not a medical device and must not be used for diagnostic or clinical decisions.

---

Part of **[Lao LabTools](https://lao-labtools.org)**: free, install-free browser tools for the bench, by Linjiang Lao.
