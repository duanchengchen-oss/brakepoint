# Written summary (submission)

Using **Claude Science**, we screened for candidate **brakes** on human CD4⁺
T-cell function — the target class behind checkpoint-blockade immunotherapy,
scoring each target's druggability separately. From a
genome-scale CRISPRi Perturb-seq screen (**2,638,736 cells, 12,449 knockdowns**,
Gladstone/Marson; two of four donors), we build a **signed causal map** of T-cell
function and prioritize a target shortlist from it.

**Why the method is different.** A significance-first Perturb-seq analysis ranks
perturbations by statistical significance — but at this scale, **97.5%** of the 11,438 tested
knockdowns clear q < 0.05, so significance ranks almost nothing. We instead rank by
**causal effect size** (power-equalized energy distance; the permutation test is
only a gate), and add the sign that an unsigned effect-size ranking omits: a
per-cell **direction-of-effect** score (an 8-hour effector-minus-checkpoint
transcriptional read-out, not a functional assay). Magnitude alone nominates the
cell's own activation machinery; the signed axis reclassifies it — 14 of the 15
largest effects are direction-negative required machinery, and every evaluated
TCR-module gene is donor-consistent — and surfaces candidate brakes in the positive
quadrant.

From there we prioritize **five prior-informed candidates for validation** — CBLB,
CD5, DGKA, SMAD3, UBASH3A — evaluated by convergent evidence (effect, direction,
donor consistency, viability, druggability, immune genetics, clinical precedent). Lead
**CBLB**: inhibitors in early-phase trials (NX-1607, HST-1011) and an autoimmune
genetic association.

We report honestly: at two donors the positive quadrant shows **no significant
brake-enrichment** (one-sided Mann–Whitney, p = 0.70), and three of the five
candidates are donor-split — so this is a prioritized hypothesis for the full
four-donor cohort, not a finished target list. Every result is versioned,
reproducible code, and an adversarial self-check caught a real n-dependent bias in
our effect-size computation before it reached a single figure.
