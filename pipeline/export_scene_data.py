"""export_scene_data.py — JSON for the animated video scenes (Significance, Brakes/donor).

Reads the genome-scale leaderboard and writes two small JSON files the Remotion scenes
render natively (same pattern as mapdata.json), so the video draws the real data in the
dark premium style instead of embedding a static figure.
Output: deliverables/_remotion/public/{sigdata,donordata}.json
"""
from __future__ import annotations
import json
import pathlib
import numpy as np
import pandas as pd

OUT = pathlib.Path(__file__).parent.parent / "deliverables/_remotion/public"
TCR = ["ZAP70", "LCP2", "CD3E", "CD3G", "PLCG1", "LAT", "VAV1", "CD3D", "CD247", "ITK"]
CAND = ["CBLB", "CD5", "DGKA", "UBASH3A", "SMAD3"]
rng = np.random.default_rng(0)


def main() -> None:
    df = pd.read_csv(pathlib.Path(__file__).parent / "outputs_gladstone/ranked_perturbations.csv")

    # ---- significance wall: x = E-distance, y = -log10(q) ----
    d = df[df["n_cells"] >= 30].dropna(subset=["e_distance", "e_qval"]).copy()
    d["y"] = -np.log10(d["e_qval"].clip(lower=1e-6))
    n = len(d)
    pct = round(100 * (d["e_qval"] < 0.05).mean(), 1)
    pfloor = float(d["e_pval"].min())
    nfloor = int(np.isclose(d["e_pval"], pfloor).sum())
    perm = int(round(1.0 / pfloor))
    by = {r.perturbation: (round(float(r.e_distance), 3), round(float(r.y), 3)) for r in d.itertuples()}
    bulk = d[~d["perturbation"].isin(TCR + CAND)][["e_distance", "y"]].to_numpy()
    if len(bulk) > 1600:
        bulk = bulk[rng.choice(len(bulk), 1600, replace=False)]
    sig = {
        "bulk": [[round(float(x), 3), round(float(y), 3)] for x, y in bulk],
        "machinery": [{"g": g, "x": by[g][0], "y": by[g][1]} for g in TCR if g in by],
        "cand": [{"g": g, "x": by[g][0], "y": by[g][1]} for g in CAND if g in by],
        "xmax": 76, "ymax": round(float(d["y"].max()) * 1.12, 2),
        "qline": round(float(-np.log10(0.05)), 3),
        "pctSig": pct, "nFloor": nfloor, "perm": perm, "n": n,
    }
    (OUT / "sigdata.json").write_text(json.dumps(sig))

    # ---- donor consistency: x = donor-A direction, y = donor-B direction ----
    def split(s):
        try:
            a, b = str(s).split(";")
            return float(a), float(b)
        except Exception:
            return None

    dd = df.dropna(subset=["direction_per_donor"]).copy()
    dd["pd"] = dd["direction_per_donor"].map(split)
    dd = dd[dd["pd"].notna()].copy()
    dd["dA"] = dd["pd"].map(lambda t: t[0])
    dd["dB"] = dd["pd"].map(lambda t: t[1])
    byd = {r.perturbation: (round(float(r.dA), 3), round(float(r.dB), 3), bool(r.direction_sign_agreement))
           for r in dd.itertuples()}
    bd = dd[~dd["perturbation"].isin(TCR + CAND)][["dA", "dB"]].to_numpy()
    if len(bd) > 1400:
        bd = bd[rng.choice(len(bd), 1400, replace=False)]
    lim = round(float(max(dd["dA"].abs().max(), dd["dB"].abs().max())) * 1.08, 2)
    don = {
        "bulk": [[round(float(a), 3), round(float(b), 3)] for a, b in bd],
        "machinery": [{"g": g, "x": byd[g][0], "y": byd[g][1], "a": byd[g][2]} for g in TCR if g in byd],
        "cand": [{"g": g, "x": byd[g][0], "y": byd[g][1], "a": byd[g][2]} for g in CAND if g in byd],
        "lim": lim,
    }
    (OUT / "donordata.json").write_text(json.dumps(don))
    print(f"sigdata: n={n} pct={pct} floor={nfloor} perm={perm}")
    print(f"donordata: cand={[(c['g'], c['a']) for c in don['cand']]}")


if __name__ == "__main__":
    main()
