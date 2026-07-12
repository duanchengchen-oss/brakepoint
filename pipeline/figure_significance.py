"""figure_significance.py — the "significance wall": why we rank by effect size, not p-value.

At 2.6 M cells, a permutation q<0.05 is near-universal — 97.5% of tested knockdowns
clear it, and 9,802 pile at the exact permutation p-floor. Significance (y) therefore
cannot rank the screen; only causal effect size (x, E-distance) spreads the biology.
This is the honest, data-driven argument for effect-size ranking + the signed axis.
Output: deliverables/figures/significance_wall.png (+ .svg)
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

SURFACE = "#fcfcfb"; INK = "#0b1220"; INK2 = "#39424e"; MUTED = "#8a8880"
TEAL = "#0d9488"; TEAL_DK = "#0b6b62"; AMBER = "#d97a12"; AMBER_DK = "#a85c08"
BULK = "#cdccc4"; GRID = "#ecebe5"

TCR = ["ZAP70", "LCP2", "CD3E", "CD3G", "PLCG1", "LAT", "VAV1", "CD3D", "CD247", "ITK"]
CAND = ["CBLB", "CD5", "DGKA", "UBASH3A", "SMAD3"]
LABEL_MACH = ["ZAP70", "CD3E", "LCP2", "LAT"]


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelsize=10.5)
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True)


def significance_wall(df: pd.DataFrame, out: str) -> None:
    d = df[df["n_cells"] >= 30].copy()
    d = d.dropna(subset=["e_distance", "e_qval"])
    q = d["e_qval"].clip(lower=1e-6)
    y = -np.log10(q)
    x = d["e_distance"].to_numpy()
    n = len(d)
    n_sig = int((d["e_qval"] < 0.05).sum())
    pct_sig = 100 * n_sig / n
    floor = q.min()
    n_floor = int((q <= floor + 1e-9).sum())
    by = {g: (float(row.e_distance), float(-np.log10(max(row.e_qval, 1e-6))))
          for g, row in d.set_index("perturbation").iterrows()}

    fig, ax = plt.subplots(figsize=(12.4, 7.0), dpi=210)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)

    ymax = float(y.max()) * 1.16
    sig_line = -np.log10(0.05)
    # shade the "everything is significant" band
    ax.axhspan(sig_line, ymax, color=TEAL, alpha=0.045)
    ax.axhline(sig_line, color="#b9b8ad", lw=1.1, ls="--", zorder=2)
    ax.text(74, sig_line + 0.05, "q = 0.05", color=MUTED, fontsize=10, ha="right", va="bottom")

    y_ceil = float(y.max())
    mask = ~d["perturbation"].isin(TCR + CAND)
    ax.scatter(x[mask.to_numpy()], y[mask.to_numpy()], s=7, c=BULK, alpha=0.28, lw=0,
               zorder=3, rasterized=True)
    for genes, col in ((TCR, TEAL), (CAND, AMBER)):
        xs = [by[g][0] for g in genes if g in by]; ys = [by[g][1] for g in genes if g in by]
        ax.scatter(xs, ys, s=95, c=col, edgecolors="white", linewidths=1.4, zorder=5)

    # ceiling headline (sits just above the band; no arrow needed)
    ax.text(24, ymax * 0.965,
            f"significance ceiling — {pct_sig:.1f}% of tested knockdowns clear q<0.05  ·  {n_floor:,} at the permutation floor",
            fontsize=11.5, color=INK2, ha="center", fontweight="bold")
    # candidate-brake cluster callout (low E, on the ceiling)
    ax.annotate("candidate brakes\nmodest-to-moderate effect · signed positive\nCBLB · CD5 · DGKA · SMAD3 · UBASH3A",
                xy=(6.2, y_ceil), xytext=(16, 2.28), fontsize=11, color=AMBER_DK,
                fontweight="bold", ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.5", fc="#fdf3e7", ec=AMBER, lw=1.2),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.4))
    # TCR machinery callout (high E)
    ax.annotate("TCR machinery\nthe largest effects\nZAP70 · CD3E · LAT · LCP2 …",
                xy=(60, y_ceil), xytext=(43, 1.62), fontsize=11, color=TEAL_DK,
                fontweight="bold", ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.5", fc="#e8f4f2", ec=TEAL, lw=1.2),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.4))
    # the useful axis + the takeaway
    ax.annotate("larger causal effect  →", xy=(58, 0.42), fontsize=12.5, color=INK,
                fontweight="bold", ha="center", style="italic")
    ax.text(3, 0.78,
            "p-value can't rank these — effect size can.\nThe signed axis then tells brake from machinery.",
            fontsize=12, color=INK2, ha="left",
            bbox=dict(boxstyle="round,pad=0.55", fc="white", ec="#e2e1d8", lw=1))

    ax.set_xlim(-1.5, 76); ax.set_ylim(0, ymax)
    ax.set_xlabel("Causal effect size  ·  E-distance (power-equalized)", fontsize=12.5, color=INK)
    ax.set_ylabel("Statistical significance  ·  −log₁₀(q)", fontsize=12.5, color=INK)
    _style(ax)
    fig.suptitle("Why we rank by effect size, not p-value", x=0.065, y=0.97, ha="left",
                 fontsize=18, fontweight="bold", color=INK)
    fig.text(0.065, 0.905,
             f"{n:,} tested knockdowns · E-distance on 2.44 M post-QC CD4⁺ T cells. Teal = TCR machinery, amber = candidate brakes.",
             fontsize=11, color=MUTED)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.80, bottom=0.11)
    fig.savefig(out, dpi=210, facecolor=SURFACE)
    fig.savefig(out.replace(".png", ".svg"), facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {out}  (n={n}, sig={pct_sig:.1f}%, floor={n_floor})")


if __name__ == "__main__":
    df = pd.read_csv("outputs_gladstone/ranked_perturbations.csv")
    significance_wall(df, "../deliverables/figures/significance_wall.png")
