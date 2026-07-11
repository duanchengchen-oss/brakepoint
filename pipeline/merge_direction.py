"""merge_direction.py — merge the signed direction axis into the E-distance leaderboard.

Takes the per-perturbation ``direction_score`` produced by
:mod:`direction_genomescale` (the genome-scale CD4 run) and merges it into the
E-distance ``ranked_perturbations.csv``, assigning a ``direction_tier`` with the
unit-tested :func:`direction.assign_tier` (which uses the leaderboard's own
``viability_ratio`` to split essential machinery from viable enhancers).

Kept separate from the heavy per-cell scoring so tier thresholds can be retuned
in milliseconds without recomputing the 2.64M-cell pass.

Usage::

    python merge_direction.py \
        --ranked   outputs_gladstone/ranked_perturbations.csv \
        --direction outputs_gladstone/direction_scores_raw.csv \
        --out      outputs_gladstone/ranked_perturbations.csv \
        --tau 0.05
"""
from __future__ import annotations

import argparse

import pandas as pd

from direction import DIRECTION_TAU, VIABILITY_FLOOR, assign_tier


def merge_direction(
    ranked_csv: str,
    direction_csv: str,
    out_csv: str,
    tau: float = DIRECTION_TAU,
    viability_floor: float = VIABILITY_FLOOR,
) -> pd.DataFrame:
    ranked = pd.read_csv(ranked_csv)
    direction = pd.read_csv(direction_csv)
    # drop any stale direction_* columns before re-merging (idempotent re-runs)
    stale = [c for c in ranked.columns if c.startswith("direction_")]
    ranked = ranked.drop(columns=stale, errors="ignore")

    merged = ranked.merge(direction, on="perturbation", how="left")
    via = dict(zip(merged["perturbation"].astype(str), merged["viability_ratio"]))
    merged["direction_tier"] = [
        assign_tier(s, via.get(str(p)), tau, viability_floor)
        if pd.notna(s)
        else "unscored"
        for p, s in zip(merged["perturbation"], merged["direction_score"])
    ]
    merged.to_csv(out_csv, index=False)
    return merged


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranked", required=True)
    ap.add_argument("--direction", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tau", type=float, default=DIRECTION_TAU)
    ap.add_argument("--viability-floor", type=float, default=VIABILITY_FLOOR)
    a = ap.parse_args()
    m = merge_direction(a.ranked, a.direction, a.out, a.tau, a.viability_floor)
    scored = m["direction_score"].notna()
    print(f"merged {int(scored.sum())}/{len(m)} perturbations with a direction_score")
    print("tier counts:", m.loc[scored, "direction_tier"].value_counts().to_dict())


if __name__ == "__main__":
    main()
