# Written summary (submission)

## Version A — the signed causal map (PRIMARY) — ~180 words
Using **Claude Science**, we built a reproducible pipeline that turns a
genome-scale CRISPRi Perturb-seq screen into a **signed causal map** of human
CD4⁺ T-cell function. On **2,638,736 primary human T cells** (12,449 knockdowns,
scVI donor-integrated, run on an NVIDIA DGX Spark), we rank perturbations by
**causal effect size** — power-equalized energy distance with a permutation test —
then add the axis magnitude cannot supply: a per-cell **direction-of-effect**
score (an effector program versus a dysfunction program). The map validates itself
in both axes. Unsupervised, the largest effects are the entire TCR-signalling
module; the direction axis then correctly flags **14 of the top 15 as required
machinery** whose knockdown *cripples* the cell — not drug targets. The
therapeutic signal is the opposite quadrant, where the map recovers canonical
immune **brakes** (CD5, DGKA, CBLB) whose knockdown *enhances* effector function.
We report donor consistency honestly (2 donors). Every artifact carries Claude
Science provenance and a reviewer trail — which caught a real statistical bug
before any figure. One command reproduces the map.

_(167 words — inside the 100–200 window.)_

## Version B — public-data fallback (Shifrut CD8; ~150 words)
Using Claude Science, we built a reproducible pipeline that ranks CRISPR-KO
perturbations in **primary human CD8⁺ T cells** (Shifrut/Marson, ~25,000 cells) by
**causal effect size** — power-equalized energy distance with a permutation test —
gated on viability, on-target effect, and donor replication, with a
direction-of-effect axis as the differentiator. Unsupervised, the ranking recovers
the TCR-signalling core (CD3D, LCP2) and re-nominates **RASA2**, a
Nature-2022-validated CAR-T potency enhancer, purely from effect size. The
direction axis separates the essential machinery from the therapeutic **brake**
class, where the lead is **CBLB** — an immune brake with two oral inhibitors
already in clinical trials. Every artifact carries Claude Science provenance and a
reviewer trail; one command reproduces the ranking and figures.

_Pick A (genome-scale signed map — the strongest, self-validating result). B is a
safe public-data fallback._
