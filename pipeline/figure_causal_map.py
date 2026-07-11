"""figure_causal_map.py — the hero figure: a genome-scale SIGNED causal map.

X = causal effect size (E-distance, magnitude).
Y = signed direction-of-effect (effector - dysfunction program vs control).

The point: the magnitude leaderboard alone cannot tell a drug target from the
cell's own machinery. Adding the sign splits the map — the largest effects
(TCR module) sit far-right but strongly NEGATIVE (knockdown cripples the cell =
required machinery), while the therapeutically useful signal lives ABOVE zero
(knockdown enhances the effector program = candidate brakes).

Reads the merged ``ranked_perturbations.csv`` (needs ``direction_score``).
Renders a high-DPI PNG + an SVG. Design follows the dataviz skill: diverging
sign encoding (warm brakes / cool machinery / neutral bulk), Y-position carries
the sign, selective direct labels, recessive chrome.
"""
from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

# --- palette (validated: teal<->amber CVD dE 60.8) ----------------------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8880"
BULK = "#cdccc4"
TEAL = "#0d9488"  # required machinery (cool)
TEAL_DK = "#0b6b62"
AMBER = "#d97a12"  # candidate brakes (warm)
AMBER_DK = "#a85c08"
GRID = "#ecebe5"

# TCR proximal-signaling machinery (positive controls; expected far-right, -Y).
TCR_MODULE = ["ZAP70", "LCP2", "CD3E", "CD3G", "PLCG1", "LAT", "VAV1", "CD3D", "CD247", "ITK"]
# Featured, mechanistically-coherent brake candidates (KD enhances effector).
# Marker shape encodes donor consistency (read from the CSV): consistent brakes
# (CD5, DGKA) are circles; higher-magnitude but donor-split candidates
# (SMAD3, LAT2, CBLB — one of two donors drives them) are diamonds.
BRAKES = ["SMAD3", "LAT2", "CBLB", "CD5", "DGKA"]

# Manual label offsets (points) to avoid collisions — (dx, dy, ha).
LABEL_OFFSETS: dict[str, tuple[float, float, str]] = {
    "ZAP70": (6, -2, "left"),
    "LCP2": (6, 6, "left"),
    "CD3E": (0, -16, "center"),
    "CD3G": (2, 10, "left"),
    "PLCG1": (-6, -15, "right"),
    "LAT": (0, -17, "center"),
    "VAV1": (-4, 9, "right"),
    "CD3D": (-6, -16, "right"),
    "CD247": (8, -12, "left"),
    "ITK": (-8, -12, "right"),
    "SMAD3": (8, 8, "left"),
    "LAT2": (8, 4, "left"),
    "CBLB": (-8, 10, "right"),
    "CD5": (8, 8, "left"),
    "DGKA": (-8, -12, "right"),
    "UBASH3A": (8, -10, "left"),
    "CDKN1B": (-8, 8, "right"),
}


def _pt(ax, x, y, color, label, off):
    dx, dy, ha = off
    ax.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(dx, dy),
        ha=ha,
        va="center",
        fontsize=10.5,
        fontweight="bold",
        color=color,
        zorder=8,
        arrowprops=dict(arrowstyle="-", color=color, lw=0.8, alpha=0.55,
                        shrinkA=1, shrinkB=3),
    )


def build(ranked_csv: str, out_png: str, out_svg: str) -> None:
    df = pd.read_csv(ranked_csv)
    df = df.dropna(subset=["e_distance", "direction_score"]).copy()
    by = {str(r.perturbation): (float(r.e_distance), float(r.direction_score))
          for r in df.itertuples()}
    agreed = {str(r.perturbation): bool(r.direction_sign_agreement) for r in df.itertuples()}

    top15 = df.sort_values("e_distance", ascending=False).head(15)
    n_neg = int((top15.direction_score < 0).sum())

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "svg.fonttype": "none",
    })
    fig, ax = plt.subplots(figsize=(12.2, 7.6), dpi=210)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    xmax = float(df.e_distance.max()) * 1.06
    ymin, ymax = -0.92, 0.72
    ax.set_xlim(-1.5, xmax)
    ax.set_ylim(ymin, ymax)

    # quadrant wash (very subtle) above/below the sign line
    ax.axhspan(0, ymax, xmin=0, xmax=1, color=AMBER, alpha=0.045, zorder=0)
    ax.axhspan(ymin, 0, xmin=0, xmax=1, color=TEAL, alpha=0.05, zorder=0)
    ax.axhline(0, color=INK2, lw=1.1, zorder=2)

    # bulk cloud
    ax.scatter(df.e_distance, df.direction_score, s=7, c=BULK, alpha=0.32,
               linewidths=0, zorder=1, rasterized=True)

    # highlights — marker shape carries donor consistency (o = both donors agree,
    # D = donor-split at n=2). Machinery is uniformly donor-consistent; the brake
    # side is where n=2 shows its limits, so we make that visible rather than hide it.
    for genes, color, edge in ((TCR_MODULE, TEAL, TEAL_DK), (BRAKES, AMBER, AMBER_DK)):
        for g in genes:
            if g not in by:
                continue
            x, y = by[g]
            mk = "o" if agreed.get(g, True) else "D"
            sz = 105 if mk == "o" else 82
            ax.scatter([x], [y], s=sz, marker=mk, c=color, edgecolors="white",
                       linewidths=1.4, zorder=6, alpha=0.97)
            ax.scatter([x], [y], s=sz, marker=mk, facecolors="none", edgecolors=edge,
                       linewidths=0.7, zorder=7)
            _pt(ax, x, y, edge, g, LABEL_OFFSETS.get(g, (6, 6, "left")))

    from matplotlib.lines import Line2D
    leg = ax.legend(
        handles=[
            Line2D([0], [0], marker="o", ls="", mfc=MUTED, mec="white", ms=9,
                   label="consistent across both donors"),
            Line2D([0], [0], marker="D", ls="", mfc=MUTED, mec="white", ms=8,
                   label="donor-split (n=2 — confirm at full 4-donor cohort)"),
        ],
        loc="lower left", fontsize=9.5, frameon=True, framealpha=0.96,
        edgecolor=GRID, handletextpad=0.5, borderpad=0.7,
    )
    leg.set_zorder(9)

    # quadrant captions
    ax.text(xmax * 0.985, 0.63,
            "knockdown ENHANCES the effector program",
            ha="right", va="center", fontsize=12, color=AMBER_DK, fontweight="bold")
    ax.text(xmax * 0.985, 0.555, "candidate brakes — the drug-target quadrant",
            ha="right", va="center", fontsize=11, color=AMBER_DK, style="italic")
    ax.text(xmax * 0.985, -0.80,
            "knockdown IMPAIRS the effector program",
            ha="right", va="center", fontsize=12, color=TEAL_DK, fontweight="bold")
    ax.text(xmax * 0.985, -0.865, "required machinery — not druggable",
            ha="right", va="center", fontsize=11, color=TEAL_DK, style="italic")

    # headline-stat callout box (upper-left)
    box = FancyBboxPatch((0.022, 0.80), 0.40, 0.155, transform=ax.transAxes,
                         boxstyle="round,pad=0.012,rounding_size=0.02",
                         fc="white", ec=GRID, lw=1.2, zorder=9)
    ax.add_patch(box)
    ax.text(0.042, 0.905, f"{n_neg} of the 15 largest-effect knockdowns",
            transform=ax.transAxes, fontsize=12.5, fontweight="bold", color=INK, zorder=10)
    ax.text(0.042, 0.848,
            "impair effector function — magnitude alone\nwould nominate the cell's own machinery.",
            transform=ax.transAxes, fontsize=11, color=INK2, zorder=10, linespacing=1.25)

    # axes chrome
    ax.set_xlabel("Causal effect size   ·   E-distance (power-equalized)",
                  fontsize=12.5, color=INK, labelpad=8)
    ax.set_ylabel("Direction of effect   ·   effector − dysfunction  (vs control)",
                  fontsize=12.5, color=INK, labelpad=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelsize=10.5)
    ax.grid(axis="both", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)

    # title block
    fig.text(0.062, 0.975, "A genome-scale signed causal map of CD4⁺ T-cell function",
             fontsize=17.5, fontweight="bold", color=INK, va="top")
    fig.text(0.062, 0.936,
             "2,638,736 primary human CD4⁺ T cells · 12,449 CRISPRi knockdowns · "
             "Gladstone Perturb-seq · built with Claude Science",
             fontsize=11.5, color=MUTED, va="top")

    fig.subplots_adjust(left=0.075, right=0.975, top=0.885, bottom=0.092)
    fig.savefig(out_png, dpi=210, facecolor=SURFACE)
    fig.savefig(out_svg, facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {out_png} + {out_svg}  ({n_neg}/15 top-effects negative)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranked", default="outputs_gladstone/ranked_perturbations.csv")
    ap.add_argument("--png", default="../deliverables/figures/causal_map.png")
    ap.add_argument("--svg", default="../deliverables/figures/causal_map.svg")
    a = ap.parse_args()
    build(a.ranked, a.png, a.svg)


if __name__ == "__main__":
    main()
