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
    # derive limits from the data so no observation is clipped
    lim = float(max(abs(d1).max(), abs(d2).max())) * 1.05
    # per-gene label offsets (dx, dy points, ha) to keep the crowded clusters legible
    OFF = {"LAT2": (10, 3, "left"), "SMAD3": (-11, 7, "right"), "UBASH3A": (-12, -2, "right"),
           "CD5": (11, 5, "left"), "DGKA": (9, -13, "left"), "CBLB": (11, 3, "left"),
           "ZAP70": (9, -3, "left"), "LCP2": (-9, -4, "right"), "CD3D": (-9, 7, "right"),
           "ITK": (10, 4, "left")}
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
        label_set = genes if col == AMBER else ["ZAP70", "LCP2", "CD3D", "ITK"]
        for g in genes:
            if g in by and g in label_set:
                dx, dy, ha = OFF.get(g, (7, 4, "left"))
                ax.annotate(g, by[g], textcoords="offset points", xytext=(dx, dy), ha=ha,
                            fontsize=10.5, fontweight="bold", color=edge, zorder=5)
        if col == TEAL:
            ax.annotate("(TCR module)", (-0.29 * lim, -0.60 * lim), fontsize=10,
                        color=TEAL_DK, style="italic", zorder=5)
    ax.text(0.36 * lim, 0.93 * lim, "replicates positive\n(candidate hypothesis)",
            color=AMBER_DK, fontsize=11, fontweight="bold", ha="left", va="top")
    ax.text(-0.96 * lim, -0.86 * lim, "replicates negative\n(TCR machinery)",
            color=TEAL_DK, fontsize=11, fontweight="bold", ha="left", va="top")
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("Donor 1 · direction of effect", fontsize=12.5, color=INK)
    ax.set_ylabel("Donor 2 · direction of effect", fontsize=12.5, color=INK)
    _style(ax)
    fig.suptitle("Which candidates replicate across donors?", x=0.06, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.06, 0.925, "CD5 and DGKA replicate in both donors; CBLB, SMAD3, UBASH3A and LAT2 are driven by one donor (n = 2).",
             fontsize=10.6, color=MUTED)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.88, bottom=0.09)
    fig.savefig(out, dpi=210, facecolor=SURFACE); plt.close(fig); print("wrote", out)


def dist_plot(df: pd.DataFrame, out: str) -> None:
    v = df["direction_score"].dropna().to_numpy()
    xlo, xhi = -0.9, 0.6
    tau = 0.05  # DIRECTION_TAU — |score| <= tau is treated as no clear direction
    fig, ax = plt.subplots(figsize=(12.2, 5.4), dpi=210)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    bins = np.linspace(xlo, xhi, 120)
    # colour marks the SIGN of the shift (descriptive), not a proven function
    ax.hist(v[v <= 0], bins=bins, color=TEAL, alpha=0.5, edgecolor="none")
    ax.hist(v[v > 0], bins=bins, color=AMBER, alpha=0.55, edgecolor="none")
    # neutral dead-band: most knockdowns have no clear direction
    ax.axvspan(-tau, tau, color="#8a8880", alpha=0.16, zorder=0)
    ax.axvline(0, color=INK2, lw=1.2)

    trans = ax.get_xaxis_transform()  # x in data, y in axes fraction
    by = dict(zip(df["perturbation"], df["direction_score"]))
    # gene guides live in axes-fraction height so they cannot be mistaken for bars
    for g, col, yo in (("ZAP70", TEAL_DK, 0.93), ("CD3D", TEAL_DK, 0.79),
                       ("CD5", AMBER_DK, 0.93), ("DGKA", AMBER_DK, 0.79), ("CBLB", AMBER_DK, 0.65)):
        if g in by:
            x = by[g]
            ax.plot([x, x], [0, yo - 0.055], transform=trans, color=col, lw=0.9,
                    ls=(0, (3, 2)), alpha=0.5, zorder=2)
            ax.text(x, yo, g, transform=trans, ha="center", va="bottom",
                    fontsize=10.5, fontweight="bold", color=col, zorder=5)

    ax.text(-0.5, 0.90, "negative direction\n(TCR machinery)", transform=trans,
            color=TEAL_DK, fontsize=12, fontweight="bold", ha="center", va="top", linespacing=1.05)
    ax.text(0.34, 0.90, "positive direction\n(candidate hypotheses)", transform=trans,
            color=AMBER_DK, fontsize=12, fontweight="bold", ha="center", va="top", linespacing=1.05)
    ax.text(0.0, 0.55, "neutral\n|score| ≤ 0.05", transform=trans, ha="center", va="center",
            fontsize=8.6, color=INK2, linespacing=1.05,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#e2e1d8", lw=0.8, alpha=0.92))

    n_lo = int((v < xlo).sum()); n_hi = int((v > xhi).sum())
    ax.text(0.995, 0.03, f"+{n_hi} knockdowns beyond {xhi:+.1f} · {n_lo} beyond {xlo:+.1f}  (off-axis)",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=9, color=MUTED)

    ax.set_xlim(xlo, xhi)
    ax.set_xlabel("Direction of effect  ·  effector − dysfunction (vs control)", fontsize=12.5, color=INK)
    ax.set_ylabel("knockdowns per bin", fontsize=12.5, color=INK)
    _style(ax)
    fig.suptitle(f"The signed axis splits {len(v):,} knockdowns", x=0.055, y=0.965, ha="left",
                 fontsize=17, fontweight="bold", color=INK)
    fig.text(0.055, 0.90,
             "Most sit near zero; the negative tail is enriched for TCR machinery, the positive tail is the candidate hypothesis space.",
             fontsize=11, color=MUTED)
    fig.text(0.055, 0.855,
             "The positive side is not brake-enriched (Mann–Whitney p = 0.70) — a hypothesis space, not a validated set.",
             fontsize=11, color=MUTED)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.785, bottom=0.13)
    fig.savefig(out, dpi=210, facecolor=SURFACE); plt.close(fig); print("wrote", out)


if __name__ == "__main__":
    df = pd.read_csv("outputs_gladstone/ranked_perturbations.csv")
    donor_plot(df, "../deliverables/figures/donor_consistency.png")
    dist_plot(df, "../deliverables/figures/direction_dist.png")
