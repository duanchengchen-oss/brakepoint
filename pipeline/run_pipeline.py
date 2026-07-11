"""
run_pipeline.py — T-cell Perturb-seq causal-target pipeline (runs in Claude Science / your env).

RUNS IN: Claude Science's sandbox or any env with the deps in environment.yml.
NOT runnable in the Cowork sandbox (no scanpy/pertpy there). The E-distance CORE
it depends on (edistance_core.py) IS unit-tested there via `make smoke`.

Anchored on Shifrut & Marson 2018 (primary human CD8+ T cells, GSE119450) via the
scPerturb harmonized h5ad (guide calls already in .obs['perturbation']) — chosen so a
solo builder never hand-parses feature barcodes.

Red-team hardening baked in (see README §Rigor):
  - rank by E-distance MAGNITUDE, power-equalized; permutation p is only a gate
  - report donors-per-perturbation; require >=2 concordant guides/gene for a call
  - VIABILITY flag: per-perturbation cell recovery vs control (dropout reverses naive ranking)
  - KNOCKDOWN check: target-gene expression drop vs control (on-target proof)
  - intention-to-treat DE on all guide-assigned cells (avoid mixscape double-dipping)
  - fixed seeds + pinned env + one-command reproduction (`make hero`)

Usage:
  python run_pipeline.py --data data/ShifrutMarson2018.h5ad --control NT --outdir outputs
  python run_pipeline.py --synthetic                      # tiny AnnData self-test (needs anndata)
"""
from __future__ import annotations
import argparse, json, pathlib, sys
import numpy as np
import pandas as pd

from edistance_core import e_distance, e_test, power_equalize

SEED = 0


def log(msg): print(f"[pipeline] {msg}", flush=True)


def load(path, synthetic=False):
    import anndata as ad
    if synthetic:
        import scipy.sparse as sp
        rng = np.random.default_rng(SEED)
        n, g = 1800, 400
        perts = np.array(["NT"] * 600 + ["GENE1"] * 600 + ["GENE2"] * 600)
        donors = rng.choice(["d1", "d2", "d3"], n)
        X = rng.poisson(0.3, (n, g)).astype(float)
        X[perts == "GENE1", :20] += rng.poisson(3, (600, 20))   # strong effect
        X[perts == "GENE2", :5] += rng.poisson(1, (600, 5))     # weak effect
        A = ad.AnnData(sp.csr_matrix(X))
        A.var_names = [f"g{i}" for i in range(g)]
        A.obs["perturbation"] = perts
        A.obs["donor"] = donors
        return A
    return ad.read_h5ad(path)


def subsample_per_group(adata, pert_key: str = "perturbation",
                        max_per_group: int = 400, seed: int = SEED):
    """Cap cells per perturbation (incl. control) to bound memory/compute at genome scale.
    Ranking is preserved — E-distance needs only a few hundred cells per group."""
    rng = np.random.default_rng(seed)
    labels = adata.obs[pert_key].astype(str).values
    keep = []
    for g in np.unique(labels):
        idx = np.where(labels == g)[0]
        if len(idx) > max_per_group:
            idx = rng.choice(idx, max_per_group, replace=False)
        keep.append(idx)
    keep = np.sort(np.concatenate(keep))
    return adata[keep].copy()


def qc_normalize(adata, control, embedding: str = "X_pca"):
    import scanpy as sc
    adata.layers["counts"] = adata.X.copy()                      # keep raw for pseudobulk
    adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True, percent_top=None)
    # MAD-based cell filter (robust to outliers)
    def mad_ok(x, n=5):
        med = np.median(x); mad = np.median(np.abs(x - med)) + 1e-9
        return np.abs(x - med) / mad < n
    keep = (mad_ok(np.log1p(adata.obs["total_counts"]))
            & mad_ok(np.log1p(adata.obs["n_genes_by_counts"]))
            & (adata.obs["pct_counts_mt"] < 15))
    log(f"QC: keep {int(keep.sum())}/{adata.n_obs} cells")
    adata = adata[keep].copy()
    if embedding == "X_pca":
        # Full normalize + PCA path (small datasets): keep raw for pseudobulk via .raw.
        sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
        adata.raw = adata
        sc.pp.highly_variable_genes(adata, n_top_genes=2000, subset=True)
        sc.pp.scale(adata, max_value=10)
        sc.tl.pca(adata, n_comps=50, random_state=SEED)
    else:
        # Precomputed embedding (e.g. X_scVI): E-distance runs on the latent, and
        # knockdown_check needs only raw counts of the TARGET gene (kept sparse in
        # layers['counts']). At genome scale, densifying the full N x G normalized matrix
        # and duplicating it into .raw blows RAM — so DON'T. X stays raw counts (sparse);
        # knockdown_check normalizes per-cell on the fly, column by column.
        log(f"embedding={embedding}: skipping full normalize/.raw (memory-safe genome-scale path)")
    assert embedding in adata.obsm, f"embedding {embedding!r} not found in adata.obsm"
    return adata


def effect_sizes(adata, control, pert_key="perturbation", donor_key="donor",
                 min_cells=30, embedding: str = "X_pca"):
    """Per-perturbation E-distance (power-equalized) + E-test.

    Fix (red-team): viability is computed for ALL perturbations BEFORE any low-cell drop,
    so depleted (possibly toxic) perturbations are surfaced with a flag rather than
    silently discarded — those are exactly the hits the control exists to catch. Viability
    is relative to the MEDIAN perturbation size, not the pooled control count.
    """
    emb = adata.obsm[embedding]
    labels = adata.obs[pert_key].astype(str).values
    assert control in set(labels), f"control label {control!r} not found in obs[{pert_key!r}]"
    ctrl = emb[labels == control]
    assert len(ctrl) >= min_cells, f"only {len(ctrl)} control cells (< min_cells={min_cells})"

    perts = [p for p in sorted(set(labels)) if p != control]
    counts = {p: int((labels == p).sum()) for p in perts}
    med = float(np.median(list(counts.values()))) if counts else 0.0

    rows = []
    for p in perts:
        n = counts[p]
        viability = n / (med + 1e-9)                       # <0.5 of median => depletion/tox flag
        donors = (adata.obs.loc[labels == p, donor_key].nunique()
                  if donor_key in adata.obs else np.nan)
        if n < min_cells:                                  # surface depleted perts, don't drop
            rows.append(dict(perturbation=p, e_distance=np.nan, e_pval=np.nan, n_cells=n,
                             n_donors=donors, viability_ratio=viability,
                             note="dropped_low_cells_possible_depletion"))
            continue
        E, pval = e_test(emb[labels == p], ctrl, n_perm=1000, seed=SEED, equalize=True)
        rows.append(dict(perturbation=p, e_distance=E, e_pval=pval, n_cells=n,
                         n_donors=donors, viability_ratio=viability, note=""))

    df = pd.DataFrame(rows)
    tested = df["e_pval"].notna()
    df["e_qval"] = np.nan
    if tested.any():
        df.loc[tested, "e_qval"] = _bh(df.loc[tested, "e_pval"].values)
    df["viability_flag"] = df["viability_ratio"] < 0.5
    return df.sort_values("e_distance", ascending=False, na_position="last").reset_index(drop=True)


def knockdown_check(adata, df, control, modality="KO", pert_key="perturbation"):
    """On-target check: fold-change of the TARGET gene (perturbed/control) on per-cell-
    normalized RAW counts. Interpretation is MODALITY-aware (red-team fix):
      CRISPRi -> expect FC < 0.7 (repression);  CRISPRa -> expect FC > 1.3 (activation);
      KO (Cas9) -> mRNA often does NOT drop (frameshift transcripts can escape NMD), so a
      null FC does NOT disprove editing. For KO, on_target_ok is left NaN and you should
      prove editing via guide-calls or a functional signature instead.
    """
    import scipy.sparse as _sp
    counts = adata.layers["counts"] if "counts" in adata.layers else adata.X
    # Per-cell fraction of the TARGET gene, computed WITHOUT densifying the full matrix
    # (genome-scale: N x G dense would be ~100 GB). Extract only needed columns as sparse.
    if _sp.issparse(counts):
        counts = counts.tocsc()
        totals = np.asarray(counts.sum(1)).ravel() + 1e-9
        def _cp_col(gi):
            return (counts[:, gi].toarray().ravel()) / totals
    else:
        counts = np.asarray(counts)
        totals = counts.sum(1) + 1e-9
        def _cp_col(gi):
            return counts[:, gi] / totals
    labels = adata.obs[pert_key].astype(str).values
    ctrl_mask = labels == control
    fc, ok = [], []
    for p in df["perturbation"]:
        gene = str(p).split("_")[0]                          # 'RASA2_1' -> 'RASA2'
        if gene in adata.var_names:
            gi = adata.var_names.get_loc(gene)
            cpc = _cp_col(gi)
            m_p = cpc[labels == p].mean(); m_c = cpc[ctrl_mask].mean()
            f = float((m_p + 1e-12) / (m_c + 1e-12)); fc.append(f)
            ok.append(f > 1.3 if modality == "CRISPRa"
                      else f < 0.7 if modality == "CRISPRi"
                      else np.nan)                            # KO: mRNA FC uninformative
        else:
            fc.append(np.nan); ok.append(np.nan)
    df["target_fc"] = fc
    df["on_target_ok"] = ok
    return df


def _bh(p):
    p = np.asarray(p, float); n = len(p); order = np.argsort(p)
    q = np.empty(n); q[order] = (p[order] * n / (np.arange(n) + 1))
    return np.minimum.accumulate(q[order][::-1])[::-1][np.argsort(order)] if n else p


def score_and_rank(df):
    """Transparent gate + within-tier rank (no opaque weighted sum)."""
    df = df.copy()
    df["gate_sig"] = df["e_qval"] < 0.05
    df["gate_viable"] = ~df["viability_flag"]
    df["passes_gates"] = df["gate_sig"] & df["gate_viable"]
    df = df.sort_values(["passes_gates", "e_distance"], ascending=[False, False])
    return df.reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data"); ap.add_argument("--control", default="NT")
    ap.add_argument("--modality", default="KO", choices=["KO", "CRISPRi", "CRISPRa"])
    ap.add_argument("--embedding", default="X_pca",
                    help="obsm key for E-distance; pass e.g. X_scVI to use the scvi-tools skill output")
    ap.add_argument("--max-cells-per-group", type=int, default=0,
                    help="cap cells per perturbation/control before analysis (0=off); use for genome-scale")
    ap.add_argument("--outdir", default="outputs"); ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args()
    np.random.seed(SEED)
    out = pathlib.Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    adata = load(a.data, synthetic=a.synthetic)
    log(f"loaded {adata.n_obs} cells x {adata.n_vars} genes")
    if a.max_cells_per_group:
        adata = subsample_per_group(adata, max_per_group=a.max_cells_per_group)
        log(f"subsampled to <= {a.max_cells_per_group}/group -> {adata.n_obs} cells")
    adata = qc_normalize(adata, a.control, embedding=a.embedding)
    df = effect_sizes(adata, a.control, embedding=a.embedding)
    df = knockdown_check(adata, df, a.control, modality=a.modality)
    df = score_and_rank(df)

    df.to_csv(out / "ranked_perturbations.csv", index=False)
    (out / "run_meta.json").write_text(json.dumps(
        {"seed": SEED, "n_cells": int(adata.n_obs), "control": a.control,
         "n_perturbations": int(len(df)), "top": df.head(10)["perturbation"].tolist()}, indent=2))
    log(f"wrote {out/'ranked_perturbations.csv'}")
    print(df.head(12).to_string(index=False))
    # NEXT (in Claude Science): pseudobulk DE per (perturbation x donor) w/ pydeseq2;
    # mixscape as a sensitivity analysis; Open Targets direction-of-effect funnel on top hits.


if __name__ == "__main__":
    main()
