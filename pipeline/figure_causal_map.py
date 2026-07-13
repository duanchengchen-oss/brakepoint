"""figure_causal_map.py — the hero figure: a genome-scale SIGNED causal map.

X = causal effect size (E-distance, magnitude).
Y = signed direction-of-effect (effector - dysfunction program vs control).

The point: the magnitude leaderboard alone cannot tell a drug target from the
cell's own machinery. Adding the sign splits the map — the largest effects
(TCR module) sit far-right but strongly NEGATIVE (knockdown cripples the cell =
required machinery), while the candidate-brake signal lives ABOVE zero
(knockdown shifts cells toward the effector program). The positive quadrant is a
hypothesis space, not a validated set — known brakes are not enriched there
(Mann-Whitney p = 0.70) and 3 of the 5 highlighted candidates are donor-split.

Reads the merged ``ranked_perturbations.csv`` (needs ``direction_score``).
Renders a high-DPI PNG + an SVG. Design follows the dataviz skill: diverging
sign encoding (warm brakes / cool machinery / neutral bulk), Y-position carries
the sign, selective direct labels, recessive chrome.
"""
from __future__ import annotations

import argparse

import pandas as pd  # noqa: E402

import figstyle

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
    "CBLB": (0, 15, "center"),
    "CD5": (11, -7, "left"),
    "DGKA": (9, -13, "left"),
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
    figstyle.apply_rc()
    df = pd.read_csv(ranked_csv)
    df = df.dropna(subset=["e_distance", "direction_score"]).copy()
    by = {str(r.perturbation): (float(r.e_distance), float(r.direction_score))
          for r in df.itertuples()}
    agreed = {str(r.perturbation): bool(r.direction_sign_agreement) for r in df.itertuples()}

    top15 = df.sort_values("e_distance", ascending=False).head(15)
    n_neg = int((top15.direction_score < 0).sum())
    n_split = sum(1 for g in BRAKES if g in agreed and not agreed[g])

    fig, ax = figstyle.dark_figure((12.2, 7.6), dpi=200)

    xmax = float(df.e_distance.max()) * 1.06
    # derive y-limits from the plotted data (never clip a real observation)
    dmin, dmax = float(df.direction_score.min()), float(df.direction_score.max())
    ymin = min(-0.92, dmin * 1.06)
    ymax = max(0.75, dmax * 1.07)
    ax.set_xlim(-1.5, xmax)
    ax.set_ylim(ymin, ymax)

    # quadrant wash (very subtle) above/below the sign line
    ax.axhspan(0, ymax, xmin=0, xmax=1, color=figstyle.AMBER_MID,
               alpha=figstyle.AMBER_WASH, zorder=0)
    ax.axhspan(ymin, 0, xmin=0, xmax=1, color=figstyle.TEAL_MID,
               alpha=figstyle.TEAL_WASH, zorder=0)
    ax.axhline(0, color=figstyle.HAIRLINE, lw=1.1, zorder=2)

    # bulk cloud
    figstyle.bulk_cloud(ax, df.e_distance, df.direction_score, size=7,
                        alpha=0.32, zorder=1)

    # highlights — marker shape carries donor consistency (o = both donors agree,
    # D = donor-split at n=2). Machinery is uniformly donor-consistent; the brake
    # side is where n=2 shows its limits, so we make that visible rather than hide it.
    for genes, fill, label_color in (
        (TCR_MODULE, figstyle.TEAL_MID, figstyle.TEAL),
        (BRAKES, figstyle.AMBER_MID, figstyle.AMBER),
    ):
        for g in genes:
            if g not in by:
                continue
            x, y = by[g]
            mk = "o" if agreed.get(g, True) else "D"
            sz = 105 if mk == "o" else 82
            figstyle.marker(ax, [x], [y], fill, size=sz, mk=mk, lw=2.2,
                            zorder=6, alpha=0.97)
            _pt(ax, x, y, label_color, g, LABEL_OFFSETS.get(g, (6, 6, "left")))

    from matplotlib.lines import Line2D
    leg = ax.legend(
        handles=[
            Line2D([0], [0], marker="o", ls="", mfc=figstyle.BULK, mec="white", mew=1.5, ms=9,
                   label="consistent across both donors"),
            Line2D([0], [0], marker="D", ls="", mfc=figstyle.BULK, mec="white", mew=1.5, ms=8,
                   label="donor-split (n=2 — confirm at full 4-donor cohort)"),
        ],
        loc="lower left", fontsize=9.5, frameon=True, framealpha=0.88,
        facecolor=figstyle.BG_PANEL, edgecolor=figstyle.HAIRLINE,
        handletextpad=0.5, borderpad=0.7,
    )
    for text in leg.get_texts():
        text.set_color(figstyle.BODY)
    leg.set_zorder(9)

    # quadrant captions (axes-fraction coords so they never collide with data or
    # shift when the limits change)
    ax.text(0.985, 0.965, "knockdown ENHANCES the effector program",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=12, color=figstyle.AMBER, fontweight="bold")
    ax.text(0.985, 0.918,
            "candidate brakes — a hypothesis space, not brake-enriched (Mann–Whitney p = 0.70)",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10.5, color=figstyle.AMBER, style="italic")
    ax.text(0.985, 0.879,
            f"{n_split} of {len(BRAKES)} highlighted candidates are donor-split (n = 2)",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10.5, color=figstyle.AMBER, style="italic")
    ax.text(0.985, 0.058, "knockdown IMPAIRS the effector program",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=12, color=figstyle.TEAL, fontweight="bold")
    ax.text(0.985, 0.015, "required TCR machinery — inhibition opposes the goal",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=10.5, color=figstyle.TEAL, style="italic")

    # headline-stat callout box (upper-left)
    figstyle.panel_box(ax, 0.022, 0.80, 0.40, 0.155, zorder=9)
    ax.text(0.042, 0.905, f"{n_neg} of the 15 largest-effect knockdowns",
            transform=ax.transAxes, fontsize=12.5, fontweight="bold",
            color=figstyle.INK, zorder=10)
    ax.text(0.042, 0.848,
            "impair effector function — magnitude alone\nwould nominate the cell's own machinery.",
            transform=ax.transAxes, fontsize=11, color=figstyle.BODY,
            zorder=10, linespacing=1.25)

    # axes chrome
    ax.set_xlabel("Causal effect size   ·   E-distance (power-equalized)",
                  fontsize=12.5, color=figstyle.BODY, labelpad=8)
    ax.set_ylabel("Direction of effect   ·   effector − dysfunction  (vs control)",
                  fontsize=12.5, color=figstyle.BODY, labelpad=8)

    # title block
    figstyle.title_block(
        fig,
        "A genome-scale signed causal map of CD4⁺ T-cell function",
        [f"{len(df):,} CRISPRi knockdowns with a measurable causal effect · "
         "E-distance on 2.44 M post-QC CD4⁺ T cells",
         "Gladstone Perturb-seq · built with Claude Science"],
        x=0.062,
        y=0.975,
        title_size=17.5,
        sub_size=11,
        dy=0.038,
    )

    fig.subplots_adjust(left=0.075, right=0.975, top=0.858, bottom=0.092)
    fig.savefig(out_png, dpi=200, facecolor=figstyle.BG)
    fig.savefig(out_svg, facecolor=figstyle.BG)
    figstyle.plt.close(fig)
    print(f"wrote {out_png} + {out_svg}  "
          f"(n_neg={n_neg}/15, donor-split={n_split}/{len(BRAKES)})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranked", default="outputs_gladstone/ranked_perturbations.csv")
    ap.add_argument("--png", default="../deliverables/figures/causal_map.png")
    ap.add_argument("--svg", default="../deliverables/figures/causal_map.svg")
    a = ap.parse_args()
    build(a.ranked, a.png, a.svg)


if __name__ == "__main__":
    main()
