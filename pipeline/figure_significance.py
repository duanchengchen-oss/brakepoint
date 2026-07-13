"""figure_significance.py — the "significance wall": why we rank by effect size, not p-value.

At 2.6 M cells, a permutation q<0.05 is near-universal — 97.5% of tested knockdowns
clear it, and 9,802 pile at the exact permutation p-floor. Significance (y) therefore
cannot rank the screen; only causal effect size (x, E-distance) spreads the biology.
This is the honest, data-driven argument for effect-size ranking + the signed axis.
Output: deliverables/figures/significance_wall.png (+ .svg)
"""
from __future__ import annotations

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import figstyle

TCR = ["ZAP70", "LCP2", "CD3E", "CD3G", "PLCG1", "LAT", "VAV1", "CD3D", "CD247", "ITK"]
CAND = ["CBLB", "CD5", "DGKA", "UBASH3A", "SMAD3"]
LABEL_MACH = ["ZAP70", "CD3E", "LCP2", "LAT"]

def significance_wall(df: pd.DataFrame, out: str) -> None:
    figstyle.apply_rc()
    d = df[df["n_cells"] >= 30].copy()
    d = d.dropna(subset=["e_distance", "e_qval"])
    q = d["e_qval"].clip(lower=1e-6)
    y = -np.log10(q)
    x = d["e_distance"].to_numpy()
    n = len(d)
    n_sig = int((d["e_qval"] < 0.05).sum())
    pct_sig = 100 * n_sig / n
    # the "floor" is a permutation p-value floor (p = 1/(n_perm+1)); the y-axis is
    # the BH-adjusted q, so compute the pile-up from the underlying p to be precise.
    p_floor = float(d["e_pval"].min())
    n_floor = int(np.isclose(d["e_pval"], p_floor).sum())
    perm_denom = int(round(1.0 / p_floor))
    by = {g: (float(row.e_distance), float(-np.log10(max(row.e_qval, 1e-6))))
          for g, row in d.set_index("perturbation").iterrows()}
    cand_x = float(np.median([by[g][0] for g in CAND if g in by]))
    mach_x = float(np.median([by[g][0] for g in TCR if g in by]))

    fig, ax = figstyle.dark_figure((12.4, 7.0), dpi=200)

    ymax = float(y.max()) * 1.16
    sig_line = -np.log10(0.05)
    # shade the "everything is significant" band — NEUTRAL grey (not machinery-teal)
    ax.axhspan(sig_line, ymax, color="white", alpha=0.06, zorder=0)
    ax.axhline(sig_line, color=figstyle.MUTED, alpha=0.7, lw=1.1, ls="--", zorder=2)
    ax.text(0.995, sig_line + 0.03, "q = 0.05", transform=ax.get_yaxis_transform(),
            color=figstyle.MUTED, fontsize=10, ha="right", va="bottom")

    y_ceil = float(y.max())
    mask = ~d["perturbation"].isin(TCR + CAND)
    figstyle.bulk_cloud(ax, x[mask.to_numpy()], y[mask.to_numpy()], size=7, zorder=3)
    for genes, col in ((TCR, figstyle.TEAL_MID), (CAND, figstyle.AMBER_MID)):
        xs = [by[g][0] for g in genes if g in by]; ys = [by[g][1] for g in genes if g in by]
        figstyle.marker(ax, xs, ys, col, size=95, lw=2.2, zorder=5)

    # ceiling headline (axes-fraction coords so it never drifts with the ranges)
    ax.text(0.5, 0.975,
            f"significance ceiling — {pct_sig:.1f}% of tested knockdowns clear q < 0.05  ·  "
            f"{n_floor:,} at the permutation p-floor (p = 1/{perm_denom:,})",
            transform=ax.transAxes, fontsize=11.5, color=figstyle.BODY,
            ha="center", va="top", fontweight="bold")
    # candidate cluster callout — arrow anchored to the real cluster (data), text box
    # pinned in axes fraction so nothing breaks if the ranges shift.
    ax.annotate("candidate brakes\nmodest-to-moderate effect · signed positive\n"
                "not brake-enriched (Mann–Whitney p = 0.70)\nCBLB · CD5 · DGKA · SMAD3 · UBASH3A",
                xy=(cand_x, y_ceil), xycoords="data",
                xytext=(0.235, 0.70), textcoords="axes fraction",
                fontsize=11, color=figstyle.AMBER, fontweight="bold", ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.5", fc=figstyle.BG_PANEL,
                          ec=figstyle.AMBER, lw=1.2),
                arrowprops=dict(arrowstyle="-|>", color=figstyle.AMBER, lw=1.4))
    # TCR machinery callout (high E)
    ax.annotate("TCR machinery\nthe largest effects\nZAP70 · CD3E · LAT · LCP2 …",
                xy=(mach_x, y_ceil), xycoords="data",
                xytext=(0.60, 0.48), textcoords="axes fraction",
                fontsize=11, color=figstyle.TEAL, fontweight="bold", ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.5", fc=figstyle.BG_PANEL,
                          ec=figstyle.TEAL, lw=1.2),
                arrowprops=dict(arrowstyle="-|>", color=figstyle.TEAL, lw=1.4))
    # takeaway — single-purpose; the sign story lives in the companion causal map
    ax.text(0.018, 0.10,
            "p-value can't rank these — effect size can.\n"
            "(the signed causal map then separates brake from machinery)",
            transform=ax.transAxes, fontsize=12, color=figstyle.BODY, ha="left", va="bottom",
            bbox=dict(boxstyle="round,pad=0.55", fc=figstyle.BG_PANEL,
                      ec=figstyle.HAIRLINE, lw=1))

    ax.set_xlim(-1.5, 76); ax.set_ylim(0, ymax)
    ax.set_xlabel("Causal effect size  ·  E-distance (power-equalized)", fontsize=12.5,
                  color=figstyle.BODY)
    ax.set_ylabel("Statistical significance  ·  −log₁₀(q)", fontsize=12.5,
                  color=figstyle.BODY)
    figstyle.title_block(
        fig,
        "Why we rank by effect size, not p-value",
        [f"{n:,} tested knockdowns · E-distance on 2.44 M post-QC CD4⁺ T cells. "
         "Teal = TCR machinery, amber = candidate brakes."],
        x=0.065,
        y=0.97,
        title_size=18,
        sub_size=11,
        dy=0.065,
    )
    fig.subplots_adjust(left=0.075, right=0.975, top=0.80, bottom=0.11)
    fig.savefig(out, dpi=200, facecolor=figstyle.BG)
    fig.savefig(out.replace(".png", ".svg"), facecolor=figstyle.BG)
    figstyle.plt.close(fig)
    print(f"wrote {out}  (n={n}, sig={pct_sig:.1f}%, floor={n_floor})")


if __name__ == "__main__":
    df = pd.read_csv("outputs_gladstone/ranked_perturbations.csv")
    significance_wall(df, "../deliverables/figures/significance_wall.png")
