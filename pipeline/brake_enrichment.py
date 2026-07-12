"""brake_enrichment.py — is the positive/brake quadrant enriched for known brakes?

Honest self-check on the signed map. Tests whether a curated set of *known*
T-cell negative regulators ("brakes") has a more positive ``direction_score`` than
background. Scoring-module genes are excluded (a module gene would shift its own
pole — circular). Reports a one-sided Mann–Whitney U.

Result at 2 donors / Stim-8h: **not significant (p ≈ 0.56)** — the positive side
is a noisy hypothesis space, not a brake-enriched ranking. We report this null
rather than cherry-pick; the validated result is the machinery axis (see
``real-finding-genomescale.md``).
"""
from __future__ import annotations

import argparse

import pandas as pd
from scipy.stats import mannwhitneyu

# scoring-module genes — excluded to avoid circularity
MODULE = set(
    "IFNG IL2 TNF CSF2 LTA XCL1 XCL2 CCL3 CCL4 GZMB TNFRSF9 CD69 MYC IRF4 BATF TBX21 "
    "PDCD1 CTLA4 LAG3 HAVCR2 TIGIT BTLA CD160 VSIR ENTPD1 TOX NR4A1 NR4A2 NR4A3".split()
)
# curated known T-cell negative regulators / brakes (KO enhances function), non-module
KNOWN_BRAKES = [
    "CBLB", "CBL", "CD5", "DGKA", "DGKZ", "TNFAIP3", "SOCS1", "SOCS3", "CISH", "PTPN2",
    "PTPN6", "RASA2", "RASA3", "UBASH3A", "RC3H1", "ZC3H12A", "TCEB2", "SUV39H1",
    "ARID1A", "ARID2", "STK11", "TNFAIP8L2", "GRAP2", "TMEM222", "FAM49B", "CYRIB",
    "RNF125", "MAP4K1", "TET2", "SLA", "SLA2",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranked", default="outputs_gladstone/ranked_perturbations.csv")
    ap.add_argument("--matched", action="store_true", default=True,
                    help="restrict background to the same quality tier as the brakes "
                         "(2-donor, kd-gated) so the comparison is fair (per code review)")
    a = ap.parse_args()
    m = pd.read_csv(a.ranked).set_index("perturbation")
    present = [g for g in KNOWN_BRAKES if g in m.index]
    brakes = m.loc[present, "direction_score"].dropna()
    # matched eligible universe: 2-donor + knockdown-gated (same quality as the brakes),
    # excluding scoring-module genes and the brake set itself — a fair background.
    elig = m[(m.get("direction_n_donors", 2) >= 2)]
    if "kd_gated_hit" in m.columns:
        elig = elig[elig["kd_gated_hit"] == True]  # noqa: E712
    bg = elig[~elig.index.isin(MODULE) & ~elig.index.isin(present)]["direction_score"].dropna()
    u, p = mannwhitneyu(brakes, bg, alternative="greater")
    print(f"known brakes present : {len(present)}/{len(KNOWN_BRAKES)}  (curated literature set — EXPLORATORY, not pre-registered)")
    print(f"matched background n : {len(bg)}  (2-donor, kd-gated; module + brakes excluded)")
    print(f"brake median / mean  : {brakes.median():+.3f} / {brakes.mean():+.3f}")
    print(f"background median/mean: {bg.median():+.3f} / {bg.mean():+.3f}")
    print(f"fraction positive    : brakes {(brakes > 0).mean():.1%} vs bg {(bg > 0).mean():.1%}")
    print(f"Mann-Whitney one-sided (brakes > bg): U={u:.0f}  p={p:.3f}")
    print("VERDICT:", "ENRICHED" if p < 0.05 else "no significant evidence of enrichment — positive side is a noisy hypothesis space")


if __name__ == "__main__":
    main()
