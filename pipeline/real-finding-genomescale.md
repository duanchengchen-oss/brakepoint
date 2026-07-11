# REAL FINDING — genome-scale CD4⁺ T-cell CRISPRi (Gladstone Perturb-seq)

Real Claude Science run on the DGX Spark. Verified and corrected by the co-pilot (live ClinicalTrials/Open Targets). Supersedes the auto-generated `outputs_gladstone/hero_dossier.md` where they differ.

## The run
- **Data:** genome-scale CRISPRi Perturb-seq, **primary human CD4⁺ T cells** (Marson/Gladstone; CZI VCP). Donors D1+D2, **Stim 8 h**.
- **Scale:** **2.44 M cells** after QC (of 2.64 M), **12,449 perturbations**, 11,438 tested, control = non-targeting guides.
- **Method:** scVI donor-integration (`X_scVI`) → power-equalized **E-distance** + permutation E-test → gates: q<0.05, viability, **author-provided knockdown efficiency**. **9,535 pass; 7,816 knockdown-confirmed.**

## Validation (genome-scale, unsupervised)
The top causal hits are the **entire canonical TCR proximal-signaling module** — the strongest possible internal control: **ZAP70, CD3E/G/D, CD247, PLCG1, LAT, LCP2, VAV1, RASGRP1, ITK**. The method measures real biology at 2.4 M-cell scale.

## Network step → novel candidates
Causal signal diffused over the human interactome (personalized PageRank, degree-corrected) → **203 novel candidates** (network-central, ≥3 causal-hit neighbors, not themselves direct hits). Immune-focused top: **BLNK, VAV2, NCR1, FCGR1A, IL2RB, PIK3R3**.

## Hero — honest, verified
**Lead (network-nominated, best-evidenced): IL2RB (CD122, IL-2/IL-15 receptor β).** Never a direct hit, yet sits amid five causal hits (CD247, STAT3, ITK, PTPRC, CD3D); governs CD4⁺ effector/Treg balance; autoimmune genetics (MS, T1D).
- **Druggability — corrected (live ClinicalTrials, this session):** the approved anti-IL-2R antibodies **basiliximab/daclizumab target IL2RA/CD25, *not* IL2RB**, and **daclizumab was withdrawn (2018)** for safety. IL2RB (CD122) is drugged by **IL-2 pathway agonists** — aldesleukin (approved, oncology) and CD122-biased **bempegaldesleukin** (trials; NKTR-214's pivotal melanoma program failed 2022). → IL2RB is a **pathway-validated, drug-*adjacent*** node, not a clean approved target. Frame it as such.
- Read: the causal→network funnel **re-discovers the IL-2 signaling axis** as an actionable CD4⁺ node purely from raw Perturb-seq — strong validation that the method finds real, drug-relevant biology.

**Novel frontier (genuinely undrugged — higher risk/reward):**
- **VAV2** — Rho-family GEF, **VAV1 paralog** sitting in the exact TCR-proximal module (SYK, PLCG1, ZAP70, ITK, VAV1); top network enrichment; **no existing drug** (GEFs are a hard but emerging target class). The most biologically coherent *novel* immune nomination on **network/paralog** grounds — though its **human genetics are non-immune** (live OT: glaucoma/hypertension; T1D only 0.26), so the immune rationale is mechanistic, not genetic. See `dossiers/VAV2.json`.
- **BLNK** — highest raw network enrichment via shared SYK/PLCG1/ZAP70/LAT neighbours, **but honestly caveated:** BLNK/SLP-65 is canonically the **B-cell** adaptor (the SLP-76/LCP2 analog) and its human genetics are **agammaglobulinemia** (live OT 0.72; PMID 24582315), off-axis from a CD4⁺ T-cell effector program; as an **intracellular adaptor it is poorly tractable** (no small molecule, not a practical antibody target — "antibody-only" overstates it). Best read as target-biology, not a near-term program. See `dossiers/BLNK.json`.
- *De-prioritized:* PIK3R3 (most small-molecule-tractable, but human genetics point to cancer, not immunity).

**Proposed experiment (hero):** arrayed CRISPR in primary CD4⁺/CD8⁺ T cells with a cytokine/effector readout, plus **opposite-modality replication** (CRISPRa should move the program the other way); for IL2RB, a CD122-agonist tool-compound counter-test.

## Honest caveats (state these in the demo)
1. **PPI + regulatory inputs were public substitutes** — the network step used **STRING v12** and genetics used **Open Targets**, because the *Gladstone-provided* protein-interaction network and Decima/Performer regulatory model were not in the workspace. Re-running with the actual provided PPI/regulatory data is the obvious next step and would make this a true "all-three-provided-datasets" result.
2. **2 of 4 donors, Stim 8 h only** (compute-budget scope). The full 4-donor / Stim-48 h scope would sharpen effect sizes.
3. Ranking = E-distance magnitude; permutation q is a gate. Mito-QC was inactive (Ensembl var names) — total-count/gene MAD filters applied.

## Submission framing — pick one (one-line swap in the deliverables)
- **A) Method + IL2RB (recommended, best-evidenced):** genome-scale validation → network re-discovers the IL-2 axis (drug-adjacent, autoimmune genetics), with VAV2/BLNK as the novel frontier. Honest, strong, hard to attack.
- **B) Novel-hero headline: VAV2:** lead with the genuinely-undrugged discovery; IL2RB + the TCR module become the positive controls proving the method. Bolder; weaker on tractability/genetics — flag the hard target class.
