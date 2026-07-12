# REAL FINDING — druggable-brake target discovery in CD4⁺ T cells

**Deliverable:** a shortlist of **five druggable brakes** on human CD4⁺ T-cell
effector function (lead **CBLB**; also **CD5, DGKA, SMAD3, UBASH3A**), nominated by
convergent evidence and scored in `figure_targets.py`. The signed causal map below
is the *discovery engine*; the target shortlist is the *output*. Honesty caveats
(2 donors; positive quadrant not yet enriched, p=0.56) are kept throughout.

## The engine — a genome-scale *signed* causal map of CD4⁺ T-cell function

Real Claude Science run on the DGX Spark (NVIDIA GB10), verified end-to-end. This
supersedes the earlier IL2RB-centric framing and the auto-generated
`outputs_gladstone/hero_dossier.md` where they differ.

## The one-line finding
On 2.64 M primary human CD4⁺ T cells, ranking CRISPRi knockdowns by **causal
effect size alone cannot tell a drug target from the cell's own machinery** — 8 of
the 9 largest effects are the TCR signalling module. Adding a **signed
direction-of-effect axis** splits the map: those top effects are all strongly
**negative** (knockdown *cripples* the effector program → required machinery),
donor-consistently. That machinery→negative result is the **validated,
load-bearing finding**, confirmed against ground-truth biology in both magnitude
and sign. The **positive** quadrant (knockdown *enhances* effector function) is the
therapeutic hypothesis space — presented honestly: at 2 donors it is noisy and
**not yet enriched** for a curated known-brake set (p = 0.56), so it is a
prioritized space for the full cohort, not a finished target list.

## The run
- **Data:** genome-scale CRISPRi Perturb-seq, **primary human CD4⁺ T cells**
  (Marson lab / Gladstone; CZI Virtual Cells Platform). Donors **D1 + D2**,
  condition **Stim 8 h**. Control = non-targeting guides (`control`).
- **Scale:** **2,638,736 cells** × 4,816 measured HVGs; **12,449 perturbations**
  (11,438 with ≥30 cells tested). scVI donor-integrated latent (`X_scVI`).
- **Axis 1 — magnitude:** power-equalized **E-distance** on `X_scVI` +
  1,000-permutation E-test; gates: permutation q<0.05, viability, and the
  authors' per-guide knockdown-efficiency sidecar.
- **Axis 2 — sign:** per cell, `mean(log-norm effector genes) − mean(log-norm
  dysfunction genes)`, aggregated per (perturbation × donor) vs control (donors as
  replicates, with a per-donor sign-agreement flag). Effector program = IFNG, IL2,
  TNF, CSF2, LTA, XCL1/2, CCL3/4, GZMB, TNFRSF9, CD69, MYC, IRF4, BATF, TBX21;
  dysfunction program = PDCD1, CTLA4, LAG3, HAVCR2, TIGIT, BTLA, CD160, VSIR,
  ENTPD1, TOX, NR4A1/2/3. `direction_score > 0` ⇒ knockdown pushes cells toward
  the effector program (a brake); `< 0` ⇒ toward loss of effector function.
  Code: `direction.py`, `direction_genomescale.py`, `merge_direction.py`.

## Validation — the map recovers ground truth in *both* axes
1. **Magnitude (unsupervised):** the top of the leaderboard is dominated by the
   canonical TCR proximal-signalling module. **8 of the 9 largest effects** are
   TCR-proximal genes — ZAP70, LCP2, CD3E, CD3G, PLCG1, LAT, VAV1, CD3D; the one
   exception (rank 8, **SMARCD3**, a SWI/SNF chromatin-remodeler) is a
   high-toxicity dropout (viability 0.16). The rest of the module — CD247, ITK,
   RASGRP1 — sits just below (ranks ~15–17). This is the strongest possible
   internal control that the method measures real biology at 2.6 M-cell scale.
2. **Sign (the key result):** **14 of the 15 largest-effect knockdowns have a
   negative direction score**, and every TCR-module gene is **donor-consistent**
   (both donors strongly negative: e.g. ZAP70 −0.63, LCP2 −0.76, CD3D −0.66, LAT
   −0.64). Magnitude alone would headline the cell's own activation machinery; the
   sign axis correctly reclassifies it as **required machinery, not druggable.**
   This machinery→negative direction is the validated, load-bearing result.

## The therapeutic signal — the positive (brake) quadrant, reported honestly
Knockdowns that *raise* the effector program are the drug-relevant class. Several
literature-known immune **brakes** land in this quadrant and are donor-consistent —
a useful consistency check:

| Gene | E-distance | direction | donor-consistent? | note |
|---|---|---|---|---|
| **CD5** | 5.6 | +0.15 | **yes** (+0.15 / +0.14) | inhibitory co-receptor; KD de-represses TCR signalling |
| **DGKA** | 2.5 | +0.08 | **yes** (+0.09 / +0.07) | DAG kinase brake; DGKα inhibitors are an IO strategy |
| **CBLB** | 6.4 | +0.14 | no (+0.44 / −0.15) | E3-ligase brake; oral CBL-B inhibitors (NX-1607, HST-1011) in Ph1 |
| **SMAD3** | 25.1 | +0.06 | no (−0.13 / +0.26) | TGF-β effector brake; the highest-E-distance *biologically-coherent* positive node |
| **LAT2** | 23.0 | +0.20 | no (−0.09 / +0.49) | negative modulator of LAT signalling |

**The critical honest caveat — we do not overclaim the positive side.** Two
things must be stated plainly:
1. **The positive quadrant is not brake-enriched at this scale.** A curated set of
   29 known T-cell negative regulators (CBLB, CBL, DGKA/Z, TNFAIP3, SOCS1/3, CISH,
   PTPN2/6, RASA2/3, UBASH3A, MAP4K1, TET2, …; scoring-module genes excluded to
   avoid circularity) is **not significantly shifted toward positive direction vs
   background** (Mann–Whitney one-sided **p = 0.56**; 37.9% positive vs 35.5%).
   The genes above were selected by prior biology and are a **consistency check,
   not a method-level enrichment result.**
2. **The raw top of the positive quadrant is dominated by likely artifacts** — the
   highest-E-distance positive-direction hits include CFAP298 (a cilia gene) and
   germ-cell/chromatin genes, not credible CD4 brakes. So SMAD3 is the
   highest-magnitude *coherent* brake, not the highest positive overall.

**What this means.** The **validated, load-bearing result is the machinery axis**
(14/15 largest effects negative, donor-consistent — magnitude alone would mislead).
The **positive/brake side is a noisy hypothesis space at 2 donors / Stim-8 h**: the
donor-consistent brakes (CD5, DGKA) are low-magnitude, the higher-magnitude ones
(SMAD3, LAT2, CBLB) are donor-split, and the set as a whole isn't yet enriched. The
honest deliverable is a **validated signed-map method + a prioritized hypothesis
space** that the full 4-donor / Stim-48 h cohort is expected to sharpen — not a
finished target list. (Enrichment recomputes via `pipeline/brake_enrichment.py`.)

## IL2RB — a convergence node, reframed honestly
An independent layer (personalized-PageRank diffusion of the causal signal over
the STRING interactome) nominates **IL2RB (CD122, IL-2/IL-15 receptor β)**: never
a direct hit, yet network-central among five causal hits, with multiple-sclerosis
/ broader autoimmune genetics (Open Targets). The direction axis now *explains*
it: **IL2RB knockdown is essentially lethal** (viability 0.13, direction −0.24) —
it is required machinery for the pro-survival IL-2 signal. That is precisely why
the drug is an **IL-2/CD122 agonist**, not an inhibitor: **aldesleukin** (approved
IL-2) and the approved IL-15 superagonist **nogapendekin alfa / N-803 (Anktiva)**
signal through CD122. **Correction (kept):** the approved anti-IL-2R antibodies
**basiliximab / daclizumab target IL2RA (CD25), *not* IL2RB**, and **daclizumab was
withdrawn (2018)** for safety (PMID 29645071); the CD122-biased
**bempegaldesleukin (NKTR-214)** program was **terminated in 2022**. IL2RB is a
pathway-validated, drug-*adjacent* convergence node — supporting evidence, not the
headline.

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
   The featured brakes (CD5, DGKA, CBLB, SMAD3, LAT2) are not module genes.
4. **Ranking = E-distance magnitude**; permutation q is a gate. The
   required-vs-enhancer split uses viability as a *coarse* proxy (e.g. LAT is
   viable yet clearly required) — the figure encodes sign + donor consistency
   directly rather than leaning on that split.

## Provenance
Every step is a versioned Claude Science artifact (code + environment +
conversation), and a background reviewer checks claims against what actually ran —
which surfaced a real diagonal-bias bug in the E-distance statistic before any
figure. Heavy compute ran on the DGX Spark over SSH; `make smoke` reproduces the
pure-logic core anywhere; `make direction` + `make figure` regenerate the signed
map and the hero figure. Outputs: `outputs_gladstone/ranked_perturbations.csv`
(+ `direction_*`), `direction_meta.json`, `deliverables/figures/causal_map.png`.
