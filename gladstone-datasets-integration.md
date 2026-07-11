# Using the Gladstone-provided datasets (deep-research + integration plan)

The hackathon provides three real Gladstone datasets: **immune T-cell sequencing · DNA regulatory-activity prediction · protein-interaction network** ([Cerebral Valley](https://cerebralvalley.ai/e/built-with-claude-life-sciences)). Below is what each most likely is and how to use all three together — this is the Gladstone-aligned, novelty-capable submission.

## 1. Immune T-cell sequencing ≈ genome-scale CRISPRi Perturb-seq (primary human CD4⁺ T) — ~85% confidence
Marson lab (Gladstone–UCSF Institute of Genomic Immunology), Zhu/Dann/…/Pritchard/Marson, **bioRxiv 10.64898/2025.12.23.696273**, public on **CZI Virtual Cells Platform** (`genome-scale-tcell-perturb-seq`, MIT). **~22M cells, 4 donors, 3 conditions (Rest / Stim 8h / Stim 48h)**, all expressed genes knocked down. **This is a perturbation screen → our `run_pipeline.py` E-distance method applies directly.**

**Structure** (analysis repo: `github.com/emdann/GWT_perturbseq_analysis_2025`, `data_sharing_readme.md`):
- Per-cell `D*_*.assigned_guide.h5ad`; `.X` = sparse UMI counts.
- `.obs`: `guide_id`, `perturbed_gene_name`, `perturbed_gene_id`, **`guide_type` (`targeting`/`non-targeting`)**, `top_guide_UMI_counts`, `guide_group`, QC cols, `lane_id`.
- **Controls** = cells with `guide_type == "non-targeting"` (NTC).
- Sidecars: `sgrna_library_metadata`, **`guide_kd_efficiency` (`signif_knockdown`)**, pseudobulk, precomputed DE, cross-guide/cross-donor concordance.
- Access: CZI **`vcp` CLI** (`vcp data search "Primary Human CD4+ T Cell Perturb-seq" --exact`) or S3.

**How to run it (adapts our pipeline):**
- Build `obs['perturbation'] = perturbed_gene_name`, set `guide_type=='non-targeting'` cells to `"control"` → `--control control --modality CRISPRi`.
- **Run per condition** (start with Stim 48h — activated, most disease-relevant); the paper's core point is regulators change with stimulation.
- **Integrate the 4 donors** with the `scvi-tools` skill (`batch_key=donor`) → `X_scVI`; subsample (`--max-cells-per-group 300`) for the 22M-cell scale.
- **Gate** additionally with the provided `guide_kd_efficiency.signif_knockdown` (better than mRNA-FC for CRISPRi) + cross-guide/cross-donor concordance.
- Confirm-it's-a-screen checklist: `guide_type` has a `non-targeting` class; `perturbed_gene_name.nunique()` in the thousands; sidecar CSVs present. (Observational tells that would rule it out: TCR clonotype columns, CITE-seq ADT, or only cell-type labels with no `guide_*` fields.)

## 2. DNA regulatory-activity prediction ≈ Pollard-lab sequence-to-activity model (Decima / Performer)
Deep-learning models mapping DNA sequence/variant → predicted regulatory activity per cell type ([Decima, bioRxiv 2024.10.09.617507](https://www.biorxiv.org/content/10.1101/2024.10.09.617507v1); [Performer, bioRxiv 2024.07.27.605449](https://www.biorxiv.org/content/10.1101/2024.07.27.605449v1)). **Use for the hero:** (i) confirm T-cell-specific expression; (ii) score nearby **autoimmune GWAS/eQTL variants (ref-vs-alt)** for predicted regulatory disruption → independent human-genetic causality beyond the CRISPR effect; (iii) motif attributions → mechanism.

## 3. Protein-interaction network ≈ Krogan-lab AP-MS interactome (or Silas "virtual" PPI)
A weighted protein graph (node=gene, edge=interaction+confidence) — Krogan/QBI AP-MS ([breast-cancer PPI, Science abf3066](https://www.science.org/doi/10.1126/science.abf3066)) or Silas's genome-wide *virtual* PPI (his hackathon talk). **This is how we get a NOVEL hero:**
- **(a) Expand hits — network propagation.** Personalized PageRank / random-walk-with-restart (`networkx.pagerank(G, personalization=hit_scores, alpha=0.5)`) seeded on the E-distance effect sizes; **high-diffusion NON-hit neighbors = novel target nominations** ([RWR interactome target prediction, PMC5998759](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5998759/)). Alt: DIAMOnD, OmicsIntegrator2 (PCSF).
- **(b) Druggable-complex prioritization.** Keep hits/neighbors whose complex contains a ligandable member (Open Targets tractability / ChEMBL) → causal×druggability.
- **(c) Mechanism.** Enrichment on the propagated module (GSEApy/STRING) → the pathway the hits converge on.

## The combined story (what wins the Gladstone prize)
**CRISPR Perturb-seq = causality · PPI network = mechanism + novel neighbors + a druggable handle · regulatory model = human-genetic support.** A hero carrying all three — large E-distance effect, sits in a druggable complex, a predicted-causal autoimmune regulatory variant, T-cell-specific expression — is a strong, defensible, *provided-data* submission.

## Uncertainty flags (verify in-hand)
- Exact hackathon delivery channel for the files unconfirmed (platform/Discord vs CZI/S3).
- PPI network identity (Krogan experimental vs Silas virtual) and whether the regulatory dataset ships as a runnable model vs precomputed scores — plan for both.
- Confirm the T-cell file is the perturbation screen via the §1 checklist before committing.

## Sources
[Marson genome-scale T-cell Perturb-seq (CZI VCP)](https://virtualcellmodels.cziscience.com/dataset/genome-scale-tcell-perturb-seq) · [analysis repo](https://github.com/emdann/GWT_perturbseq_analysis_2025) · [Decima](https://www.biorxiv.org/content/10.1101/2024.10.09.617507v1) · [Performer](https://www.biorxiv.org/content/10.1101/2024.07.27.605449v1) · [Krogan breast-cancer PPI](https://www.science.org/doi/10.1126/science.abf3066) · [RWR target prediction](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5998759/) · [hackathon](https://cerebralvalley.ai/e/built-with-claude-life-sciences)
