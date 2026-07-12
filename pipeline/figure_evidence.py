"""figure_evidence.py — supporting target-discovery plots (dot/density).

1) donor_consistency.png — per-donor direction (D1 vs D2). Robust brakes sit in
   the both-positive corner; machinery in the both-negative corner; donor-split
   candidates off the diagonal. This is the honest read on which nominations hold.
2) direction_dist.png — distribution of the signed direction score with the
   machinery tail (−) and brake tail (+) marked.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

SURFACE = "#fcfcfb"; INK = "#0b1220"; INK2 = "#39424e"; MUTED = "#8a8880"
TEAL = "#0d9488"; TEAL_DK = "#0b6b62"; AMBER = "#d97a12"; AMBER_DK = "#a85c08"; BULK = "#cdccc4"; GRID = "#ecebe5"

TCR = ["ZAP70", "LCP2", "CD3E", "CD3G", "PLCG1", "LAT", "VAV1", "CD3D", "CD247", "ITK"]
CAND = ["CBLB", "CD5", "DGKA", "UBASH3A", "SMAD3", "LAT2"]


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelsize=10.5)
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True)


def donor_plot(df: pd.DataFrame, out: str) -> None:
    d = df.dropna(subset=["direction_per_donor"]).copy()
    pd2 = d["direction_per_donor"].astype(str).str.split(";", expand=True)
    d = d[pd2[1].notna()]  # need 2 donors
    d1 = pd2[0].astype(float)[d.index]; d2 = pd2[1].astype(float)[d.index]
    by = {g: (float(d1[i]), float(d2[i])) for i, g in zip(d.index, d["perturbation"])}
    lim = 1.15
    fig, ax = plt.subplots(figsize=(8.6, 8.0), dpi=210)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    ax.axhspan(0, lim, xmin=0.5, xmax=1, color=AMBER, alpha=0.05)
    ax.axhspan(-lim, 0, xmin=0, xmax=0.5, color=TEAL, alpha=0.06)
    ax.plot([-lim, lim], [-lim, lim], color="#c3c2b7", lw=1, ls="--", zorder=1)
    ax.axhline(0, color="#d7d6cf", lw=1); ax.axvline(0, color="#d7d6cf", lw=1)
    mask = ~d["perturbation"].isin(TCR + CAND)
    ax.scatter(d1[mask], d2[mask], s=6, c=BULK, alpha=0.3, lw=0, zorder=2, rasterized=True)
    for genes, col, edge in ((TCR, TEAL, TEAL_DK), (CAND, AMBER, AMBER_DK)):
        xs = [by[g][0] for g in genes if g in by]; ys = [by[g][1] for g in genes if g in by]
        ax.scatter(xs, ys, s=90, c=col, edgecolors="white", linewidths=1.3, zorder=4)
        for g in genes:
            if g in by:
                ax.annotate(g, by[g], textcoords="offset points", xytext=(7, 4), fontsize=10,
                            fontweight="bold", color=edge, zorder=5)
    ax.text(0.62, 1.02, "consistent brake\n(both donors +)", color=AMBER_DK, fontsize=11, fontweight="bold", ha="left")
    ax.text(-1.08, -1.0, "consistent machinery\n(both donors −)", color=TEAL_DK, fontsize=11, fontweight="bold", ha="left")
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xlabel("Donor 1 · direction of effect", fontsize=12.5, color=INK)
    ax.set_ylabel("Donor 2 · direction of effect", fontsize=12.5, color=INK)
    _style(ax)
    fig.suptitle("Which brakes hold up across donors?", x=0.06, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.06, 0.925, "CD5 and DGKA are donor-consistent; CBLB / SMAD3 / LAT2 are driven by one donor (n=2).",
             fontsize=11, color=MUTED)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.88, bottom=0.09)
    fig.savefig(out, dpi=210, facecolor=SURFACE); plt.close(fig); print("wrote", out)


def dist_plot(df: pd.DataFrame, out: str) -> None:
    v = df["direction_score"].dropna().to_numpy()
    fig, ax = plt.subplots(figsize=(12.2, 5.4), dpi=210)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    bins = np.linspace(-0.9, 0.6, 120)
    ax.hist(v[v <= 0], bins=bins, color=TEAL, alpha=0.55, edgecolor="none")
    ax.hist(v[v > 0], bins=bins, color=AMBER, alpha=0.6, edgecolor="none")
    ax.axvline(0, color=INK2, lw=1.2)
    by = dict(zip(df["perturbation"], df["direction_score"]))
    ymax = ax.get_ylim()[1]
    for g, col, yo in (("ZAP70", TEAL_DK, 0.82), ("CD3D", TEAL_DK, 0.62), ("CD5", AMBER_DK, 0.82),
                       ("DGKA", AMBER_DK, 0.62), ("CBLB", AMBER_DK, 0.42)):
        if g in by:
            x = by[g]
            ax.annotate(g, (x, ymax * yo), textcoords="offset points", xytext=(0, 0), ha="center",
                        fontsize=10.5, fontweight="bold", color=col)
            ax.plot([x, x], [0, ymax * (yo - 0.06)], color=col, lw=0.8, alpha=0.5)
    ax.text(-0.55, ymax * 0.9, "machinery\n(knockdown impairs)", color=TEAL_DK, fontsize=12, fontweight="bold", ha="center")
    ax.text(0.33, ymax * 0.9, "brakes\n(knockdown enhances)", color=AMBER_DK, fontsize=12, fontweight="bold", ha="center")
    ax.set_xlim(-0.9, 0.6)
    ax.set_xlabel("Direction of effect  ·  effector − dysfunction (vs control)", fontsize=12.5, color=INK)
    ax.set_ylabel("knockdowns", fontsize=12.5, color=INK)
    _style(ax)
    fig.suptitle("The signed axis splits 12,449 knockdowns", x=0.055, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.055, 0.925, "Most sit near zero; the negative tail is required machinery, the positive tail is the brake search space.",
             fontsize=11, color=MUTED)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.86, bottom=0.13)
    fig.savefig(out, dpi=210, facecolor=SURFACE); plt.close(fig); print("wrote", out)


if __name__ == "__main__":
    df = pd.read_csv("outputs_gladstone/ranked_perturbations.csv")
    donor_plot(df, "../deliverables/figures/donor_consistency.png")
    dist_plot(df, "../deliverables/figures/direction_dist.png")
