"""figure_targets.py — the target-discovery centerpiece: a convergent-evidence matrix.

Research-track deliverable: the signed causal map nominates druggable **brakes**
on CD4+ T-cell effector function (release the brake -> boost immunity). Because
the positive quadrant is noisy at 2 donors, a candidate must survive CONVERGENT
evidence. This bubble matrix scores the shortlist across 7 evidence dimensions
(dot size + color = strength, 0-1).

Effect / brake-direction / donor-consistency / viability come from the genome-scale
CD4 leaderboard (`ranked_perturbations.csv`); druggability / immune-genetics /
clinical-precedent are curated from the MCP-verified dossiers (`dossiers/*.json`:
Open Targets, ChEMBL v34, ClinicalTrials.gov v2). Values are documented per cell.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

SURFACE = "#fcfcfb"; INK = "#0b1220"; INK2 = "#39424e"; MUTED = "#8a8880"
TEAL = "#0d9488"; AMBER = "#d97a12"; GRID = "#e9e8e2"

DIMS = ["Causal\neffect", "Brake\ndirection", "Donor\nconsistency", "Viability\n(fitness)",
        "Drugg-\nability", "Immune\ngenetics", "Clinical\nprecedent"]

# rows: (gene, call, call_color, [7 scores 0-1], one-line evidence)
# NB: this is a curated evidence *summary* (0-1 per axis), not a fitted/weighted
# model. CBLB leads on external (clinical + genetics) evidence; CD5/DGKA are the
# most screen-consistent; SMAD3/UBASH3A are exploratory. Scores documented per cell.
TARGETS = [
    ("CBLB", "LEAD · clinical", AMBER,
     [0.88, 0.72, 0.35, 0.55, 1.00, 0.90, 0.90],
     "CBL-B inhibitors NX-1607, HST-1011 in trials · autoimmune assoc."),
    ("CD5", "SCREEN-CONSISTENT", TEAL,
     [0.87, 0.75, 1.00, 0.90, 0.70, 0.50, 0.40],
     "donor-consistent · CD5 deletion boosts CAR-T (preclinical)"),
    ("DGKA", "SCREEN-CONSISTENT", TEAL,
     [0.71, 0.42, 1.00, 0.78, 1.00, 0.25, 0.85],
     "donor-consistent · Bayer DGKα inhibitor in Ph1"),
    ("SMAD3", "EXPLORATORY", "#7a8a99",
     [0.92, 0.32, 0.35, 0.90, 0.60, 0.45, 0.55],
     "highest-effect brake · TGF-β node · donor-split"),
    ("UBASH3A", "GENETICS-LED", "#7a8a99",
     [0.40, 0.28, 0.35, 0.82, 0.55, 0.90, 0.15],
     "T1D / RA GWAS · tractable phosphatase · weak in screen"),
]

CMAP = LinearSegmentedColormap.from_list("t", ["#e8f2f0", "#7fccc0", TEAL, "#0b5a53"])


def build(out_png: str, out_svg: str) -> None:
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
                         "svg.fonttype": "none"})
    n_r, n_c = len(TARGETS), len(DIMS)
    fig, ax = plt.subplots(figsize=(13.4, 7.6), dpi=210)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)

    ax.set_xlim(-0.5, n_c + 5.0); ax.set_ylim(-0.9, n_r + 0.2)
    ax.invert_yaxis()

    # column headers
    for j, d in enumerate(DIMS):
        ax.text(j, -0.75, d, ha="center", va="center", fontsize=11.5, color=INK2, fontweight="bold", linespacing=1.05)
    ax.text(n_c + 0.55, -0.75, "Call", ha="left", va="center", fontsize=11.5, color=INK2, fontweight="bold")

    for i, (gene, call, ccol, scores, ev) in enumerate(TARGETS):
        # gene name
        ax.text(-0.62, i, gene, ha="right", va="center", fontsize=16, color=INK, fontweight="bold", family="Helvetica Neue")
        # bubbles
        for j, s in enumerate(scores):
            ax.scatter(j, i, s=120 + s * 900, c=[CMAP(s)], edgecolors="white", linewidths=1.4, zorder=3)
        # call chip
        ax.text(n_c + 0.55, i - 0.16, call, ha="left", va="center", fontsize=12.5, color=ccol, fontweight="bold")
        ax.text(n_c + 0.55, i + 0.2, ev, ha="left", va="center", fontsize=8.6, color=MUTED)

    # gridlines (recessive)
    for j in range(n_c):
        ax.axvline(j, color=GRID, lw=0.8, zorder=0)
    for i in range(n_r):
        ax.axhline(i, color=GRID, lw=0.8, zorder=0)

    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    # legend for bubble size/color
    lx = 0.2
    for k, s in enumerate([0.25, 0.6, 1.0]):
        ax.scatter(lx + k * 0.9, n_r - 0.35, s=120 + s * 900, c=[CMAP(s)], edgecolors="white", linewidths=1.2)
    ax.text(lx - 0.35, n_r - 0.35, "evidence", ha="right", va="center", fontsize=10, color=MUTED)
    ax.text(lx + 2.5, n_r - 0.35, "weak to strong  (0–1)", ha="left", va="center", fontsize=10, color=MUTED)

    fig.text(0.045, 0.975, "A convergent-evidence shortlist of druggable T-cell brakes",
             fontsize=18, fontweight="bold", color=INK, va="top")
    fig.text(0.045, 0.935,
             "Release the brake, boost the effector program — an 8-hour transcriptional signature, not a functional assay.",
             fontsize=11, color=MUTED, va="top")
    fig.text(0.045, 0.906,
             "Evidence curated 0–1 from Open Targets · ChEMBL · ClinicalTrials.gov — a summary, not a fitted model.",
             fontsize=11, color=MUTED, va="top")
    fig.subplots_adjust(left=0.135, right=0.995, top=0.83, bottom=0.05)
    fig.savefig(out_png, dpi=210, facecolor=SURFACE); fig.savefig(out_svg, facecolor=SURFACE)
    plt.close(fig)
    print("wrote", out_png, "+", out_svg)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", default="../deliverables/figures/target_matrix.png")
    ap.add_argument("--svg", default="../deliverables/figures/target_matrix.svg")
    a = ap.parse_args()
    build(a.png, a.svg)
