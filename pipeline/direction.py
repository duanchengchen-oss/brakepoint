"""direction.py — signed direction-of-effect axis for the perturbation leaderboard.

The E-distance leaderboard (``edistance_core`` / ``run_pipeline``) ranks by
*magnitude* only. Magnitude alone cannot tell an activation-**required** gene
(CD3D, ZAP70, LAT — whose knockout *cripples* the cell) apart from a therapeutic
**brake** (CBLB, PDCD1 — whose knockout *enhances* effector function): both move
far from control. This module supplies the missing sign.

Per cell we score two curated T-cell programs with ``scanpy.tl.score_genes``:

* cytotoxic / effector : FGFBP2, GZMB, GZMH, GNLY, PRF1, NKG7, IFNG, GZMA, GZMK, KLRD1
* dysfunction / exhaustion : LAG3, PDCD1, HAVCR2, TIGIT, TOX, ENTPD1, CXCL13

(van der Leun / Li et al., *Cell* 2019; DOI 10.1016/j.cell.2018.11.043.)

``direction_score(perturbation) = Δ(cytotoxic − exhaustion)`` versus control,
aggregated per ``(perturbation × donor)`` then averaged across donors (donors as
replicates). Sign convention:

* ``> 0`` — knockout shifts cells toward the cytotoxic/effector program → the gene
  is a **brake** (its removal enhances function; an enhancement candidate).
* ``< 0`` — knockout shifts cells toward exhaustion / loss of effector function →
  the gene is an **enhancer** (it normally promotes function).

A per-donor sign-agreement flag reports whether every donor agrees (softens n=2).

Tiers (E-distance stays the magnitude; this module supplies the sign plus a
viability-aware split that separates non-essential enhancers from essential
machinery):

======================  =========================================  ============================
tier                    rule                                       reading
======================  =========================================  ============================
``brake``               ``direction_score > +tau``, viable          enhancement candidate
``enhancer``            ``direction_score < -tau``, viable          normally promotes effector fn
``required-machinery``  ``direction_score < -tau``, NOT viable      positive control (essential)
``neutral``             ``|direction_score| <= tau``                no directional shift
======================  =========================================  ============================

``scanpy.tl.score_genes`` needs scanpy; the SIGN LOGIC does not.
``_direction_scores_numpy`` reproduces the module-minus-background logic in pure
numpy so the axis is unit-testable in the numpy-only Cowork sandbox (no scanpy
here). ``_smoke`` builds a matrix with a known cytotoxic-up perturbation and a
known exhaustion-up perturbation and asserts the sign is recovered.

NOTE: regenerating the REAL ranked CSV with a scanpy ``score_genes`` column needs
a Claude Science re-run (the scanpy/scvi stack is unavailable in this sandbox).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

# --- curated modules (van der Leun / Li et al., Cell 2019) --------------------
CYTOTOXIC_GENES: tuple[str, ...] = (
    "FGFBP2",
    "GZMB",
    "GZMH",
    "GNLY",
    "PRF1",
    "NKG7",
    "IFNG",
    "GZMA",
    "GZMK",
    "KLRD1",
)
EXHAUSTION_GENES: tuple[str, ...] = (
    "LAG3",
    "PDCD1",
    "HAVCR2",
    "TIGIT",
    "TOX",
    "ENTPD1",
    "CXCL13",
)

# --- CD4 effector axis (the genome-scale Gladstone arm is primary human CD4+) --
# The CD8 cytotoxic/exhaustion contrast above is the wrong axis for a CD4+
# stimulation screen. For the Stim-8h CD4 arm we score the canonical T-cell
# effector/activation program against the inhibitory-receptor / exhaustion-TF
# program. Same signed convention: KD that raises (effector - dysfunction)
# relative to control => brake (its removal enhances effector function).
#
#   effector cytokines + activation TFs  ......... IFNG, IL2, TNF, CSF2, LTA,
#       XCL1/2, CCL3/4, GZMB, TNFRSF9 (4-1BB), CD69, MYC, IRF4, BATF, TBX21
#   inhibitory receptors + exhaustion/anergy TFs . PDCD1, CTLA4, LAG3, HAVCR2,
#       TIGIT, BTLA, CD160, VSIR, ENTPD1, TOX, NR4A1/2/3
#
# Effector cytokines/receptors are textbook activation markers; TOX (Khan et al.
# Nature 2019) and NR4A1/2/3 (Chen et al. Nature 2019; Liu et al. Nature 2019)
# are the master exhaustion/tolerance transcription factors. IL2RB is
# deliberately excluded (it is the network-nominated hero — scoring it would be
# circular). All genes below are present in the 4,816 measured HVGs of the
# Gladstone CD4 build (coverage verified before the run).
CD4_EFFECTOR_GENES: tuple[str, ...] = (
    "IFNG",
    "IL2",
    "TNF",
    "CSF2",
    "LTA",
    "XCL1",
    "XCL2",
    "CCL3",
    "CCL4",
    "GZMB",
    "TNFRSF9",
    "CD69",
    "MYC",
    "IRF4",
    "BATF",
    "TBX21",
)
CD4_DYSFUNCTION_GENES: tuple[str, ...] = (
    "PDCD1",
    "CTLA4",
    "LAG3",
    "HAVCR2",
    "TIGIT",
    "BTLA",
    "CD160",
    "VSIR",
    "ENTPD1",
    "TOX",
    "NR4A1",
    "NR4A2",
    "NR4A3",
)

# --- tier thresholds (tunable; see re-run note) -------------------------------
DIRECTION_TAU: float = 0.05  # |direction_score| at or below this => neutral
VIABILITY_FLOOR: float = 0.8  # viability_ratio below this => essential machinery

TIER_BRAKE = "brake"
TIER_ENHANCER = "enhancer"
TIER_REQUIRED = "required-machinery"
TIER_NEUTRAL = "neutral"


@dataclass(frozen=True)
class DirectionResult:
    """Signed direction-of-effect summary for one perturbation."""

    perturbation: str
    direction_score: float
    tier: str
    donor_sign_agreement: bool
    n_donors: int
    per_donor_scores: tuple[float, ...]

    def as_dict(self) -> dict[str, object]:
        """Flat, CSV-friendly record (``direction_`` prefix for merge safety)."""
        return {
            "perturbation": self.perturbation,
            "direction_score": self.direction_score,
            "direction_tier": self.tier,
            "direction_sign_agreement": self.donor_sign_agreement,
            "direction_n_donors": self.n_donors,
            "direction_per_donor": ";".join(f"{v:.4f}" for v in self.per_donor_scores),
        }


def assign_tier(
    direction_score: float,
    viability_ratio: float | None = None,
    tau: float = DIRECTION_TAU,
    viability_floor: float = VIABILITY_FLOOR,
) -> str:
    """Map a signed direction score (+ optional viability) to a tier label.

    E-distance remains the magnitude; this only encodes the sign and, on the
    loss-of-effector side, a viability split that separates a non-essential
    enhancer from essential machinery whose knockout kills the cell.

    Direction performs the classification; viability is only a toxicity annotation
    on the negative side. Non-finite scores are treated as neutral (never silently
    mis-tiered).
    """
    if not np.isfinite(direction_score):
        return TIER_NEUTRAL
    if abs(direction_score) <= tau:
        return TIER_NEUTRAL
    if direction_score > 0:
        return TIER_BRAKE
    if viability_ratio is not None and viability_ratio < viability_floor:
        return TIER_REQUIRED
    return TIER_ENHANCER


def _direction_scores_numpy(
    expr: np.ndarray,
    gene_names: Sequence[str],
    positive_genes: Sequence[str] = CYTOTOXIC_GENES,
    negative_genes: Sequence[str] = EXHAUSTION_GENES,
) -> np.ndarray:
    """Per-cell ``positive − negative`` module score, pure numpy.

    A dependency-light stand-in for ``scanpy.tl.score_genes``: each module score
    is ``mean(module genes) − mean(background genes)`` where the background is
    every gene outside both modules. Same sign behaviour as ``score_genes``'s
    binned control set; used for the smoke test and as a scanpy-free fallback.
    Defaults to the CD8 cytotoxic/exhaustion axis; pass the ``CD4_*`` modules for
    the CD4 effector/dysfunction axis.
    """
    name_to_idx = {g: i for i, g in enumerate(gene_names)}
    cyto_idx = [name_to_idx[g] for g in positive_genes if g in name_to_idx]
    exh_idx = [name_to_idx[g] for g in negative_genes if g in name_to_idx]
    if not cyto_idx or not exh_idx:
        raise ValueError(
            "expression matrix is missing all genes of a module "
            f"(cytotoxic hits={len(cyto_idx)}, exhaustion hits={len(exh_idx)})"
        )
    module = set(cyto_idx) | set(exh_idx)
    bg_idx = [i for i in range(len(gene_names)) if i not in module]
    if not bg_idx:  # degenerate: everything is a module gene
        bg_idx = list(range(len(gene_names)))
    background = expr[:, bg_idx].mean(axis=1)
    cyto = expr[:, cyto_idx].mean(axis=1) - background
    exh = expr[:, exh_idx].mean(axis=1) - background
    return np.asarray(cyto - exh, dtype=float)


def compute_cell_direction_scanpy(
    adata: "object",
    use_raw: bool | None = None,
    random_state: int = 0,
    positive_genes: Sequence[str] = CYTOTOXIC_GENES,
    negative_genes: Sequence[str] = EXHAUSTION_GENES,
) -> np.ndarray:
    """Per-cell ``positive − negative`` module score via ``scanpy.tl.score_genes``.

    Runs in Claude Science / any scanpy env (NOT exercised by the numpy smoke
    test). Writes ``cytotoxic_score`` / ``exhaustion_score`` into ``adata.obs``
    and returns their per-cell difference. Only genes present in ``var_names``
    are scored, so var names carrying only a subset of the module simply score
    fewer genes rather than crashing. Pass gene *symbols* here; if ``var_names``
    are Ensembl ids, translate the modules to Ensembl before calling (see
    ``direction_genomescale.py``).
    """
    import scanpy as sc  # local import: heavy, absent in the sandbox

    present_cyto = [g for g in positive_genes if g in adata.var_names]
    present_exh = [g for g in negative_genes if g in adata.var_names]
    if not present_cyto or not present_exh:
        raise ValueError(
            "adata.var_names carries none of a module's genes — are var names "
            "Ensembl ids? map to symbols before scoring "
            f"(cytotoxic={len(present_cyto)}, exhaustion={len(present_exh)})"
        )
    sc.tl.score_genes(
        adata, present_cyto, score_name="cytotoxic_score",
        use_raw=use_raw, random_state=random_state,
    )
    sc.tl.score_genes(
        adata, present_exh, score_name="exhaustion_score",
        use_raw=use_raw, random_state=random_state,
    )
    return (
        adata.obs["cytotoxic_score"].to_numpy()
        - adata.obs["exhaustion_score"].to_numpy()
    )


def score_direction(
    perturbations: Sequence[str],
    donors: Sequence[str],
    control: str,
    *,
    expr: np.ndarray | None = None,
    gene_names: Sequence[str] | None = None,
    cell_scores: np.ndarray | None = None,
    viability: Mapping[str, float] | None = None,
    tau: float = DIRECTION_TAU,
    viability_floor: float = VIABILITY_FLOOR,
) -> list[DirectionResult]:
    """Aggregate per-cell direction scores into a signed per-perturbation call.

    Provide either ``cell_scores`` (e.g. the scanpy output) or ``expr`` +
    ``gene_names`` (the numpy fallback computes the per-cell score). For each
    perturbation the score is the mean over donors of ``(pert donor mean −
    control donor mean)`` — donors as replicates — with a sign-agreement flag.
    """
    if cell_scores is None:
        if expr is None or gene_names is None:
            raise ValueError("pass cell_scores, or both expr and gene_names")
        cell_scores = _direction_scores_numpy(expr, gene_names)

    scores = np.asarray(cell_scores, dtype=float)
    perts = np.asarray([str(x) for x in perturbations])
    donor_arr = np.asarray([str(x) for x in donors])
    if scores.shape[0] != perts.shape[0] or scores.shape[0] != donor_arr.shape[0]:
        raise ValueError("perturbations, donors and cell scores must be aligned")
    if control not in set(perts.tolist()):
        raise ValueError(f"control label {control!r} not found in perturbations")

    # Vectorized per-(perturbation x donor) means via integer group codes — pure
    # numpy (bincount), so this scales to millions of cells / thousands of
    # perturbations while producing exactly the per-donor deltas the loop above
    # computed (donors sorted; unseen-donor control falls back to the pooled mean).
    uperts, pcode = np.unique(perts, return_inverse=True)
    udon, dcode = np.unique(donor_arr, return_inverse=True)
    n_p, n_d = uperts.shape[0], udon.shape[0]
    combo = pcode * n_d + dcode
    g_sum = np.bincount(combo, weights=scores, minlength=n_p * n_d).reshape(n_p, n_d)
    g_cnt = np.bincount(combo, minlength=n_p * n_d).reshape(n_p, n_d)
    with np.errstate(invalid="ignore", divide="ignore"):
        g_mean = g_sum / g_cnt

    ctrl_row = int(np.where(uperts == control)[0][0])
    global_ctrl_mean = float(g_sum[ctrl_row].sum() / max(g_cnt[ctrl_row].sum(), 1))
    ctrl_ref = np.where(g_cnt[ctrl_row] > 0, g_mean[ctrl_row], global_ctrl_mean)

    results: list[DirectionResult] = []
    for pi in range(n_p):
        if pi == ctrl_row:
            continue
        present = g_cnt[pi] > 0
        if not present.any():
            continue
        deltas = g_mean[pi, present] - ctrl_ref[present]
        direction_score = float(deltas.mean())
        agg_sign = np.sign(direction_score)
        agreement = bool(agg_sign != 0 and np.all(np.sign(deltas) == agg_sign))
        p = str(uperts[pi])
        via = viability.get(p) if viability is not None else None
        results.append(
            DirectionResult(
                perturbation=p,
                direction_score=direction_score,
                tier=assign_tier(direction_score, via, tau, viability_floor),
                donor_sign_agreement=agreement,
                n_donors=int(present.sum()),
                per_donor_scores=tuple(round(float(x), 6) for x in deltas),
            )
        )
    return results


def direction_dataframe(results: Sequence[DirectionResult]) -> "object":
    """Convert results to a pandas DataFrame (lazy import; not needed for smoke)."""
    import pandas as pd

    return pd.DataFrame([r.as_dict() for r in results])


def run_direction(
    adata: "object",
    ranked_df: "object",
    pert_key: str = "perturbation",
    donor_key: str = "donor",
    control: str = "NT",
    tau: float = DIRECTION_TAU,
    viability_floor: float = VIABILITY_FLOOR,
) -> "object":
    """Claude Science entry point: score direction and merge into the ranked CSV.

    Reuses ``viability_ratio`` from ``ranked_df`` (from ``run_pipeline``) so the
    ``required-machinery`` split reflects the same fitness signal the leaderboard
    already computed. Returns ``ranked_df`` with the ``direction_*`` columns.
    """
    cell_scores = compute_cell_direction_scanpy(adata)
    perts = adata.obs[pert_key].astype(str).to_numpy()
    if donor_key in adata.obs:
        donors = adata.obs[donor_key].astype(str).to_numpy()
    else:
        donors = np.full(adata.n_obs, "all")
    viability = None
    if "viability_ratio" in ranked_df.columns:
        viability = dict(
            zip(ranked_df["perturbation"].astype(str), ranked_df["viability_ratio"])
        )
    results = score_direction(
        perts,
        donors,
        control=control,
        cell_scores=cell_scores,
        viability=viability,
        tau=tau,
        viability_floor=viability_floor,
    )
    return ranked_df.merge(direction_dataframe(results), on="perturbation", how="left")


def _smoke() -> None:
    """Numpy-only self-test: recover the SIGN of known perturbations."""
    rng = np.random.default_rng(0)
    n_bg = 23  # 10 cytotoxic + 7 exhaustion + 23 background = 40 genes
    gene_names = (
        list(CYTOTOXIC_GENES) + list(EXHAUSTION_GENES) + [f"BG{i}" for i in range(n_bg)]
    )
    cyto_cols = list(range(0, len(CYTOTOXIC_GENES)))
    exh_cols = list(range(len(CYTOTOXIC_GENES), len(CYTOTOXIC_GENES) + len(EXHAUSTION_GENES)))

    def block(n: int, kind: str) -> np.ndarray:
        mat = rng.normal(1.0, 0.2, (n, len(gene_names)))
        if kind == "cyto_up":  # KO drives the cytotoxic program => a brake
            mat[:, cyto_cols] += 2.0
        elif kind == "exh_up":  # KO drives exhaustion => an enhancer
            mat[:, exh_cols] += 2.0
        return mat

    plan = (
        ("NT", "ctrl", 80),
        ("BRAKEGENE", "cyto_up", 60),
        ("ENHGENE", "exh_up", 60),
        ("NEUTRALGENE", "ctrl", 60),
    )
    mats, perts, donors = [], [], []
    for donor in ("d1", "d2"):  # two donors => exercise sign agreement
        for name, kind, n in plan:
            mats.append(block(n, kind))
            perts += [name] * n
            donors += [donor] * n
    expr = np.vstack(mats)

    viability = {"BRAKEGENE": 1.3, "ENHGENE": 1.0, "NEUTRALGENE": 1.0}
    results = score_direction(
        np.array(perts),
        np.array(donors),
        control="NT",
        expr=expr,
        gene_names=gene_names,
        viability=viability,
    )
    by = {r.perturbation: r for r in results}
    for name in ("BRAKEGENE", "ENHGENE", "NEUTRALGENE"):
        r = by[name]
        print(
            f"{name:12s} direction_score={r.direction_score:+.3f} "
            f"tier={r.tier:18s} sign_agree={r.donor_sign_agreement} "
            f"n_donors={r.n_donors}"
        )

    # (1) sign recovery — the core assertion
    assert by["BRAKEGENE"].direction_score > 0, "cytotoxic-up KO must score positive"
    assert by["ENHGENE"].direction_score < 0, "exhaustion-up KO must score negative"

    # (2) tier mapping
    assert by["BRAKEGENE"].tier == TIER_BRAKE, by["BRAKEGENE"].tier
    assert by["ENHGENE"].tier == TIER_ENHANCER, by["ENHGENE"].tier
    assert by["NEUTRALGENE"].tier == TIER_NEUTRAL, by["NEUTRALGENE"].tier

    # (3) both donors agree on the sign of the two real effects
    assert by["BRAKEGENE"].donor_sign_agreement, "donors should agree (brake)"
    assert by["ENHGENE"].donor_sign_agreement, "donors should agree (enhancer)"
    assert by["BRAKEGENE"].n_donors == 2 and by["ENHGENE"].n_donors == 2

    # (4) viability split on the loss-of-effector side (direct tier logic)
    assert assign_tier(-0.5, viability_ratio=0.4) == TIER_REQUIRED
    assert assign_tier(-0.5, viability_ratio=1.0) == TIER_ENHANCER
    assert assign_tier(+0.5, viability_ratio=1.3) == TIER_BRAKE
    assert assign_tier(0.0) == TIER_NEUTRAL

    print("SMOKE TEST PASSED  (direction sign recovered; tiers + sign-agreement correct)")


if __name__ == "__main__":
    _smoke()
