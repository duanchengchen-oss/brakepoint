# Target-matrix score provenance (`figure_targets.py`)

The convergent-evidence matrix is a **curated evidence summary (0–1 per axis), not a
fitted or weighted model**, and not a computed rank. This file documents the basis of
every score so each cell is traceable. Four axes are **data-derived** from the genome-
scale leaderboard (`outputs_gladstone/ranked_perturbations.csv`); three are **curated**
subjective tiers from the MCP-verified dossiers (`dossiers/*.json`: Open Targets, ChEMBL
v34, ClinicalTrials.gov v2) and the literature. Curation was done from prior biology, so
the matrix is an **exploratory prioritization**, not a validated ranking. Raw data values
are kept beside the transformed scores below so nothing is hidden behind a transform.

## The actual scored matrix (values as coded in `figure_targets.py`)
Order of axes: **Causal effect · Brake direction · Donor consistency · Viability (fitness)
· Druggability · Immune genetics · Clinical precedent** (each 0–1; larger dot = stronger).

| Gene | Causal effect | Brake direction | Donor consistency | Viability | Druggability | Immune genetics | Clinical precedent | Call |
|---|---|---|---|---|---|---|---|---|
| **CBLB** | 0.88 | 0.72 | 0.35 | 0.55 | 1.00 | 0.90 | 0.90 | LEAD · clinical (external) |
| **CD5** | 0.87 | 0.75 | 1.00 | 0.90 | 0.70 | 0.50 | 0.40 | SCREEN-CONSISTENT |
| **DGKA** | 0.71 | 0.42 | 1.00 | 0.78 | 1.00 | 0.25 | 0.85 | SCREEN-CONSISTENT |
| **SMAD3** | 0.92 | 0.32 | 0.35 | 0.90 | 0.60 | 0.45 | 0.55 | EXPLORATORY |
| **UBASH3A** | 0.40 | 0.28 | 0.35 | 0.82 | 0.55 | 0.90 | 0.15 | GENETICS-LED |

These 0–1 values are a **presentation encoding of the evidence tiers**, not measured
probabilities; they are not summed or weighted into a composite. Read each row across, not
as a total.

## Axis definitions and transforms
| Axis | Type | Source / rule (with the exact transform) |
|---|---|---|
| Causal effect | data | percentile of `e_distance` among the **11,438 tested** perturbations (denominator = tested set), mapped to 0–1 |
| Brake direction | data | `direction_score` (positive side) linearly scaled to the observed positive range — **outlier-sensitive** (a single extreme positive rescales the axis); read with the raw value below |
| Donor consistency | data | **categorical annotation**, not a confidence: **1.0** = both donors agree in sign, **0.35** = donor-split (the 0.35 is a display heuristic, not a probability) |
| Viability (fitness) | data | closeness of `viability_ratio` to 1.0, where `viability_ratio` = (perturbation cell count) ÷ (median perturbation count) — a **relative-abundance depletion proxy, NOT therapeutic safety**; the closeness-to-1 mapping is a subjective tier |
| Druggability | curated | subjective tractability tier from the dossier / literature (see per-target split below) |
| Immune genetics | curated | subjective autoimmune-GWAS / Open-Targets association strength |
| Clinical precedent | curated | max phase of a modulator of the target **or its pathway** — see the direct-vs-pathway split below |

## Evidence-type separation (do not blur these)
The curated axes deliberately keep distinct kinds of evidence apart, because "a drug
exists" can mean very different things:
- **Direct-target tractability + direct clinical precedent** (matching intervention
  direction: inhibition to release the brake): CBLB (CBL-B inhibitors NX-1607, HST-1011),
  DGKA (DGKα inhibitor BAY2862789). These score high on both druggability and clinical
  precedent.
- **Pathway-level precedent, not direct-target** (flagged, scored lower/EXPLORATORY):
  SMAD3 — the TGF-β pathway is heavily drugged, but SMAD3 itself is not a validated direct
  drug target; its clinical-precedent score reflects **pathway** precedent only.
- **Different modality** (not systemic pharmacological inhibition): CD5 — addressed to date
  as a CAR antigen / ex-vivo deletion, not a systemic inhibitor; clinical precedent scored
  LOW deliberately and the enhancement data are **preclinical**.
- **Genetic evidence without validated chemical matter**: UBASH3A — strong T1D/RA GWAS
  association, but **tractability is unestablished; no validated small-molecule or biologic
  chemical matter is cited** (GENETICS-LED). Do not read its druggability tier as a drugged
  target.

## Per-target sources (data columns are exact from the CSV)
- **CBLB** — E-dist 6.43 (rank 439; ~88th pct), dir +0.14 (**donor-split** +0.44/−0.15),
  viab 0.56, kd-gated. Druggability/clinical: oral CBL-B inhibitors **NX-1607** (Ph1,
  NCT05107674) and **HST-1011** (Ph1/2, NCT05662397) — the *inhibitors* are in trials, not
  CBLB itself. Genetics: CBLB is a published autoimmune-risk gene (RA/T1D); the matrix
  scores the *association*, not a specific causal variant (no variant-to-gene fine-mapping
  claimed).
- **CD5** — E-dist 5.64 (rank 583; ~87th pct), dir +0.15 (**donor-consistent** +0.15/+0.14),
  viab 1.38, kd-gated. Druggability: cell-surface (biologic/engineered). Clinical precedent
  scored LOW: CD5-directed CAR-T targets CD5 as a *tumour antigen* (different modality); CD5
  deletion enhancing CAR-T function is **preclinical**.
- **DGKA** — E-dist 2.50 (rank 2,579; ~71st pct), dir +0.08 (**donor-consistent** +0.09/+0.07),
  viab 0.87, kd-gated. Druggability/clinical: **BAY2862789** oral DGKα inhibitor, Ph1
  (NCT05858164).
- **SMAD3** — E-dist 25.1 (rank 21; ~92nd pct), dir +0.06 (**donor-split** −0.13/+0.26),
  viab 1.37, kd-gated. TGF-β **pathway** is heavily drugged (pathway-level precedent only).
  No per-gene dossier file; external scores are literature-curated (flagged EXPLORATORY).
- **UBASH3A** — E-dist 2.03 (rank 3,579), dir +0.05 (**donor-split** −0.08/+0.19), viab 0.88,
  kd-gated. Genetics: T1D/RA GWAS gene (strong). Druggability: histidine-phosphatase;
  **tractability unestablished, undrugged, no validated chemical matter cited** (GENETICS-LED).

## Honest limitations (see also `real-finding-genomescale.md`)
- The three curated axes are **subjective 0–1 tiers**, not measured quantities; the numeric
  values are a display encoding, not a model output.
- **Donor consistency is categorical** (both-agree vs donor-split); the 0.35 for donor-split
  is a display heuristic, not a pseudo-quantitative confidence.
- **Brake-direction scaling is outlier-sensitive**; always read the raw `direction_score`
  (given per target above) alongside the scaled dot.
- SMAD3 lacks a per-gene dossier; its external axes are literature estimates.
- The "Call" (LEAD / SCREEN-CONSISTENT / EXPLORATORY / GENETICS-LED) reflects the **basis of
  support, not a computed rank**: CBLB leads on *external* (clinical + genetics) evidence but
  is donor-split in the screen; CD5/DGKA are the most *screen-consistent* (donor-concordant);
  SMAD3/UBASH3A are exploratory. No axis-weighting or composite score is claimed.
