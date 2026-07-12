# Target-matrix score provenance (`figure_targets.py`)

The convergent-evidence matrix is a **curated evidence summary (0–1 per axis), not
a fitted or weighted model**. This file documents the basis of every score so each
cell is traceable. Four axes are **data-derived** from the genome-scale leaderboard
(`outputs_gladstone/ranked_perturbations.csv`); three are **curated** from the
MCP-verified dossiers (`dossiers/*.json`: Open Targets, ChEMBL v34,
ClinicalTrials.gov v2). Curation was done from prior biology, so the matrix is an
**exploratory prioritization**, not a validated ranking.

## Axis definitions
| Axis | Type | Source / rule |
|---|---|---|
| Causal effect | data | percentile of `e_distance` among all tested perturbations |
| Brake direction | data | `direction_score` (positive), scaled to the observed positive range |
| Donor consistency | data | `direction_sign_agreement` (1.0 = both donors agree; 0.35 = donor-split) |
| Viability (fitness) | data | closeness of `viability_ratio` to 1.0 (NOT therapeutic safety) |
| Druggability | curated | tractability tier from the dossier / literature |
| Immune genetics | curated | autoimmune GWAS / Open-Targets association strength |
| Clinical precedent | curated | max phase of a modulator of the target (or its pathway) |

## Per-target sources (data columns are exact from the CSV)
- **CBLB** — E-dist 6.43 (88th pct), dir +0.14 (donor-split +0.44/−0.15), viab 0.56, kd-gated. Druggability/clinical: oral CBL-B inhibitors **NX-1607** (Ph1, NCT05107674) and **HST-1011** (Ph1/2, NCT05662397) — the inhibitors are in trials, not CBLB itself. Genetics: CBLB is a published autoimmune-risk gene (RA/T1D); the matrix scores the *association*, not a specific causal variant.
- **CD5** — E-dist 5.64 (87th pct), dir +0.15 (donor-consistent +0.15/+0.14), viab 1.38, kd-gated. Druggability: cell-surface (biologic/engineered). Clinical precedent scored LOW: CD5-directed CAR-T targets CD5 as a *tumour antigen* (different modality); CD5 deletion enhancing CAR-T function is **preclinical**.
- **DGKA** — E-dist 2.50 (71st pct), dir +0.08 (donor-consistent +0.09/+0.07), viab 0.87, kd-gated. Druggability/clinical: **BAY 2862789** oral DGKα inhibitor, Ph1 completed (NCT05858164).
- **SMAD3** — E-dist 25.1 (92nd pct), dir +0.06 (donor-split −0.13/+0.26), viab 1.37, kd-gated. TGF-β pathway is heavily drugged (pathway-level precedent). No dossier file; external scores are literature-curated (flagged EXPLORATORY).
- **UBASH3A** — E-dist 2.03, dir +0.05 (donor-split −0.08/+0.19), viab 0.88, kd-gated. Genetics: T1D/RA GWAS gene (strong). Druggability: histidine-phosphatase, tractable but **undrugged** (GENETICS-LED).

## Honest limitations (see also `real-finding-genomescale.md`)
- The three curated axes are subjective 0–1 tiers, not measured quantities.
- SMAD3 lacks a per-gene dossier; its external axes are literature estimates.
- The "Call" (LEAD / SCREEN-CONSISTENT / EXPLORATORY / GENETICS-LED) reflects the
  basis of support, not a computed rank: CBLB leads on *external* (clinical +
  genetics) evidence; CD5/DGKA are the most *screen-consistent*.
