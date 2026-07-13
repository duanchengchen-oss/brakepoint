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

import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

import figstyle

# The first N_SCREEN dimensions are measured in the CD4 screen; the rest are
# curated from external databases. They are visually separated so the figure
# never implies the two provenances live on one comparable measured scale.
N_SCREEN = 4
DIMS = ["Causal\neffect", "Brake\ndirection", "Donor\nconsistency", "Screen\nfitness",
        "Target\ntractability", "Immune\ngenetics", "Clinical\nprecedent"]

# rows: (gene, call, call_color, [7 scores 0-1], one-line evidence)
# NB: this is a curated evidence *summary* (0-1 per axis), not a fitted/weighted
# model, and none of these are validated brakes — the positive quadrant is not
# brake-enriched (Mann-Whitney p = 0.70). CBLB leads on external (clinical +
# genetics) evidence; CD5/DGKA are the most screen-consistent; SMAD3/UBASH3A are
# exploratory. Colour marks candidate identity only (never machinery-teal).
TARGETS = [
    ("CBLB", "LEAD · external evidence", figstyle.AMBER,
     [0.96, 0.72, 0.35, 0.55, 1.00, 0.90, 0.90],
     "CBL-B inhibitors NX-1607, HST-1011 in trials · autoimmune assoc."),
    ("CD5", "SCREEN-CONSISTENT", figstyle.AMBER,
     [0.95, 0.75, 1.00, 0.90, 0.70, 0.50, 0.40],
     "donor-consistent · CD5 deletion boosts CAR-T (preclinical)"),
    ("DGKA", "SCREEN-CONSISTENT", figstyle.AMBER,
     [0.78, 0.42, 1.00, 0.78, 1.00, 0.25, 0.85],
     "donor-consistent · Bayer DGKα inhibitor in Ph1"),
    ("SMAD3", "EXPLORATORY", figstyle.MUTED,
     [1.00, 0.32, 0.35, 0.90, 0.60, 0.45, 0.55],
     "highest-effect candidate · TGF-β node · donor-split"),
    ("UBASH3A", "GENETICS-LED", figstyle.MUTED,
     [0.69, 0.28, 0.35, 0.82, 0.55, 0.90, 0.15],
     "T1D / RA GWAS · tractable phosphatase · weak in screen"),
]

# Sequential neutral ramp (dim -> bright): encodes evidence strength by lightness
# alone, so it is colourblind-safe and never collides with the teal/amber classes.
CMAP = LinearSegmentedColormap.from_list(
    "ev-dark", ["#243330", "#5d6f69", "#b9cfc8", "#eef5f2"]
)


def _bubble_size(s: float) -> float:
    """Marker area — small base so a weak score reads as visibly small."""
    return 55 + s * 1050


def build(out_png: str, out_svg: str) -> None:
    figstyle.apply_rc()
    n_r, n_c = len(TARGETS), len(DIMS)

    # Spaced column x-positions with an extra gap between the screen-derived and
    # curated-external blocks (stops adjacent 2-line headers from merging).
    pitch, gap = 1.32, 0.62
    xpos = np.array([j * pitch + (gap if j >= N_SCREEN else 0.0) for j in range(n_c)])
    x_div = (xpos[N_SCREEN - 1] + xpos[N_SCREEN]) / 2.0   # divider between blocks
    call_x = xpos[-1] + 1.5
    gene_x = -1.15

    fig, ax = figstyle.plt.subplots(figsize=(15.6, 7.8), dpi=200)
    fig.patch.set_facecolor(figstyle.BG)
    figstyle.radial_glow(fig)
    ax.set_facecolor("none")
    figstyle.style_axes(ax, grid=False, hide=("top", "right", "left", "bottom"))
    ax.set_xlim(gene_x - 0.55, call_x + 9.6)
    ax.set_ylim(-2.05, n_r + 0.55)
    ax.invert_yaxis()

    # provenance group headers + a light divider between the two blocks
    sc_mid = float(np.mean(xpos[:N_SCREEN])); ex_mid = float(np.mean(xpos[N_SCREEN:]))
    ax.text(sc_mid, -1.72, "MEASURED IN THE CD4 SCREEN", ha="center", va="center",
            fontsize=10.5, color=figstyle.BODY, fontweight="bold")
    ax.text(ex_mid, -1.72, "CURATED EXTERNAL EVIDENCE", ha="center", va="center",
            fontsize=10.5, color=figstyle.MUTED, fontweight="bold")
    ax.plot([sc_mid - 1.55, sc_mid + 1.55], [-1.5, -1.5],
            color=figstyle.HAIRLINE, lw=1.4)
    ax.plot([ex_mid - 1.35, ex_mid + 1.35], [-1.5, -1.5],
            color=figstyle.HAIRLINE, lw=1.4)
    ax.plot([x_div, x_div], [-1.35, n_r - 0.55], color=figstyle.HAIRLINE,
            lw=1.1, ls=(0, (4, 3)), zorder=0)

    # column headers
    for j, d in enumerate(DIMS):
        ax.text(xpos[j], -0.78, d, ha="center", va="center", fontsize=11.5,
                color=figstyle.BODY, fontweight="bold", linespacing=1.05)
    ax.text(call_x, -0.78, "Call", ha="left", va="center", fontsize=11.5,
            color=figstyle.BODY, fontweight="bold")

    for i, (gene, call, ccol, scores, ev) in enumerate(TARGETS):
        ax.text(gene_x, i, gene, ha="right", va="center", fontsize=16,
                color=figstyle.INK, fontweight="bold", family=figstyle.DISP)
        for j, s in enumerate(scores):
            ax.scatter(xpos[j], i, s=_bubble_size(s), c=[CMAP(s)],
                       edgecolors="white", linewidths=1.2, zorder=3)
        ax.text(call_x, i - 0.17, call, ha="left", va="center", fontsize=12.5,
                color=ccol, fontweight="bold")
        ax.text(call_x, i + 0.2, ev, ha="left", va="center", fontsize=8.8,
                color=figstyle.MUTED)

    # recessive gridlines
    for j in range(n_c):
        ax.axvline(xpos[j], color="white", alpha=0.05, lw=0.8, zorder=0)
    for i in range(n_r):
        ax.axhline(i, color="white", alpha=0.05, lw=0.8, zorder=0)

    ax.set_xticks([]); ax.set_yticks([])
    # bubble size/colour legend with numeric anchors
    ly = n_r + 0.05
    ax.text(gene_x, ly, "evidence", ha="right", va="center", fontsize=10,
            color=figstyle.MUTED)
    for k, s in enumerate([0.25, 0.6, 1.0]):
        lx = 0.15 + k * 1.02
        ax.scatter(lx, ly, s=_bubble_size(s), c=[CMAP(s)], edgecolors="white", linewidths=1.2)
        ax.text(lx, ly + 0.42, f"{s:.2f}", ha="center", va="center", fontsize=8.5,
                color=figstyle.MUTED)
    ax.text(0.15 + 2 * 1.02 + 0.7, ly, "weak to strong  (0–1 summary score)",
            ha="left", va="center", fontsize=10, color=figstyle.MUTED)

    figstyle.title_block(
        fig,
        "A convergent-evidence shortlist of candidate T-cell brakes",
        [
            "Positive direction = a candidate brake hypothesis — an 8-hour transcriptional signature, not a functional assay.",
            "The positive quadrant is not brake-enriched (Mann–Whitney p = 0.70, n = 2 donors) — a shortlist to test, not a validated set.",
            "Scored 0–1 from the CD4 screen and Open Targets · ChEMBL · ClinicalTrials.gov — a curated summary, not a fitted model.",
        ],
        x=0.038,
        y=0.975,
        title_size=18,
        sub_size=11,
        dy=0.029,
    )
    fig.subplots_adjust(left=0.115, right=0.995, top=0.80, bottom=0.05)
    fig.savefig(out_png, dpi=200, facecolor=figstyle.BG)
    fig.savefig(out_svg, facecolor=figstyle.BG)
    figstyle.plt.close(fig)
    print("wrote", out_png, "+", out_svg)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", default="../deliverables/figures/target_matrix.png")
    ap.add_argument("--svg", default="../deliverables/figures/target_matrix.svg")
    a = ap.parse_args()
    build(a.png, a.svg)
