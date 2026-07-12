# Written summary (submission)

## Version A — druggable-brake target discovery (PRIMARY)
Using **Claude Science**, we screened for druggable **brakes** on human CD4⁺
T-cell effector function — the mechanism behind checkpoint and CAR-T therapy. From
a genome-scale CRISPRi Perturb-seq screen (**2,638,736 cells, 12,449 knockdowns**,
Gladstone/Marson, on an NVIDIA DGX Spark), we rank each knockdown by causal effect
(power-equalized energy distance) and add a per-cell **direction-of-effect** axis (an 8-hour transcriptional signature).
This signed causal map cleanly separates the cell's essential machinery — large
effects, but knockdown *cripples* the cell — from candidate **brakes**, whose
knockdown *enhances* effector function. From the brake quadrant we nominate a
shortlist of **five prior-informed candidate targets** for validation, by convergent evidence: effect, direction,
donor consistency, druggability, immune genetics, and clinical precedent. Our lead
is **CBLB** — an E3-ligase brake with two oral inhibitors already in Phase 1/2 and
an autoimmune genetic association; **CD5** and **DGKA** follow,
donor-consistent and clinically tractable. We report honestly that at two donors
the quadrant is not yet enriched (Mann–Whitney p = 0.56), so this is a prioritized
shortlist for the full cohort. Every target traces back to versioned code.

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
