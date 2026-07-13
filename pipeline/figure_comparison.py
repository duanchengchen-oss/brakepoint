"""figure_comparison.py — why the signed axis matters (naive vs signed ranking).

Unsigned, the top-20 knockdowns by causal effect look interchangeable. Add the
signed direction axis and 18 of 20 are revealed as the cell's own essential
machinery — leaving the real candidate brakes. Output: deliverables/figures/naive_vs_signed.{png,svg}
"""
from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
try:
    import figstyle  # shared dark theme (fonts + palette)
    figstyle.apply_rc()
    C = figstyle.PALETTE
    BG, INK, MUT = C["bg"], C["ink"], C["mut"]
    TEAL, AMBER = C["teal2"], C["amber2"]
except Exception:  # safe fallback — never crash the build
    BG, INK, MUT, TEAL, AMBER = "#0a1211", "#ffffff", "#8fa39d", "#0d9488", "#d97a12"
    plt.rcParams.update({"font.family": "DejaVu Sans"})

df = pd.read_csv("outputs_gladstone/ranked_perturbations.csv")
d = df[df["n_cells"] >= 30].dropna(subset=["e_distance", "direction_score"]).copy()
top = d.sort_values("e_distance", ascending=False).head(20).reset_index(drop=True)
n_mach = int((top["direction_score"] < 0).sum())

fig, ax = plt.subplots(figsize=(12.6, 6.6), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(-0.6, 20); ax.set_ylim(-0.2, 2.7); ax.axis("off")

xs = np.arange(20)
# Row 1 — ranked by effect size, UNSIGNED: identical neutral dots
for x in xs:
    ax.scatter(x, 2.0, s=230, c="#8f9d98", edgecolors="white", linewidths=1.6, zorder=3)
# Row 2 — same 20, SIGNED by direction: teal=machinery(neg), amber=candidate(pos)
for x in xs:
    neg = top.loc[x, "direction_score"] < 0
    ax.scatter(x, 0.8, s=230, c=(TEAL if neg else AMBER), edgecolors="white", linewidths=1.6, zorder=3)
# label the positive (candidate) ones on row 2
for x in xs:
    if top.loc[x, "direction_score"] >= 0:
        ax.annotate(top.loc[x, "perturbation"], (x, 0.8), (x, 0.36), ha="center", va="top",
                    fontsize=11, color=AMBER, fontweight="bold")

ax.text(-0.4, 2.0, "Ranked by\neffect size", ha="right", va="center", fontsize=13, color=MUT)
ax.text(-0.4, 0.8, "+ direction\n(signed)", ha="right", va="center", fontsize=13, color=INK, fontweight="bold")
ax.text(9.7, 2.52, "The top 20 knockdowns look interchangeable —", ha="center", fontsize=14.5, color=MUT)
ax.text(9.7, 1.44, f"but {n_mach} of 20 are the cell's own essential machinery (teal), not drug targets.",
        ha="center", fontsize=14.5, color=TEAL, fontweight="bold")

fig.suptitle("Why the signed axis matters", x=0.5, y=0.98, fontsize=20, fontweight="bold", color=INK)
fig.text(0.5, 0.055,
         "Effect size alone can't tell a drug target from machinery a T cell needs to survive. "
         "The signed direction axis can — and surfaces the candidate brakes.",
         ha="center", fontsize=12.5, color=MUT)
fig.subplots_adjust(left=0.12, right=0.97, top=0.86, bottom=0.13)
out = "../deliverables/figures/naive_vs_signed.png"
fig.savefig(out, facecolor=BG, dpi=200)
fig.savefig(out.replace(".png", ".svg"), facecolor=BG)
plt.close(fig)
print(f"wrote {out}  (machinery in top-20 = {n_mach}/20)")


if __name__ == "__main__":
    pass
