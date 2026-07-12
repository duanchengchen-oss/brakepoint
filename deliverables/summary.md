# Written summary (submission)

Using **Claude Science**, we screened for druggable **brakes** on human CD4⁺
T-cell function — the target class behind checkpoint-blockade therapy (CAR-T,
separately, is engineered antigen recognition that brake-removal can further
enhance). From a genome-scale CRISPRi Perturb-seq screen (**2,638,736 cells,
12,449 knockdowns**, Gladstone/Marson; two of four donors), we rank each knockdown
by causal effect (power-equalized energy distance) and add a per-cell
**direction-of-effect** score — an 8-hour effector-minus-checkpoint transcriptional
readout, not a functional assay. The signed map separates the cell's
activation-required machinery (large effects whose knockdown *cripples* the cell)
from candidate **brakes** (knockdown shifts cells toward the effector program). As
a strong internal consistency check, the largest, donor-consistent effects are the
TCR machinery, correctly scored negative. From the positive region we prioritize
**five candidate targets for validation** — CBLB, CD5, DGKA, SMAD3, UBASH3A — by
convergent evidence (effect, direction, donor consistency, viability, druggability,
genetics, clinical precedent). Lead **CBLB**: its inhibitors are in early-phase
trials and its human genetics are autoimmune-associated. We report honestly that at
two donors the region shows **no significant brake-enrichment** (p = 0.56), so this
is a prioritized hypothesis for the full cohort. Every candidate traces back to
versioned, reproducible code.
