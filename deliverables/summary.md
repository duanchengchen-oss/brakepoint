# Written summary (submission)

Using **Claude Science**, we screened for **brakes** on human CD4⁺ T-cell function
— the target class checkpoint-blockade immunotherapy drugs. From a genome-scale
CRISPRi Perturb-seq screen (**2,638,736 cells, 12,449 knockdowns**; Gladstone/Marson,
two of four donors), we build a **signed causal map** and prioritize a shortlist
from it.

The method is the point. At two million cells, 97.5% of tested knockdowns clear
statistical significance — so we rank by **causal effect size** (power-equalized
energy distance), not p-value, then add the axis a magnitude ranking omits: a
per-cell **direction-of-effect** score (an 8-hour transcriptional read-out, not a
functional assay). Magnitude alone nominates the cell's own signaling machinery;
the signed axis reclassifies it — 14 of the 15 largest effects are
direction-negative required machinery — and surfaces **candidate brakes**.

We put forward five prior-informed candidates — CBLB, CD5, DGKA, SMAD3, UBASH3A —
by convergent evidence; lead **CBLB** has oral inhibitors in early-phase trials.
Reported honestly: at two donors the positive quadrant shows **no significant
enrichment** (Mann–Whitney p = 0.70) and three of five are donor-split — a
prioritized hypothesis for the full cohort, not a finished list. Every result is
versioned, reproducible code.
