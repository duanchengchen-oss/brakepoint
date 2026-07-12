import json, pandas as pd, numpy as np, pathlib
df = pd.read_csv("outputs_gladstone/ranked_perturbations.csv")
df = df[df.n_cells >= 30].dropna(subset=["e_distance","direction_score"]).copy()
TCR = {"ZAP70","LCP2","CD3E","CD3G","PLCG1","LAT","VAV1","CD3D","CD247","ITK"}
CAND = {"CBLB","CD5","DGKA","UBASH3A","SMAD3"}
def cat(g): return 2 if g in CAND else (1 if g in TCR else 0)
df["cat"] = df.perturbation.map(cat)
# sort so highlighted points draw on top (bulk first)
df = df.sort_values("cat")
genes = df.perturbation.tolist()
x = [round(float(v),3) for v in df.e_distance]
y = [round(float(v),4) for v in df.direction_score]
n = [int(v) for v in df.n_cells]
cats = [int(v) for v in df.cat]
tier = df.direction_tier.fillna("").tolist()
# per-donor only meaningful for highlighted (keep small)
pdon = df.direction_per_donor.fillna("").tolist()
out = {
  "genes": genes, "x": x, "y": y, "n": n, "cat": cats, "tier": tier, "pdon": pdon,
  "xmax": float(df.e_distance.max()), "ymin": float(df.direction_score.min()), "ymax": float(df.direction_score.max()),
  "count": len(df),
}
p = pathlib.Path("../deliverables/data/causal_map_points.json")
p.write_text(json.dumps(out, separators=(",",":")))
print("wrote", p, f"{p.stat().st_size/1024:.0f} KB, {len(df)} points; cats:", {c:cats.count(c) for c in (0,1,2)})
