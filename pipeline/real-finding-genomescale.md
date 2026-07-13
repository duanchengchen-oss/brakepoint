# REAL FINDING — a signed prioritization of candidate T-cell brakes in CD4⁺ T cells

**Deliverable:** five **prior-informed, literature-supported candidate brakes** on
human CD4⁺ T-cell effector function — **CBLB, CD5, DGKA, SMAD3, UBASH3A** —
**prioritized by a computational re-analysis of the public Marson (Gladstone) +
Pritchard (Stanford) genome-scale CD4⁺ T-cell CRISPRi screen** (prior-informed and
re-ranked by the screen, not discovered de novo). Druggability
varies and is *not* uniform: CBLB/DGKA have clinical-stage inhibitors, CD5 is a
cell-surface protein addressed to date only as a CAR/deletion (a different modality),
SMAD3 is a **pathway-level** node, and UBASH3A is **undrugged** (genetics-led, no
validated chemical matter). Within the screen, **CD5 and DGKA are the most
donor-concordant**; CBLB is the most clinically advanced prior target but is **donor-
split**. These are **hypotheses for validation, not finished targets**. The signed
map below is the *prioritization engine*; the shortlist (scored in `figure_targets.py`)
is the *output*. Honesty caveats — 2 donors; 3 of the 5 (CBLB, SMAD3, UBASH3A) donor-
split; no significant enrichment of the positive quadrant (one-sided Mann–Whitney
p = 0.70) — are kept throughout.

## The engine — a genome-scale *signed* map of CD4⁺ T-cell perturbation effects

Real Claude Science run on the DGX Spark (NVIDIA GB10), verified end-to-end. Here
"causal/effect" is used in the **interventional** sense — every point is a CRISPRi
*knockdown*, not an observational correlation — but the **read-outs are transcriptional**
(a perturbation distance and an 8-hour program score), **not proven effects on cellular
function**. Full methods and honest caveats below.

**What is and is not novel.** The magnitude statistic — power-equalized **E-distance**
plus a permutation **E-test** — is the **scPerturb / Peidli et al. (Nat Methods 2024)
standard**, implemented as in PertPy; **we claim no new Perturb-seq statistic and no
proof of therapeutic causality.** What is novel here is the **combination**: pairing
that established unsigned distance with a **prespecified, IO-objective-specific signed
direction axis**, a **donor-concordance** requirement, **perturbation QC gating**, and
**external target evidence**, so that magnitude and translational direction are read
together on a genome-scale primary-cell screen.

## The one-line finding
On this genome-scale screen, ranking CRISPRi knockdowns by **effect size alone cannot
tell a drug target from the cell's own machinery** — 8 of the 9 largest effects are the
TCR-signalling module. Adding a **signed direction-of-effect axis** splits the map:
those top effects are all strongly **negative** (knockdown *cripples* the effector
program → required machinery), donor-consistently. That machinery→negative result is a
**positive-control / face-validity check** — in both magnitude and sign (a sanity check,
not external validation, and not a validation of the positive quadrant). The **positive**
quadrant (knockdown *raises* the effector transcriptional program) is the therapeutic
hypothesis space — presented honestly: at 2 donors it is noisy and shows **no significant
evidence of enrichment** for a curated known-brake set (p = 0.70; inconclusive, *not*
evidence of no effect), so it is a prioritized space for the full cohort, not a finished
target list.

## The run
- **Data:** genome-scale CRISPRi Perturb-seq, **primary human CD4⁺ T cells** (Marson lab,
  Gladstone, with the Pritchard lab, Stanford; CZI Virtual Cells Platform, dataset `genome-scale-tcell-perturb-seq`;
  bioRxiv 10.64898/2025.12.23.696273). Build `GWCD4i_Stim8hr_D1D2.built.h5ad`, donors
  **D1 + D2**, condition **Stim 8 h**. Control = non-targeting guides (`control`).
- **Scale:** dataset **2,638,736 cells** × **4,816 measured HVGs** (Ensembl `var_names`);
  **12,449 perturbations**, **11,438 tested** (≥30 cells pooled across both donors; sub-
  threshold perturbations are *surfaced with a depletion flag*, not silently dropped).
  The E-distance leaderboard ran on **2,436,881 QC-passing cells** (the ~202k gap vs the
  full 2.64M is MAD-based QC on counts/genes/%-mito, `pct_mt < 15`); the direction axis
  scored **all 2,638,736** cells. Unit of analysis = **target gene** (guides pooled to the
  gene level; per-guide knockdown efficiency used only for the QC gate).
- **Axis 1 — magnitude (`edistance_core.py`, `run_pipeline.py`):** **E-distance** =
  energy distance in squared-Euclidean form, computed as an **unbiased U-statistic**
  (within-group terms exclude the zero self-distance diagonal, i.e. divide by n(n−1),
  not n²) on the **scVI latent** present in the build (`adata.obsm['X_scVI']`; latent
  supplied in the build, not retrained here). For compute tractability each group
  (including control) is **capped to a few hundred cells** (`subsample_per_group`,
  `seed=0`), and **every perturbation-vs-control comparison is power-equalized** to a
  common n = min(n_pert, n_ctrl) by subsampling **without replacement** (`seed=0`), so
  magnitudes are comparable across perturbations of different coverage. Significance is a
  **1,000-permutation label-shuffle E-test**; the **one-sided empirical p =
  (1 + #{E_perm ≥ E_obs}) / (1 + 1,000)**, then **Benjamini–Hochberg FDR** across exactly
  the **11,438 tested** perturbations → `e_qval`. **Ranking is by E-distance magnitude;
  the permutation q is only a gate** (at 2.44M cells 97.5% of tested perturbations clear
  q < 0.05, so q separates almost nothing — this is why magnitude, not significance, is
  the ranking axis). `viability_ratio` = (perturbation cell count) ÷ (median perturbation
  cell count); ratio < 0.5 raises a **depletion/toxicity flag**. Gates for *nomination
  eligibility* (not for the raw leaderboard): q < 0.05 **and** viability ≥ 0.5 **and** the
  authors' per-guide knockdown-efficiency confirmation (`kd_gated_hit`).
- **Axis 2 — sign (`direction.py`, `direction_genomescale.py`, `merge_direction.py`):**
  per cell, on `normalize_total(1e4) + log1p` expression,
  `direction_score = mean(log-norm effector genes) − mean(log-norm dysfunction genes)`,
  taken vs control and aggregated per (perturbation × donor), then averaged across the two
  donors; a **per-donor sign-agreement flag** records whether both donors agree
  (donor-stratified; **no donor-level population inference**). This is an **8-hour
  transcriptional read-out, NOT a functional assay** — functional validation is required
  before calling any nominee a brake. Effector program (16 genes, all present) = IFNG,
  IL2, TNF, CSF2, LTA, XCL1/2, CCL3/4, GZMB, TNFRSF9, CD69, MYC, IRF4, BATF, TBX21;
  dysfunction program (13 genes, all present) = PDCD1, CTLA4, LAG3, HAVCR2, TIGIT, BTLA,
  CD160, VSIR, ENTPD1, TOX, NR4A1/2/3. `direction_score > 0` ⇒ knockdown pushes cells
  toward the effector program (a *candidate brake* — a transcriptional shift, not proven
  function); `< 0` ⇒ toward loss of that program. Across all 12,451 scored perturbations
  (2 more than the 12,449-perturbation E-distance universe — the direction axis also
  scores ATP1A1 and DGCR8, two perturbations the E-distance leaderboard drops)
  the distribution is left-shifted (percentiles: 50th −0.037, 75th +0.029, 95th +0.144,
  99th +0.312), so the featured brakes (+0.05 to +0.15) sit in roughly the **upper 5–25%
  of the direction distribution**, not merely just-above-zero.

## Positive-control behaviour — a face-validity check (both axes), NOT validation
1. **Magnitude (unsupervised):** the top of the leaderboard is dominated by the canonical
   TCR proximal-signalling module. **8 of the 9 largest effects** are TCR-proximal genes —
   ZAP70 (E 73.3), LCP2 (72.6), CD3E (65.7), CD3G (61.0), PLCG1 (58.3), LAT (52.2), VAV1
   (49.5), CD3D (47.2); the one exception (**rank 8, SMARCD3**, a SWI/SNF chromatin
   remodeler) is a severe-dropout perturbation (viability 0.16, fails the viability gate).
   The rest of the module — CD247, RASGRP1, ITK — sits just below (ranks 15–17). Recovering
   known biology as the largest effects is a **face-validity** check on the magnitude axis.
2. **Sign (the reclassification):** **14 of the 15 largest-effect knockdowns have a
   negative direction score** (the lone positive is CFAP298, a cilia gene — see below), and
   every TCR-module gene is **donor-consistent** (both donors strongly negative: ZAP70
   −0.63, LCP2 −0.76, CD3D −0.66, LAT −0.64). Magnitude alone would headline the cell's own
   activation machinery; the sign axis correctly reclassifies it as **activation-required —
   unsuitable inhibition targets for this objective.**

The "8 of 9" and "14 of 15" figures are **descriptive summaries of the leaderboard head**,
not tuned cut-offs (the full ranked table is in `outputs_gladstone/ranked_perturbations.csv`;
tier counts are auditable there). **This positive-control behaviour is face validity for the
workflow; it does not validate any positive-direction candidate or target-discovery
accuracy.**

## The therapeutic signal — the positive (brake) quadrant, reported honestly
Knockdowns that *raise* the effector program are the candidate class. Several literature-
known immune **brakes** land in this quadrant; where they are donor-consistent this is a
useful consistency check, but see the null-enrichment caveat below.

| Gene | E-distance | direction | donor-consistent? | note |
|---|---|---|---|---|
| **CD5** | 5.6 | +0.15 | **yes** (+0.15 / +0.14) | inhibitory co-receptor; KD de-represses TCR signalling (CD5 deletion boosts adoptive T-cell therapy — *preclinical*, PMID 39028827, 2024) |
| **DGKA** | 2.5 | +0.08 | **yes** (+0.09 / +0.07) | DAG-kinase brake; DGKα inhibitors are an IO strategy (BAY2862789 Ph1) |
| **CBLB** | 6.4 | +0.14 | **no** (+0.44 / −0.15) | E3-ligase brake; investigational CBL-B inhibitors NX-1607 (Ph1), HST-1011 (Ph1/2) |
| **SMAD3** | 25.1 | +0.06 | **no** (−0.13 / +0.26) | TGF-β pathway node (**pathway-level** candidate); highest-E-distance positive hit among the five prior targets (SKI–SMAD2/3 disruption counters TGF-β suppression of adoptive T cells, PMID 41612698, 2026) |
| **UBASH3A** | 2.0 | +0.05 | **no** (−0.08 / +0.19) | autoimmune-GWAS (T1D/RA) phosphatase (T1D association, PMID 28607106); **undrugged**, tractability unestablished (genetics-led) |

*(These five are the curated shortlist scored in `figure_targets.py`. A further high-E-
distance positive, **LAT2** (E 23.0, +0.20, donor-split), is a raw candidate but less
druggable/characterized, so it is not in the shortlist.)*

**The critical honest caveat — we do not overclaim the positive side.** Three things must
be stated plainly:

1. **The positive quadrant shows no significant brake-enrichment at this scale.** A curated
   set of **31** known T-cell negative regulators (CBLB, CBL, DGKA/Z, TNFAIP3, SOCS1/3,
   CISH, PTPN2/6, RASA2/3, UBASH3A, MAP4K1, TET2, …; scoring-module genes excluded to avoid
   circularity), of which **29 were present/tested** in this leaderboard, shows **no
   significant evidence of a positive shift vs background**: one-sided Mann–Whitney U (brakes
   > background) **U = 106,208, p = 0.70**, against a **matched background of 7,760**
   perturbations (2-donor, knockdown-gated, module + brake genes excluded). Brake median
   direction −0.047 vs background median −0.031; fraction positive **37.9% (11/29) vs
   36.7%**. This is **inconclusive / no detected enrichment — NOT evidence of equivalence**,
   and the test is exploratory (post-hoc, not pre-registered). The five genes above were
   selected by prior biology and are a **consistency check, not a method-level enrichment
   result.** (Recompute: `pipeline/brake_enrichment.py`.)
2. **Ranking the positive quadrant by raw E-distance surfaces genes with no established
   CD4 brake mechanism** — so SMAD3's designation is honest, not cherry-picked. Ordered by
   E-distance, the top positive-direction hits are: **CFAP298** (E 35.0, +0.53, donor-split
   — a cilia/flagellar gene, no known CD4-brake role), **RASGRP1** (E 28.2, **+0.02, near-
   zero** — and a TCR-activation gene), **SMAD3** (E 25.1, +0.06, donor-split), FBXO32 (E
   23.1), **LAT2** (E 23.0, +0.20), TXNL4B (E 22.5, low viability 0.47), TNNC1 (E 21.9, a
   troponin), BCL11B (E 21.0, +0.23). **SMAD3 is therefore the highest-E-distance positive
   hit *among the five manually-selected prior targets*, not the highest-ranked positive
   overall** (CFAP298 and RASGRP1 rank above it). We exclude the higher hits by explicit,
   stated criteria — no established CD4 effector-brake mechanism, donor-split direction,
   and/or low viability — rather than by calling them "artifacts"; every one is listed here
   and in the CSV so the reader can judge.

**What this means.** The **load-bearing result is the machinery axis** (a positive-control /
internal consistency check: 14/15 largest effects negative; the TCR module among them is
donor-consistent — magnitude alone would mislead). The **positive/brake side is a noisy
hypothesis space at 2 donors / Stim-8 h**: the donor-consistent brakes (CD5, DGKA) are
low-magnitude, the higher-magnitude ones (SMAD3, LAT2, CBLB) are donor-split, and the set
as a whole shows no significant enrichment. The honest deliverable is a **reproducible
signed-prioritization method + a prioritized hypothesis space** that the full 4-donor /
Stim-48 h cohort will test for improved robustness and enrichment — not a finished target
list.

## IL2RB — a non-shortlisted note
An **orthogonal public annotation layer** (STRING v12 network diffusion, **seeded from the
screen hits — an add-on layer, not independent validation**) flagged **IL2RB** (CD122). But
IL2RB knockdown shows severe viability loss (0.13) and negative direction and did not pass
the E-test gate, so it is a pathway node, not a shortlisted brake; the therapeutic angle
there would be IL-2/CD122 **agonism** (aldesleukin, N-803), not inhibition. It is excluded
from the shortlist.

## Honest caveats (state these)
1. **No Gladstone-provided interaction network or regulatory model exists.** The provided
   data share is Perturb-seq expression + a genome-wide DESeq2 DE result + supplementary
   signature/validation tables (per `data_sharing_readme.md`). **STRING v12 and Open Targets
   are legitimate *public* layers on top of the provided data — not substitutes for withheld
   provided data.** (Earlier drafts miscalled them "substitutes for a provided PPI/regulatory
   model"; corrected.)
2. **No comparison against the source authors' own analyses has been run yet.** The provided
   DESeq2 DE and Th1/Th2 polarization tables were not pulled to the workstation. Cross-checking
   the E-distance ranking, the direction score, and the five candidates against the authors'
   DESeq2 / cytokine / polarization results — reporting concordance, discordant hits, and any
   genuinely incremental information — is the **most important outstanding validation** and is
   a known gap, not a strength. We do **not** claim to have shown this pipeline adds information
   beyond the reference analysis.
3. **Donor is the biological replication unit; cells are not independent replicates.** All
   p/q values are **conditional on the analyzed D1/D2 cell distributions** and do **not**
   support donor-population inference; with 2 donors, between-donor variance and generalizability
   cannot be estimated. This is exactly why brake robustness leans on the **per-donor sign-
   agreement flag**, not the (cell-count-driven) q-value. **2 of 4 donors, Stim 8 h only**
   (compute-budget scope); the full cohort sharpens this.
4. **Perturbations of the module genes themselves are excluded from brake nominations** —
   knocking down PDCD1/TOX/NR4A/etc. trivially shifts its own pole. The featured brakes
   (CD5, DGKA, CBLB, SMAD3, UBASH3A) are not module genes.
5. **Ranking = E-distance magnitude**; permutation q is a gate. The direction axis performs
   the required-vs-enhancer split; **viability is a relative-abundance depletion proxy**
   (perturbation cell count ÷ median perturbation count; a coarse toxicity annotation, not an
   assay — e.g. LAT is viable yet clearly required), so the figure leans on **sign + donor
   consistency**, not viability. Viability did **not** reorder the raw E-distance leaderboard;
   it is applied only at the nomination-eligibility gate.
6. **The direction score is an operational transcriptional prioritization score, not a
   validated effector-versus-dysfunction axis.** It is `mean(log-norm effector) − mean(log-norm
   dysfunction)`; positive nominees require protein/functional validation (cytokine,
   proliferation, killing) before being called brakes. **Several negative-pole genes are also
   induced by *acute* TCR activation** at early timepoints — NR4A1/2/3 are immediate-early
   activation genes, and CTLA4/TOX rise with activation as well as with dysfunction — so at
   **Stim-8 h** a positive score may partly reflect activation kinetics, cell-state
   composition, stress, or global transcriptional scaling rather than a clean effector-vs-
   dysfunction contrast. The score is a simple difference of two module means, so it is
   directly amenable to effector-only / dysfunction-only / leave-one-gene-out sensitivity
   checks (recommended before functional follow-up). Normalization uses the 4,816-gene
   measured-HVG panel as the library size (not the full transcriptome), a known compositional
   caveat; the effector−dysfunction *difference* partially cancels depth effects.
7. **The brake-enrichment test is exploratory** — the 31-gene brake set is a curated literature
   list (not pre-registered); it is used to report a *descriptive null* (no significant
   enrichment, p = 0.70 vs a matched 2-donor background), and post-hoc selection can bias
   inference, so we make no confirmatory claim. The **target matrix is a curated evidence
   summary, not a fitted model** — every score's basis is in `target_matrix_provenance.md`.

## Provenance
Run manifest (auditable): dataset `genome-scale-tcell-perturb-seq` (CZI Virtual Cells; MIT
data-sharing), build `GWCD4i_Stim8hr_D1D2.built.h5ad`, bioRxiv 10.64898/2025.12.23.696273;
embedding `X_scVI`; global `seed = 0`; E-test `n_perm = 1000`, one-sided empirical p, BH-FDR
over 11,438 tested; environment pinned in `environment.yml`. Every step is a versioned Claude
Science artifact (code + environment + conversation). A background reviewer and the "MCP-
verified" dossiers are **workflow aids, not scientific provenance** — the scientific record is
the code, the pinned environment, and the output CSVs/metadata below. Separately, an adversarial
self-critique pass reproduced and caught a real **V→U diagonal-bias bug** in the E-distance
implementation (a V-statistic includes the zero self-distance diagonal, inflating the within-
group terms by an n-dependent offset ≈ 4d/n — ~5 at n = 40 — which let a pure null outrank a real
effect; the U-statistic fix drives the null E→0 and is regression-guarded in `edistance_core._smoke`).
This bug was caught by the active self-critique, not the passive reviewer. Heavy compute ran on
the DGX Spark over SSH; `make smoke` reproduces the pure-logic core anywhere; `make direction` +
`make figure` regenerate the signed map and the hero figure. Outputs:
`outputs_gladstone/ranked_perturbations.csv` (+ `direction_scores_raw.csv`), `run_meta.json`,
`direction_meta.json`, `deliverables/figures/causal_map.png`.
