"""Simulate a CellProfiler per-nucleus table (Nuclei.csv layout) for the QIBC Plot example.

Every value is generated here from a simple cell-cycle model; no measured data are used.
Columns follow the layout of a standard CellProfiler MeasureObjectIntensity /
MeasureObjectSizeShape export for four channels (DAPI, Cy5, GFP, mCherry).

Model
- DNA content: G1 = 2N, S = uniform 2N-4N, G2/M = 4N, plus a few >4N cells under treatment.
- Cy5 (S-phase marker, e.g. EdU): low in G1/G2, high and peaking mid-S in S phase.
- mCherry (DNA-damage marker, e.g. gammaH2AX): background in control, induced in S/G2 by treatment.
- GFP: a uniform nuclear reporter, slightly up and more variable under treatment.
"""
import csv, math, sys
import numpy as np

rng = np.random.default_rng(20261104)
CH = ["cy5", "dapi", "gfp", "mcherry"]
W, H, MAXV = 1388, 1040, 16383   # image size (px) and 14-bit ceiling

COND = {
    "-Treatment": dict(phases=(0.52, 0.31, 0.17), dna2n=3.30e6, area2n=1750, mch=None,  gfp=(745, 0.035)),
    "+Treatment": dict(phases=(0.36, 0.43, 0.21), dna2n=3.45e6, area2n=2150, mch=True,  gfp=(1150, 0.17)),
}
IMAGES_PER_COND, CELLS_PER_IMAGE = 50, 36


def ln(m, s, n=None):
    return m * np.exp(rng.normal(0, s, n))


def cell(cond, p):
    ph = rng.choice(["G1", "S", "G2"], p=p["phases"])
    if ph == "G1":
        c = 2.0
    elif ph == "S":
        s_frac = rng.uniform(0, 1); c = 2.0 + 2.0 * s_frac
    else:
        c = 4.0
    if cond == "+Treatment" and ph == "G2" and rng.random() < 0.08:
        c = rng.uniform(4.6, 6.5)                        # a few re-replicated / polyploid cells
    dna = p["dna2n"] * (c / 2) * ln(1, 0.065)
    area = p["area2n"] * (c / 2) ** 0.65 * ln(1, 0.13)
    # S-phase marker (Cy5)
    if ph == "S":
        peak = 1 - (2 * s_frac - 1) ** 2               # brightest mid-S
        base = 620 if cond == "-Treatment" else 470
        cy5 = ln(150 + base * (0.35 + 0.65 * peak), 0.30)
    else:
        cy5 = ln(88, 0.16)
    # damage marker (mCherry)
    if p["mch"] is None:
        mch = ln(28, 0.45)
    else:
        mch = ln({"G1": 90, "S": 2100, "G2": 2900}[ph], 0.55 if ph == "G1" else 0.38)
    gfp = ln(p["gfp"][0], p["gfp"][1])
    return dna, area, {"cy5": cy5, "dapi": dna / area, "gfp": gfp, "mcherry": mch}


def pixel_stats(mean, area, ch):
    cv = {"cy5": 0.38, "dapi": 0.20, "gfp": 0.07, "mcherry": 0.55}[ch] * ln(1, 0.25)
    sd = mean * cv
    perim = 2 * math.sqrt(math.pi * area) * ln(1, 0.05)   # edge pixels
    edge_f = {"dapi": 0.66}.get(ch, 0.97) * ln(1, 0.06)
    emean = mean * edge_f
    q = {
        "Mean": mean, "Median": mean * (1 - 0.15 * cv), "Std": sd,
        "LowerQuartile": max(0, mean - 0.6745 * sd), "UpperQuartile": mean + 0.6745 * sd,
        "MAD": 0.6745 * sd * ln(1, 0.1),
        "Min": max(0, mean - 2.6 * sd * ln(1, 0.1)), "Max": min(MAXV, mean + 3.8 * sd * ln(1, 0.15)),
        "Integrated": mean * area,
        "MeanEdge": emean, "StdEdge": sd * 0.8 * ln(1, 0.1),
        "IntegratedEdge": emean * perim,
        "MinEdge": max(0, emean - 2.2 * sd * ln(1, 0.1)), "MaxEdge": min(MAXV, emean + 2.8 * sd * ln(1, 0.15)),
        "MassDisplacement": float(ln(0.35 if ch != "gfp" else 0.12, 0.7)),
    }
    for k in ("Integrated", "IntegratedEdge"):
        q[k] = round(q[k])
    for k in ("LowerQuartile", "UpperQuartile", "Median", "MAD", "Min", "Max", "MinEdge", "MaxEdge"):
        q[k] = round(q[k])                               # pixel-valued statistics are integers
    return q


INT_COLS = [("IntegratedIntensityEdge", "IntegratedEdge"), ("IntegratedIntensity", "Integrated"),
            ("LowerQuartileIntensity", "LowerQuartile"), ("MADIntensity", "MAD"),
            ("MassDisplacement", "MassDisplacement"), ("MaxIntensityEdge", "MaxEdge"),
            ("MaxIntensity", "Max"), ("MeanIntensityEdge", "MeanEdge"), ("MeanIntensity", "Mean"),
            ("MedianIntensity", "Median"), ("MinIntensityEdge", "MinEdge"), ("MinIntensity", "Min"),
            ("StdIntensityEdge", "StdEdge"), ("StdIntensity", "Std"),
            ("UpperQuartileIntensity", "UpperQuartile")]

header = ["", "ImageNumber", "ObjectNumber", "Metadata_FileLocation", "Metadata_FolderName",
          "Metadata_Frame", "Metadata_Series"]
header += [f"Intensity_{a}_rescale{c}channel" for a, _ in INT_COLS for c in CH]
header += [f"Location_CenterMassIntensity_{ax}_rescale{c}channel" for ax in "XYZ" for c in CH]
header += ["Location_Center_X", "Location_Center_Y", "Location_Center_Z"]
header += [f"Location_MaxIntensity_{ax}_rescale{c}channel" for ax in "XYZ" for c in CH]
header += ["Number_Object_Number"]

rows, rid = [], 0
order = list(rng.permutation(np.arange(1, 2 * IMAGES_PER_COND + 1)))
img_ids = {"-Treatment": sorted(order[:IMAGES_PER_COND]), "+Treatment": sorted(order[IMAGES_PER_COND:])}
for cond in ("-Treatment", "+Treatment"):
    p = COND[cond]
    for img in img_ids[cond]:
        n = max(8, int(rng.normal(CELLS_PER_IMAGE * (0.95 if cond == "+Treatment" else 1.05), 10)))
        for obj in range(1, n + 1):
            rid += 1
            dna, area, means = cell(cond, p)
            stats = {c: pixel_stats(float(means[c]), float(area), c) for c in CH}
            stats["dapi"]["Integrated"] = round(float(dna))
            r = math.sqrt(area / math.pi)
            cx, cy = rng.uniform(r + 2, W - r - 2), rng.uniform(r + 2, H - r - 2)
            row = [str(rid), img, obj, "NA", cond, 0, 0]
            row += [stats[c][k] for _, k in INT_COLS for c in CH]
            row += [cx + rng.normal(0, 0.8) for c in CH] + [cy + rng.normal(0, 0.8) for c in CH] + [0] * 4
            row += [cx, cy, 0]
            row += [int(round(cx + rng.normal(0, r / 3))) for c in CH] + [int(round(cy + rng.normal(0, r / 3))) for c in CH] + [0] * 4
            row += [obj]
            rows.append(row)


def fmt(v):
    if isinstance(v, str):
        return v if v == "NA" else f'"{v}"'
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    v = float(v)
    return str(int(v)) if v.is_integer() else repr(round(v, 10))


out = sys.argv[1] if len(sys.argv) > 1 else "Nuclei.csv"
with open(out, "w", newline="") as f:
    f.write(",".join(f'"{h}"' for h in header) + "\n")
    for r in rows:
        f.write(",".join(fmt(v) for v in r) + "\n")
print(f"wrote {len(rows)} nuclei x {len(header)} columns -> {out}")
