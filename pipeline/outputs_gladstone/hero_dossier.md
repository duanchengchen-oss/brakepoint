# Novel drug-target dossier — genome-scale CD4⁺ T-cell CRISPRi Perturb-seq

**Dataset:** Genome-scale CRISPRi Perturb-seq in primary human CD4⁺ T cells (Marson lab; CZI Virtual Cells Platform; bioRxiv 10.64898/2025.12.23.696273).
**Question:** *Look for new drug targets in the CD4⁺ T-cell Perturb-seq data.*
**Compute:** NVIDIA GB10 (DGX Spark), scVI donor-integrated latent; causal ranking + PPI network propagation + Open Targets druggability.

---

## 1. What was run

| Stage | Detail |
|---|---|
| Cells analysed | **2,638,736** CD4⁺ T cells (donors D1 + D2, condition **Stim 8 hr**) |
| Perturbation calls | single-guide-targeting cells + non-targeting controls (NTC → `control`) |
| Perturbations | **12,449** gene knockdowns; **11,438 tested** (≥30 cells/group) |
| Integration | scVI, `batch_key=donor`, 30-dim latent (`X_scVI`), 4,816 HVGs, 40 epochs |
| Causal statistic | power-equalised **E-distance** on `X_scVI` + 1,000-permutation E-test |
| Gates | permutation q<0.05 · viability · **guide knockdown-efficiency** (`signif_knockdown`, Stim8hr) |
| Cells after QC + subsample | 2,436,881 (cap 300/group) |

**9,535 perturbations pass the E-distance gates; 7,816 also carry confirmed knockdown** (kd-gated hits).

---

## 2. Causal ranking — internal validation

The top of the ranking is the **canonical TCR proximal-signalling module**, exactly what should dominate a CD4⁺ activation screen. This is the strongest possible internal control that the pipeline is measuring real biology, not technical artefact.

Ranks are **overall position by E-distance** across all 11,438 tested perturbations. "Gated" = passes q<0.05 + viability + knockdown-confirmation.

| Rank | Gene | E-distance | q | Gated |
|---|---|---|---|---|
| 1 | **ZAP70** | 73.3 | 0.0012 | ✓ |
| 2 | **LCP2** (SLP-76) | 72.6 | 0.0012 | — (viability) |
| 3 | **CD3E** | 65.7 | 0.0012 | ✓ |
| 4 | **CD3G** | 61.0 | 0.0012 | ✓ |
| 5 | **PLCG1** | 58.3 | 0.0012 | ✓ |
| 6 | **LAT** | 52.2 | 0.0012 | ✓ |
| 7 | **VAV1** | 49.4 | 0.0012 | ✓ |
| 8 | **SMARCD3** | 49.0 | 0.0012 | — (no kd) |
| 9 | **CD3D** | 47.2 | 0.0012 | ✓ |
| 15 | **CD247** (CD3ζ) | 29.4 | 0.0012 | ✓ |
| 16 | **RASGRP1** | 28.1 | 0.0012 | ✓ |
| 17 | **ITK** | 28.1 | 0.0012 | ✓ |

The TCR complex (CD3D/E/G, CD247), the LAT signalosome (LAT, LCP2/SLP-76, PLCG1, VAV1), the ZAP70/ITK kinases and the Ras activator RASGRP1 are all recovered as the largest causal effects. LCP2 (rank 2, SLP-76) is itself TCR-proximal; it is ungated only because its knockdown depletes cell number (viability flag), not because the effect is weak. Non-canonical hits in the top 25 include **SMAD3** (TGF-β), **BCL11B** (T-cell identity TF), **SENP5** (SUMO protease), **RB1CC1/FIP200** (autophagy) and **SYK**.

*Full table:* `ranked_perturbations.csv` (12,449 rows; E-distance, q-value, viability, target fold-change, knockdown-efficiency columns, `kd_gated_hit` flag).

---

## 3. Network propagation — nominating a *novel* target

Top causal hits are the known machinery — not new targets. To find genuinely novel candidates we diffused the **causal signal over the human protein–protein interaction network** (STRING v12, 16,201 proteins, 236,930 high-confidence edges, score ≥ 700):

- **Personalised PageRank** (restart α = 0.5) seeded by the top-200 kd-gated hits, weighted by their E-distance effect sizes.
- **Novel candidate** = high diffusion score, **≥ 3 distinct causal-hit neighbours**, **not itself a significant causal hit**, ranked by degree-corrected diffusion enrichment (guilt-by-multiple-association, which rejects hub artefacts).

**203 novel candidates** were nominated. The immune-signalling-specific top of the list:

| Gene | Enrichment | Causal-hit neighbours | Druggable? |
|---|---|---|---|
| **BLNK** | 5.5 | VAV1, SYK, ZAP70, PLCG1, LAT | antibody-only |
| **VAV2** | 3.5 | SYK, PLCG1, ZAP70, ITK, VAV1 | undrugged (GEF) |
| **NCR1** | 2.6 | CD247, CD244, BCL11B, PTPRC, CD3E | antibody-only |
| **FCGR1A** | 2.3 | SYK, CD247, CD3G, PTPRC | SM structure |
| **IL2RB** | 1.7 | CD247, STAT3, ITK, PTPRC, CD3D | **antibody + SM, clinically validated** |
| **PIK3R3** | 1.5 | PTEN, SYK, VAV1, PLCG1, ZAP70, ITK (8) | **advanced-clinical SM** |

*Full table:* `ppi_propagation.csv` (diffusion enrichment, seed-neighbour list, degree) + `ppi_propagation_full.csv` (all 16,201 nodes).

---

## 4. Hero nomination — **IL2RB** (interleukin-2 receptor β)

**Why IL2RB is the lead network hero:**

1. **Causal-network evidence** — never a direct causal hit (untested/non-significant on its own knockdown), yet sits amid **five core causal hits** (CD247/CD3ζ, STAT3, ITK, PTPRC/CD45, CD3D), with 1.7× disproportionate diffusion from the TCR/cytokine-signalling seeds.
2. **Biology** — β subunit of the IL-2 (and IL-15) receptor; transduces the mitogenic IL-2 signal that governs CD4⁺ effector expansion and Treg homeostasis. Loss-of-function-constrained (gnomAD LoF upper bin 2).
3. **Druggability — pathway-validated, drug-*adjacent* (corrected).** IL2RB (CD122) has **no selective approved drug**; Open Targets shows a structural ligand but **no druggable-family / clinical small molecule** and only Phase-1-level antibody tractability. It is engaged by **IL-2/IL-15 pathway agonists** — **aldesleukin** (approved IL-2), the **approved IL-15 superagonist nogapendekin alfa (N-803 / Anktiva)** that signals through IL2RB/CD122, and the CD122-biased **bempegaldesleukin (NKTR-214)**, whose Nektar/BMS PIVOT/PROPEL program was **terminated in 2022** after the Phase-3 melanoma failure. **Correction:** the approved anti-IL-2R antibodies **basiliximab / daclizumab target IL2RA (CD25), *not* IL2RB**, and **daclizumab was withdrawn (2018)** for safety (Pérez-Miralles, *Rev Neurol* 2018, PMID 29645071). Frame IL2RB as pathway-validated and drug-adjacent, not a clean approved target. See `dossiers/IL2RB.json`.
4. **Human genetics / association support** — Open Targets **overall association ≈ 0.67** for immunodeficiency-with-autoimmunity, with **multiple sclerosis** (0.53) and IL-2-pathway oncology among 684 associated diseases (live OT, 2026-07-11). Scores are OT *overall* association (genetic + other datatypes), not a signed genetic score — the theme is autoimmune / immune-dysregulation.

**Honest caveat:** IL2RB is already a clinically precedented target. Its emergence here is best read as **validation** that the causal→network→druggability pipeline recovers a real, actionable CD4⁺ T-cell node from raw Perturb-seq — rather than a de-novo discovery.

**Genuinely undrugged alternatives** for a higher-risk / higher-novelty program: **VAV2** (Rho-family GEF, VAV1 paralog, top-enrichment, no existing drugs — but a hard target class) and **BLNK** (SYK-pathway adaptor, highest enrichment, antibody-only). **PIK3R3** (PI3K regulatory subunit) is the most small-molecule-tractable runner-up but its human genetics point to cancer, not immunity.

---

## 5. Reproducibility & limitations

- **Donors/condition:** D1 + D2, Stim 8 hr only (2 of 4 donors, 1 of 3 conditions). Chosen to give a clean donor batch-key at ~2.6 M cells without a ~590 GB re-download. The Gladstone brief's Stim-48 hr / 4-donor scope would sharpen effect sizes but was out of compute-budget scope here.
- **Ranking metric** is E-distance magnitude; the permutation q-value is a gate, not the rank.
- **Knockdown gate** uses the authors' own per-guide `signif_knockdown` sidecar (Stim8hr).
- **Mitochondrial QC** was inactive (var names are Ensembl IDs, so the `MT-` symbol filter matched nothing); total-counts and gene-count MAD filters were applied (kept 2.59 M / 2.64 M cells).
- **PPI and regulatory data were public substitutes** (STRING v12; Open Targets human-genetics scores), as the Gladstone-provided protein-interaction network and Decima/Performer regulatory model were not in the workspace.

## Output files (`pipeline/outputs_gladstone/`)
- `ranked_perturbations.csv` — full causal ranking, gated + kd-annotated
- `ppi_propagation.csv` — novel network nominations (immune-focused, enrichment-ranked)
- `ppi_propagation_full.csv` — diffusion scores for all 16,201 network nodes
- `ranked_genes_edistance.png` — top causal perturbations figure
- `run_meta.json`, `ppi_meta.json` — run parameters
- `hero_dossier.md` — this file
