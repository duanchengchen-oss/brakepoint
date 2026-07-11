"""direction_genomescale.py — signed CD4 direction axis on the genome-scale run.

Computes the per-perturbation signed *direction-of-effect* score on the
genome-scale Gladstone CRISPRi Perturb-seq build (primary human CD4+ T cells,
~2.64M cells x 4,816 measured HVGs, donors D1+D2, Stim 8h). The E-distance
leaderboard ranks by *magnitude* only and cannot separate an activation-required
gene (ZAP70, whose knockdown cripples the cell) from a therapeutic *brake*
(whose knockdown enhances effector function): both sit far from control. This
script supplies the missing sign.

Per cell, on ``normalize_total(1e4) + log1p`` expression (matching the
pipeline), we score two curated CD4 programs and take their difference::

    direction = mean(effector program) - mean(dysfunction program)

The background baseline used by :func:`direction._direction_scores_numpy`
(``module_mean - background_mean``) cancels in this difference, so the per-cell
score reduces to ``effector_mean - dysfunction_mean``. Programs are defined (as
gene symbols) in :mod:`direction` (``CD4_EFFECTOR_GENES`` / ``CD4_DYSFUNCTION_GENES``);
because the build's ``var_names`` are Ensembl ids, we translate the modules to
Ensembl via the provided sgRNA-library metadata before scoring.

Aggregation reuses :func:`direction.score_direction` (donors as replicates, mean
of per-donor ``pert - control`` deltas, plus a per-donor sign-agreement flag) —
the exact logic unit-tested by ``direction._smoke``.

Runs in the DGX scanpy env; NOT in the numpy-only sandbox. Emits a small
``direction_scores_raw.csv`` (one row per perturbation) that is merged into the
E-distance leaderboard downstream (tiers are assigned there, where the
per-perturbation ``viability_ratio`` lives).

Usage::

    python direction_genomescale.py \
        --data   tcell_data/GWCD4i_Stim8hr_D1D2.built.h5ad \
        --lib    tcell_data/sgrna_library_metadata.suppl_table.csv \
        --control control \
        --out    direction_scores_raw.csv
"""
from __future__ import annotations

import argparse
import json
import logging
import pathlib
import time

import numpy as np
import pandas as pd

import direction

logging.basicConfig(level=logging.INFO, format="[direction] %(message)s")
log = logging.getLogger(__name__)

TARGET_SUM = 1e4  # matches run_pipeline.qc_normalize


def build_symbol_to_ensembl(lib_csv: str) -> dict[str, str]:
    """Symbol -> Ensembl id map from the provided sgRNA-library metadata."""
    lib = pd.read_csv(lib_csv, low_memory=False)
    pairs = (
        lib.dropna(subset=["target_gene_name", "target_gene_id"])[
            ["target_gene_name", "target_gene_id"]
        ]
        .drop_duplicates()
    )
    return dict(zip(pairs["target_gene_name"].astype(str), pairs["target_gene_id"].astype(str)))


def resolve_module(
    symbols: tuple[str, ...], sym2ens: dict[str, str], var_names: set[str]
) -> tuple[list[str], list[str]]:
    """Translate a symbol module to Ensembl ids present in ``var_names``."""
    ens, missing = [], []
    for s in symbols:
        e = sym2ens.get(s)
        if e is not None and e in var_names:
            ens.append(e)
        else:
            missing.append(s)
    return ens, missing


def per_cell_module_scores(
    adata: "object",
    eff_idx: np.ndarray,
    dys_idx: np.ndarray,
    chunk: int = 200_000,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-cell mean log-normalized effector/dysfunction scores + total counts.

    Streams the matrix in *row* chunks (CSR row-slicing is O(1) in the indptr,
    unlike full-matrix column fancy-indexing) and densifies only the handful of
    module columns per chunk, so memory stays flat regardless of cell count.
    """
    import scipy.sparse as sp

    n = adata.n_obs
    eff = np.empty(n, dtype=float)
    dys = np.empty(n, dtype=float)
    tot = np.empty(n, dtype=float)
    X = adata.X
    for i in range(0, n, chunk):
        j = min(i + chunk, n)
        blk = X[i:j]
        if sp.issparse(blk):
            t = np.asarray(blk.sum(axis=1)).ravel().astype(float)
            e = blk[:, eff_idx].toarray()
            d = blk[:, dys_idx].toarray()
        else:
            blk = np.asarray(blk)
            t = blk.sum(axis=1).astype(float)
            e = blk[:, eff_idx]
            d = blk[:, dys_idx]
        t_safe = np.where(t > 0, t, 1.0)[:, None]
        eff[i:j] = np.log1p(e / t_safe * TARGET_SUM).mean(axis=1)
        dys[i:j] = np.log1p(d / t_safe * TARGET_SUM).mean(axis=1)
        tot[i:j] = t
        log.info(f"  scored {j:,}/{n:,} cells")
    return eff, dys, tot


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="built h5ad (raw counts, Ensembl var)")
    ap.add_argument("--lib", required=True, help="sgRNA-library metadata csv (symbol->Ensembl)")
    ap.add_argument("--control", default="control")
    ap.add_argument("--pert-key", default="perturbation")
    ap.add_argument("--donor-key", default="donor")
    ap.add_argument("--out", default="direction_scores_raw.csv")
    ap.add_argument("--meta", default="direction_meta.json")
    args = ap.parse_args()

    import anndata as ad

    t0 = time.time()
    log.info(f"loading {args.data} (full into memory) ...")
    adata = ad.read_h5ad(args.data)
    log.info(f"loaded {adata.n_obs:,} cells x {adata.n_vars:,} genes in {time.time()-t0:.0f}s")

    sym2ens = build_symbol_to_ensembl(args.lib)
    var_names = set(map(str, adata.var_names))
    eff_ens, eff_missing = resolve_module(direction.CD4_EFFECTOR_GENES, sym2ens, var_names)
    dys_ens, dys_missing = resolve_module(direction.CD4_DYSFUNCTION_GENES, sym2ens, var_names)
    log.info(f"effector module: {len(eff_ens)}/{len(direction.CD4_EFFECTOR_GENES)} present"
             + (f" | missing {eff_missing}" if eff_missing else ""))
    log.info(f"dysfunction module: {len(dys_ens)}/{len(direction.CD4_DYSFUNCTION_GENES)} present"
             + (f" | missing {dys_missing}" if dys_missing else ""))
    if not eff_ens or not dys_ens:
        raise SystemExit("a module resolved to zero genes — aborting")

    var_index = adata.var_names
    eff_idx = np.array([var_index.get_loc(e) for e in eff_ens], dtype=int)
    dys_idx = np.array([var_index.get_loc(e) for e in dys_ens], dtype=int)

    log.info("scoring effector + dysfunction programs (row-chunked) ...")
    eff, dys, totals = per_cell_module_scores(adata, eff_idx, dys_idx)
    cell_scores = (eff - dys).astype(float)
    cell_scores[totals <= 0] = np.nan  # drop empty cells from aggregation

    perts = adata.obs[args.pert_key].astype(str).to_numpy()
    donors = (
        adata.obs[args.donor_key].astype(str).to_numpy()
        if args.donor_key in adata.obs
        else np.full(adata.n_obs, "all")
    )

    keep = ~np.isnan(cell_scores)
    results = direction.score_direction(
        perts[keep],
        donors[keep],
        control=args.control,
        cell_scores=cell_scores[keep],
        viability=None,  # tiers assigned downstream, where viability_ratio lives
    )
    df = direction.direction_dataframe(results)
    # drop the (viability-free) tier column; tiering happens at the merge step
    df = df.drop(columns=["direction_tier"], errors="ignore")
    df = df.sort_values("direction_score").reset_index(drop=True)
    df.to_csv(args.out, index=False)

    ds = df["direction_score"].to_numpy()
    pct = {str(p): round(float(np.percentile(ds, p)), 5) for p in (1, 5, 25, 50, 75, 95, 99)}
    meta = {
        "data": args.data,
        "control": args.control,
        "n_cells_scored": int(keep.sum()),
        "n_cells_total": int(adata.n_obs),
        "n_perturbations": int(df.shape[0]),
        "effector_module_symbols": list(direction.CD4_EFFECTOR_GENES),
        "effector_present_ensembl": eff_ens,
        "effector_missing": eff_missing,
        "dysfunction_module_symbols": list(direction.CD4_DYSFUNCTION_GENES),
        "dysfunction_present_ensembl": dys_ens,
        "dysfunction_missing": dys_missing,
        "target_sum": TARGET_SUM,
        "direction_score_percentiles": pct,
        "runtime_s": round(time.time() - t0, 1),
    }
    pathlib.Path(args.meta).write_text(json.dumps(meta, indent=2))
    log.info(f"wrote {args.out} ({df.shape[0]} perturbations) + {args.meta} in {meta['runtime_s']}s")
    log.info(f"direction_score percentiles: {pct}")


if __name__ == "__main__":
    main()
