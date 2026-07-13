# Written summary (submission)

Using **Claude Science**, we mine an existing genome-scale CRISPRi Perturb-seq
screen (**2,638,736 cells, 12,449 knockdowns**; Gladstone/Marson, two of four
donors) for **brakes** on human CD4⁺ T-cell function — the class
checkpoint-blockade drugs target. We build a **signed causal map** and
prioritize a shortlist from it.

The method is the point. At 2.6 million cells, 97.5% of tested knockdowns clear
q < 0.05, so we rank by **causal effect size** (power-equalized energy distance),
not p-value, then add a per-cell **direction-of-effect** score a magnitude ranking
omits (an 8-hour transcriptional read-out, not a functional assay). Magnitude alone
nominates the cell's own machinery; the signed axis reclassifies it (14 of the 15
largest effects are direction-negative required machinery) and surfaces
**candidate brakes**.

We put forward five prior-informed candidates — CBLB, CD5, DGKA, SMAD3, UBASH3A —
by convergent evidence; lead **CBLB** has oral inhibitors in early-phase trials.
What it positively establishes: the machinery reads negative in both donors and
**CBLB** — with donor-consistent CD5 and DGKA — lands positive, so the 29-gene null
(p = 0.70) marks two-donor **power**, not these calls. Three of five
are donor-split: a prioritized hypothesis for the full cohort, not a finished list.
Every result is versioned, reproducible code.
