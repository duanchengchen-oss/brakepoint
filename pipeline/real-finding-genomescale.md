# REAL FINDING — druggable-brake target discovery in CD4⁺ T cells

**Deliverable:** a shortlist of **five prior-informed candidate targets** (candidate brakes; druggability varies — CBLB/DGKA clinical, UBASH3A undrugged) on human CD4⁺ T-cell
effector function (lead **CBLB**; also **CD5, DGKA, SMAD3, UBASH3A**), nominated by
convergent evidence and scored in `figure_targets.py`. The signed causal map below
is the *discovery engine*; the target shortlist is the *output*. Honesty caveats
(2 donors; no significant enrichment of the positive quadrant, p=0.70) are kept throughout.

## The engine — a genome-scale *signed* causal map of CD4⁺ T-cell function

Real Claude Science run on the DGX Spark (NVIDIA GB10), verified end-to-end. Full
methods and honest caveats below.

## The one-line finding
On this genome-scale screen, ranking CRISPRi knockdowns by **causal
effect size alone cannot tell a drug target from the cell's own machinery** — 8 of
the 9 largest effects are the TCR signalling module. Adding a **signed
direction-of-effect axis** splits the map: those top effects are all strongly
**negative** (knockdown *cripples* the effector program → required machinery),
donor-consistently. That machinery→negative result is the **load-bearing internal
consistency check** — in both magnitude and sign (a sanity check, not external validation). The **positive** quadrant (knockdown *enhances* the effector transcriptional program) is the
therapeutic hypothesis space — presented honestly: at 2 donors it is noisy and
shows **no significant evidence of enrichment** for a curated known-brake set (p = 0.70), so it is a
prioritized space for the full cohort, not a finished target list.

## The run
- **Data:** genome-scale CRISPRi Perturb-seq, **primary human CD4⁺ T cells**
  (Marson lab / Gladstone; CZI Virtual Cells Platform). Donors **D1 + D2**,
  condition **Stim 8 h**. Control = non-targeting guides (`control`).
- **Scale:** dataset **2,638,736 cells** × 4,816 measured HVGs; **12,449 perturbations**
  (11,438 with ≥30 cells tested). The E-distance ranking used 2,436,881 post-QC/
  subsampled cells; the direction axis scored all 2,638,736. scVI latent (`X_scVI`).
- **Axis 1 — magnitude:** power-equalized **E-distance** on `X_scVI` +
  1,000-permutation E-test; gates: permutation q<0.05, viability, and the
  authors' per-guide knockdown-efficiency sidecar.
- **Axis 2 — sign:** per cell, `mean(log-norm effector genes) − mean(log-norm
  dysfunction genes)`, aggregated per (perturbation × donor) vs control (donors as
  a per-donor sign-agreement flag; donor-stratified, no donor-level population inference). This is an 8-hour transcriptional readout, NOT a functional assay — functional validation is required before calling any nominee a brake. Effector program = IFNG, IL2,
  TNF, CSF2, LTA, XCL1/2, CCL3/4, GZMB, TNFRSF9, CD69, MYC, IRF4, BATF, TBX21;
  dysfunction program = PDCD1, CTLA4, LAG3, HAVCR2, TIGIT, BTLA, CD160, VSIR,
  ENTPD1, TOX, NR4A1/2/3. `direction_score > 0` ⇒ knockdown pushes cells toward
  the effector program (a *candidate brake* — a transcriptional shift, not proven function); `< 0` ⇒ toward loss of that program.
  Code: `direction.py`, `direction_genomescale.py`, `merge_direction.py`.

## Validation — a strong internal consistency check (both axes)
1. **Magnitude (unsupervised):** the top of the leaderboard is dominated by the
   canonical TCR proximal-signalling module. **8 of the 9 largest effects** are
   TCR-proximal genes — ZAP70, LCP2, CD3E, CD3G, PLCG1, LAT, VAV1, CD3D; the one
   exception (rank 8, **SMARCD3**, a SWI/SNF chromatin-remodeler) is a
   high-toxicity dropout (viability 0.16). The rest of the module — CD247, ITK,
   RASGRP1 — sits just below (ranks ~15–17). Recovering known biology as the largest effects is one internal consistency check
   (magnitude); that those same effects fall on the negative/machinery side is a
   separate one (sign). Neither is external validation.
2. **Sign (the key result):** **14 of the 15 largest-effect knockdowns have a
   negative direction score**, and every TCR-module gene is **donor-consistent**
   (both donors strongly negative: e.g. ZAP70 −0.63, LCP2 −0.76, CD3D −0.66, LAT
   −0.64). Magnitude alone would headline the cell's own activation machinery; the
   sign axis correctly reclassifies it as **activation-required — unsuitable inhibition targets for this objective.**
   This machinery→negative direction is the load-bearing internal consistency check.

## The therapeutic signal — the positive (brake) quadrant, reported honestly
Knockdowns that *raise* the effector program are the candidate class. Several
literature-known immune **brakes** land in this quadrant and are donor-consistent —
a useful consistency check:

| Gene | E-distance | direction | donor-consistent? | note |
|---|---|---|---|---|
| **CD5** | 5.6 | +0.15 | **yes** (+0.15 / +0.14) | inhibitory co-receptor; KD de-represses TCR signalling |
| **DGKA** | 2.5 | +0.08 | **yes** (+0.09 / +0.07) | DAG kinase brake; DGKα inhibitors are an IO strategy |
| **CBLB** | 6.4 | +0.14 | no (+0.44 / −0.15) | E3-ligase brake; investigational CBL-B inhibitors NX-1607 (Ph1), HST-1011 (Ph1/2) |
| **SMAD3** | 25.1 | +0.06 | no (−0.13 / +0.26) | TGF-β pathway node (pathway-level candidate); the highest-E-distance *biologically-coherent* positive node |
| **UBASH3A** | 2.0 | +0.05 | no (−0.08 / +0.19) | autoimmune-GWAS (T1D/RA) phosphatase; putatively tractable, no drug yet (genetics-led) |

*(These five are the curated target shortlist scored in `figure_targets.py`. A
further high-E-distance positive, **LAT2** (E 23.0, +0.20, donor-split), is a
raw candidate but less druggable/characterized, so it is not in the shortlist.)*

**The critical honest caveat — we do not overclaim the positive side.** Two
things must be stated plainly:
1. **The positive quadrant shows no significant brake-enrichment at this scale.** A curated set of
   29 known T-cell negative regulators (CBLB, CBL, DGKA/Z, TNFAIP3, SOCS1/3, CISH,
   PTPN2/6, RASA2/3, UBASH3A, MAP4K1, TET2, …; scoring-module genes excluded to
   avoid circularity) shows **no significant evidence of a positive shift vs background** (one-sided
   Mann–Whitney **p = 0.70**; 37.9% vs 36.7% positive, against a matched 2-donor kd-gated background).
   The genes above were selected by prior biology and are a **consistency check,
   not a method-level enrichment result.**
2. **The raw top of the positive quadrant is dominated by likely artifacts** — the
   highest-E-distance positive-direction hits include CFAP298 (a cilia gene) and
   germ-cell/chromatin genes, not credible CD4 brakes. So SMAD3 is the
   highest-magnitude *coherent* brake, not the highest positive overall.

**What this means.** The **load-bearing result is the machinery axis** (an internal consistency check)
(14/15 largest effects negative; the TCR module among them is donor-consistent — magnitude alone would mislead).
The **positive/brake side is a noisy hypothesis space at 2 donors / Stim-8 h**: the
donor-consistent brakes (CD5, DGKA) are low-magnitude, the higher-magnitude ones
(SMAD3, LAT2, CBLB) are donor-split, and the set as a whole shows no significant enrichment. The
honest deliverable is a **reproducible signed-map method + a prioritized hypothesis
space** that the full 4-donor / Stim-48 h cohort will test for improved robustness
and enrichment — not a finished target list. (Enrichment recomputes via `pipeline/brake_enrichment.py`.)

## IL2RB — a non-shortlisted note
An independent network layer (STRING diffusion) flagged **IL2RB** (CD122), but its knockdown shows severe viability loss (0.13) and negative direction, so it is a pathway node, not a shortlisted brake; the therapeutic angle there would be IL-2/CD122 **agonism** (aldesleukin, N-803), not inhibition. It is excluded from the shortlist.


## Honest caveats (state these)
1. **No Gladstone-provided interaction network or regulatory model exists.** The
   provided data share is Perturb-seq expression + a genome-wide DESeq2 DE result
   + supplementary signature/validation tables (per `data_sharing_readme.md`).
   **STRING v12 and Open Targets are legitimate *public* layers on top of the
   provided data — not substitutes for withheld provided data.** (Earlier drafts
   miscalled them "substitutes for a provided PPI/regulatory model"; corrected.)
   The provided DESeq2 DE and Th1/Th2 polarization tables were not pulled to the
   workstation; corroborating the ranking against them is the obvious next step.
2. **2 of 4 donors, Stim 8 h only** (compute-budget scope). This is exactly why the
   brake shortlist is caveated by donor consistency; the full cohort sharpens it.
3. **Perturbations of the module genes themselves are excluded from brake
   nominations** — knocking down PDCD1/TOX/NR4A/etc. trivially shifts its own pole.
   The featured brakes (CD5, DGKA, CBLB, SMAD3, UBASH3A) are not module genes.
4. **Ranking = E-distance magnitude**; permutation q is a gate. The
   direction performs the required-vs-enhancer classification; viability is only a
   toxicity annotation/gate (a coarse proxy — e.g. LAT is viable yet clearly
   required — so the figure leans on sign + donor consistency, not viability).
5. **The direction score is an 8-hour transcriptional readout, not a functional
   assay.** It is `mean(log-norm effector) − mean(log-norm dysfunction)`; positive
   nominees require protein/functional validation (cytokine, proliferation,
   killing) before being called brakes. Normalization uses the 4,816-gene measured
   HVG panel as the library size (not the full transcriptome), a known compositional
   caveat; the effector−dysfunction *difference* partially cancels depth effects.
6. **The brake-enrichment test is exploratory** — the 29-gene brake set is a
   curated literature list (not pre-registered); it is used to report a *null*
   (no significant enrichment, p=0.70 vs a matched 2-donor background), an exploratory, descriptive null (post-hoc
   selection can bias inference, so we make no confirmatory claim). The **target matrix is a curated evidence
   summary, not a fitted model** — every score's basis is in
   `target_matrix_provenance.md`.

## Provenance
Every step is a versioned Claude Science artifact (code + environment +
conversation), and a background reviewer checks claims against what actually ran.
Separately, an adversarial self-critique pass reproduced and caught a real
diagonal-bias bug in the E-distance implementation before any figure. Heavy compute ran on the DGX Spark over SSH; `make smoke` reproduces the
pure-logic core anywhere; `make direction` + `make figure` regenerate the signed
map and the hero figure. Outputs: `outputs_gladstone/ranked_perturbations.csv`
(+ `direction_*`), `direction_meta.json`, `deliverables/figures/causal_map.png`.
