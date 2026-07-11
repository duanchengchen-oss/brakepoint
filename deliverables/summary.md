# Written summary (submission)

## Version A — the signed causal map (PRIMARY)
Using **Claude Science**, we built a reproducible pipeline that turns a
genome-scale CRISPRi Perturb-seq screen into a **signed causal map** of human
CD4⁺ T-cell function. On **2,638,736 primary human T cells** (12,449 knockdowns,
scVI donor-integrated, run on an NVIDIA DGX Spark), we rank perturbations by
**causal effect size** — power-equalized energy distance with a permutation test —
then add the axis magnitude cannot supply: a per-cell **direction-of-effect**
score (an effector program versus a dysfunction program). The map validates
itself: unsupervised, 8 of the 9 largest effects are the TCR-signalling module,
and the direction axis correctly flags **14 of the top 15 as required machinery**
whose knockdown *cripples* the cell — not drug targets, donor-consistently. That
is the load-bearing result. The opposite, positive quadrant is the therapeutic
hypothesis space; we report it honestly — at two donors it is not yet enriched for
known brakes (p = 0.56), though brakes like CD5 and DGKA do land there. Every
artifact carries Claude Science provenance and a reviewer trail, which caught a
real statistical bug before any figure. One command reproduces the map.

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
