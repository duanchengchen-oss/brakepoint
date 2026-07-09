# AI-Driven Target Discovery — State of the Art & Playbook
**Prepared for:** Built with Claude: Life Sciences (research track, solo) · causal target discovery from T-cell perturbation data
**Method:** 5-angle fan-out deep research; each load-bearing claim cross-checked against ≥2 sources; contested points flagged. Companion to `research-track-target-discovery-plan.md`, `target-assessment-framework.md`, and `worked-example-TYK2.md`.

---

## Executive summary — the 12 things that matter
1. **Genetic support ~2–2.6× drug success is real and quantified** — Nelson 2015 (2.0%→8.2% of mechanisms genetically supported, preclinical→approved), King 2019 (~2× confirmed after cleaner matching), **Minikel/King 2024 (relative success 2.6×)**, Ochoa 2022 (~66% of 2021 FDA approvals had genetic support; OR ≈2.03). **Direction-of-effect concordance is your highest-leverage, most defensible signal** — build the pipeline around it.
2. **Open Targets already encodes the multi-axis rubric** — its disease-agnostic *target prioritisation* scores precedence, tractability, doability, and safety (gnomAD LOEUF constraint, DepMap essentiality, mouse KO, tissue specificity). Don't reinvent it; call it and extend it.
3. **Pseudobulk, not cell-level, DE** — Squair 2021 showed cell-level tests inflate false discoveries via pseudoreplication; aggregate to perturbation×donor pseudobulks (edgeR/DESeq2/limma) or use a mixed model (Zimmerman 2021). This single choice is a credibility gate.
4. **mixscape + E-distance are the standard core** — filter escaped/non-perturbed cells (mixscape), quantify effect size with E-distance/E-test; both live in **pertpy**, so your whole method is one well-cited toolkit.
5. **Single-cell foundation models (scGPT/Geneformer) are contested** — three independent benchmarks find they often *don't beat* PCA/scVI/linear baselines on perturbation tasks. Don't stake the project on them; if used, benchmark against a simple baseline in the demo.
6. **Claude Science orchestrates hosted BioNeMo models (Evo 2, Boltz-2, OpenFold3, ESM) as NIM endpoints** — the compute question flips from "can I train this?" to "can I orchestrate it cleanly?" Boltz-2 (MIT-licensed, structure+affinity) and ESM-2 (CPU-capable) are the solo-friendly picks; AlphaFold3 weights are non-commercial (friction).
7. **The research track is judged on a reproducible artifact/model on real data — not slides.** Winners of prior Anthropic/Cerebral Valley events were *domain experts who are "bilingual"* (science + AI), not the strongest engineers. Lead with the discovery.
8. **Gladstone's taste (from Silas's talk) = pure-compute, genome/proteome-scale, translatable discovery.** Nominate a *specific, novel, wet-lab-testable* target, with a proposed experiment.
9. **Claude Science's auditable artifacts + reviewer agent are your reproducibility proof** — demo the provenance trail (code+env+history) and the reviewer catching an error. That literally *is* "show us how Claude Science got you there."
10. **Best primary datasets are named and accession-verified** — Schmidt 2022 CRISPRa Perturb-seq in primary human T cells (**GSE190604**) and Shifrut 2018 (**GSE119450**); Frangieh 2021 (**SCP1064**) for immuno-oncology; pull harmonized via **scPerturb**.
11. **Confirm the data is actually a perturbation screen** — look for a guide/feature-barcode library, per-cell sgRNA assignment, and non-targeting controls. No guide calls + no NTCs ⇒ observational ⇒ your causal design breaks.
12. **The shared MCP endpoints (Open Targets, ChEMBL) rate-limit/500 under load** (observed live today). Snapshot on Day 1, cache with backoff, never live-query at the deadline.

---

## AIDD target discovery & prioritization
**Open Targets: association scoring.** The [Open Targets Platform](https://platform-docs.opentargets.org/associations) aggregates ~20 datasources (genetics, somatic mutations, known drugs, pathways, expression, animal models, text-mining) into a 0–1 **association score** via a **harmonic sum** (each evidence divided by rank², normalised), then combines datasources with adjustable weights ([Ochoa et al., NAR 2021](https://academic.oup.com/nar/article/49/D1/D1302/5983621)).

**Open Targets: target prioritisation** (disease-agnostic; a −1→+1 "traffic-light" across four sections) — this is the multi-axis rubric already built ([docs](https://platform-docs.opentargets.org/web-interface/target-prioritisation)):
- **Precedence:** clinical stage of any drug hitting the target.
- **Tractability:** membrane/secreted location, ligand/small-molecule binder, predicted pockets (DrugEBIlity ≥0.7).
- **Doability:** mouse-ortholog identity, high-quality chemical probes.
- **Safety:** gnomAD **LOEUF** constraint, mouse-KO phenotypes (MGI), **DepMap** common-essential, known adverse events, cancer-driver status, paralogues, tissue specificity/distribution (GTEx + Tabula Sapiens).

**Genetic support — precise numbers:** Nelson 2015 **2.0%→8.2%** ([Nat Genet](https://www.nature.com/articles/ng.3314)); King 2019 ~2× confirmed/revised ([PLoS Genet](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1008489)); **Minikel/King 2024 relative success 2.6×** ([Nature](https://www.nature.com/articles/s41586-024-07316-0)); Ochoa 2022 ~66% of 2021 approvals, **OR 2.03** ([NRDD](https://www.nature.com/articles/d41573-022-00120-3)).

**Pharos/TCRD Target Development Level** — your novelty axis ([NAR](https://academic.oup.com/nar/article/49/D1/D1334/5958490)): **Tclin** (approved-drug target), **Tchem** (potent ligands, no drug), **Tbio** (biology known, no potent ligand), **Tdark** (understudied). A novel hero lives in **Tbio/Tdark** with a Tclin-shaped evidence pattern.

**Tractability buckets** (Open Targets/canSAR lineage): small-molecule (approved→clinical→ligand→pocket→druggable-family), antibody (clinical→plasma-membrane/secreted location), PROTAC (clinical→literature→ubiquitination sites→binder), and "other clinical." ([Tractability docs](https://platform-docs.opentargets.org/target/tractability))

*Contested:* the exact "2×" depends on definition (proportion vs relative success vs OR) and is weak in oncology; Open Targets scores are weight-configurable, not absolute; Pharos TDL counts shift per release.

---

## Causal target discovery from perturbation screens
The SOTA pipeline: confirm the perturbation took, quantify effect, integrate away technical/donor variation, test DE correctly, localize responsive cell types, summarize into programs, triage against human genetics.

- **Filter escaped cells — mixscape** (Papalexi 2021): per-cell local perturbation signature vs k nearest non-targeting controls, then a 2-component mixture classifies "perturbed" vs "escaping"; escapees removed. Essential — incomplete KO/CRISPRi leaves cells indistinguishable from controls. [Seurat](https://satijalab.org/seurat/articles/mixscape_vignette) / [pertpy](https://pertpy.readthedocs.io/en/stable/tutorials/notebooks/mixscape.html).
- **Effect size — E-distance / E-test** ([scPerturb, Nat Methods 2024](https://www.nature.com/articles/s41592-023-02144-y)): energy-statistics distance between perturbed and control distributions in PCA space; permutation test for significance; principled screen-QC + ranking. In **pertpy** ([Nat Methods 2025](https://www.nature.com/articles/s41592-025-02909-7)) alongside mixscape and Augur.
- **Integration — scVI/scANVI** ([best practices](https://www.sc-best-practices.org/cellular_structure/integration.html)): VAEs modeling raw counts while regressing out batch/donor. Caveat: can erase real signal if perturbation is confounded with batch; never run DE in latent space.
- **DE — pseudobulk** ([Squair 2021](https://www.nature.com/articles/s41467-021-25960-2)): cell-level tests inflate false discoveries via pseudoreplication; aggregate to perturbation×donor pseudobulks + edgeR/DESeq2/limma. Contested alternative: **GLMMs** with a per-donor random effect ([Zimmerman 2021](https://www.nature.com/articles/s41467-021-21038-1)) also control type-I error.
- **Responsive cell types — Augur** ([Nat Biotechnol 2021](https://www.nature.com/articles/s41587-020-0605-1)): classifier AUC ranks which cell types respond most.
- **Programs & causal structure:** consensus NMF / [SCENIC+](https://www.nature.com/articles/s41592-023-01938-4) regulons; genome-scale causal GRN inference from Perturb-seq is **unsolved** (sensitive to knockdown efficiency, confounding; [CausalBench](https://arxiv.org/pdf/2308.15395)). Flagship integrative anchor: **[Ota et al., Nature 2025](https://www.nature.com/articles/s41586-025-09866-3)** links Perturb-seq regulatory edges → cNMF programs → traits using human LoF burden tests — the template for "causal + genetics."
- **Human-genetics concordance for triage** ([GPS-DOE, Nat Genet 2023](https://www.nature.com/articles/s41588-023-01609-2)): does the perturbation's direction agree with the disease-risk direction? Orthogonal triage, not primary discovery.

**Pitfalls:** donor/batch confounding (balance guides across lanes), viability/essentiality (KO depletion masquerades as a hit), escaped cells (→mixscape), pseudoreplication/multiplicity (→pseudobulk/GLMM), effect-size≠significance (report E-distance/log-FC beside adjusted p).

**A defensible "discrete finding":** *"Perturbing gene X in cell type Y (Augur AUC↑) yields a significant E-distance shift, driven by pseudobulk-DE program P (cNMF/SCENIC), concordant in direction with human genetic evidence."*

*Contested/uncertain:* pseudobulk vs mixed-models (both valid, design-dependent); causal GRN inference from Perturb-seq remains unsolved and benchmark-dependent.

---

## AIDD foundation models & tooling
**Key reframing:** Claude Science ships NVIDIA's [BioNeMo Agent Toolkit](https://blogs.nvidia.com/blog/claude-science-bionemo-agent-toolkit/), exposing Evo 2, Boltz-2, OpenFold3, ESM, RFdiffusion, ProteinMPNN as **hosted NIM endpoints callable as agent skills** — you *orchestrate*, not train. Budget = integration time, not GPUs.

| Tool | Inputs → outputs | Solo compute | 6-day verdict |
|---|---|---|---|
| **Evo 2** (Arc) | DNA → variant likelihoods, generation | 40B needs H100s; **hosted NIM** | Useful via API for a narrow variant-effect demo; self-host = overkill |
| **Boltz-2** (MIT) | protein+SMILES → structure + **affinity** | 1 GPU (~18s) or NIM | **Best fit** — permissive, light, demo-able |
| **AlphaFold3** | seq → structure/complex | weights **non-commercial** | Friction — licensing blocks an OSS build |
| **OpenFold3** | seq → structure/complex | GPU or NIM | Useful — permissive AF3 alternative |
| **ESM-2** | seq → embeddings, mutation scores | **CPU (small models)** | Useful — lightest building block |
| **scGPT / Geneformer** | scRNA-seq → embeddings, in-silico perturbation | 1 GPU fine-tune | **Risky/contested** — benchmark vs PCA/scVI first |
| **Open Targets / ChEMBL / gnomAD / DepMap / Pharos / HPA / GTEx** | IDs → evidence, constraint, essentiality | **none (API/bulk)** | **Core** — free, fast, high-signal |

*Contested:* scGPT/Geneformer frequently fail to beat PCA/scVI/linear baselines on perturbation & zero-shot tasks ([Nat Methods 2025](https://www.nature.com/articles/s41592-025-02772-6); ["one PCA still rules them all"](https://arxiv.org/abs/2410.13956)). Boltz-2's "18s / 1000×-vs-FEP" is author/vendor-reported. Evo 2 practical inference cost on modest hardware is under-documented — assume the hosted path.

---

## Winning-strategy intelligence
**Event (confirmed):** global virtual hackathon July 7–13 2026, Anthropic × **Gladstone** × Cerebral Valley, ~$100K credit pool ([Cerebral Valley](https://cerebralvalley.ai/e/built-with-claude-life-sciences); [AlphaSignal](https://alphasignal.ai/news/anthropic-s-claude-science-hackathon-offers-researchers-100k-to-reinvent)). Two tracks — research (Claude Science → reproducible analysis/model) and builder (Claude Code). Gladstone supplies **real datasets: immune T-cell sequencing, DNA regulatory-activity prediction, protein-interaction networks** (single reporting chain — verify in-platform). Talk titles are confirmed from the kickoff deck: Tarashansky "Overview of Claude Science"; Silas "From genome to inference without touching a pipette: virtual genome-wide PPI screening leads to real discoveries."

**What wins:** judges grasp the problem in ~30s, then want a **live working demo, not slides** ([JetBrains judging notes](https://blog.jetbrains.com/ai/2026/06/how-to-win-a-hackathon-notes-from-the-judging-table/)); do **one thing really well**. Prior Anthropic/Cerebral Valley events were won by **domain experts, not the best engineers** (a lawyer beat 500 developers; [Kotrotsos](https://kotrotsos.medium.com/anthropic-hackathon-results-b13f8466296e)); GLP-1 inventor Lotte Knudsen: winners are **"bilingual"** in science + AI ([Fast Company](https://www.fastcompany.com/91567549/claude-science)).

**Make Claude Science legible:** its edge is **auditable artifacts** (every figure carries code+environment+plain-language description+message history) and a **reviewer agent** that flags untraceable numbers/citations ([Anthropic](https://www.anthropic.com/news/claude-science-ai-workbench)). Demo moves: (1) generate a real artifact live; (2) open its provenance trail; (3) show the reviewer catching an error; (4) fork a session to compare approaches. Tarashansky's flagship demo emphasized interactive visual exploration and even **autonomous candidate proposal (PKU)** ([MIT Tech Review](https://www.technologyreview.com/2026/06/30/1139987/claude-science-is-anthropics-newest-flagship-product/)).

**Silas signal (Gladstone taste):** genome/proteome-scale screens fused with AI inference → **pure-compute, translatable, wet-lab-testable discoveries** ([Gladstone profile](https://gladstone.org/people/sukrit-silas)). Nominate specific, novel, testable claims — not a generic tool.

**3-minute demo:** ~30s problem+stakes → ~90s *live* result + headline finding → ~30s provenance/reproducibility → ~30s translational impact + proposed wet-lab step. Rehearse the click-path; pre-cache slow steps.

*Contested/unconfirmed:* no official public judging rubric exists for this event (the rubric above is extrapolated + the kickoff's "standardized criteria"); the Gladstone dataset list is single-chain reporting; do not attribute any specific PPI preprint to Silas without checking.

---

## T-cell perturbation datasets
| Dataset | Modality | Cell type | Scale | Accession | License |
|---|---|---|---|---|---|
| **Schmidt 2022** | CRISPRa Perturb-seq (+ bulk a/i) | Primary human CD4/CD8 T | ~70 hit genes scRNA | GEO **[GSE190604](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190604)** | NCBI public |
| **Shifrut 2018** (SLICE) | CRISPR KO | Primary human CD8 T | genome-wide + 20-gene scRNA | GEO **[GSE119450](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE119450)** | NCBI public |
| **Frangieh 2021** (Perturb-CITE-seq) | CRISPR KO | Melanoma + autologous TIL | ~218k cells, 248 genes | Broad **[SCP1064](https://singlecell.broadinstitute.org/single_cell/study/SCP1064)** | study terms |
| Datlinger 2017 (CROP-seq) | CRISPR KO | Jurkat ±TCR | ~5.9k cells, 29 genes | GEO [GSE92872](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92872) | NCBI public |
| Marson 2025 (bioRxiv) | CRISPRi Perturb-seq | Primary human CD4 T | ~22M cells, genome-scale | [CZI Virtual Cells](https://virtualcellmodels.cziscience.com/dataset/genome-scale-tcell-perturb-seq) | CZI terms |
| Papalexi 2021 (*method ref*) | CRISPR KO | THP-1 **myeloid** | 26 genes | GEO [GSE153056](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153056) | NCBI public |
| Replogle 2022 (*method ref*) | CRISPRi | K562/RPE1 | genome-scale | [Figshare+ 20029387](https://plus.figshare.com/articles/dataset/20029387) | CC-BY 4.0 |
| **scPerturb** (harmonized) | mixed | ~44 datasets | uniform h5ad | [Zenodo 13350497](https://zenodo.org/records/13350497) | CC-BY 4.0 |

**Pick:** Schmidt (GSE190604) or Shifrut (GSE119450) as primary autoimmune-relevant sets; Frangieh (SCP1064) for immuno-oncology; pull harmonized via [scPerturb](https://www.nature.com/articles/s41592-023-02144-y) to skip reprocessing.

**Confirm it's a perturbation screen (not observational):** a per-cell **guide-to-cell assignment** — a separate guide/feature-barcode library + guide-calls file (e.g. GSE190604 ships `...guidecalls-aggregated...txt.gz`), sgRNA metadata columns (`perturbation`, `target_gene`, `sgRNA`, `feature_call`), and **non-targeting controls**; designed low MOI (~0.1–0.3). No guide library + no NTCs ⇒ observational ⇒ causal design invalid.

**Licensing:** GEO/SRA = effectively public-domain (safest to redistribute); Zenodo/Figshare scPerturb & Replogle = CC-BY 4.0; Broad SCP (Frangieh) & CZI (Marson) = study/platform terms — confirm before bundling into an open-source repo.

*Flagged:* Frangieh GEO number unconfirmed (use SCP1064); Freimer 2022 accession unverified; Papalexi (myeloid) and Replogle (K562) are method references, not T cells.

---

## Solo-build playbook (how this changes what you do)
1. **Pick data Day 1 and prove it's a screen** — default to the Gladstone-provided T-cell set; if unclear, fall back to **GSE190604 (Schmidt CRISPRa)** and confirm guide calls + NTCs before writing pipeline code.
2. **Method spine = pertpy** — mixscape → E-distance/E-test → **pseudobulk DE (donor-aware)** → Augur → cNMF/SCENIC programs. One cited toolkit; no exotic models needed.
3. **Center the differentiator: direction-of-effect concordance** with Open Targets genetics (GPS-DOE logic). This is what turns a scatter plot into a nomination and mirrors the Minikel-2024 "genetics → 2.6× success" story.
4. **Assessment = Open Targets prioritisation + your five axes** — call OT for tractability/safety/genetics, ChEMBL for max-phase/mechanism, ClinicalTrials for status, gnomAD LOEUF + DepMap for safety, Pharos TDL for novelty. **Cache/snapshot Day 1** (endpoints throttle under load).
5. **Foundation models only where they earn it** — optional Boltz-2 (via BioNeMo in Claude Science) to show a tractability/structure angle on your hero; skip AF3 (license) and single-cell FMs (contested) unless benchmarked.
6. **Demo the discovery + the provenance** — live artifact → Claude Science provenance trail → reviewer agent → concrete proposed wet-lab experiment. Be "bilingual": science first, AI as the engine.
7. **Hero = Tbio/Tdark gene with a TYK2-shaped pattern** (concordant protective-genetics direction, tractable, selective/safe) but **no drug yet** — the novel inverse of the calibration example.

---

## Consolidated confidence & open questions
- **High confidence:** Open Targets mechanics/prioritisation; genetic-support numbers (4 primary sources); pseudobulk>cell-level DE; mixscape/E-distance as standard; BioNeMo packaging in Claude Science; dataset accessions GSE190604/GSE119450/GSE92872/SCP1064/scPerturb.
- **Contested:** magnitude of "2× genetic support" by definition/therapy area; pseudobulk vs GLMM; single-cell foundation models vs simple baselines; causal GRN inference from Perturb-seq (unsolved).
- **Unconfirmed — verify in-platform:** the official judging rubric; the exact Gladstone dataset list; Frangieh/Freimer GEO accessions. Do not attribute any specific PPI preprint to Silas.

## References
Consolidated inline above; primary anchors: Open Targets ([assoc](https://platform-docs.opentargets.org/associations), [prioritisation](https://platform-docs.opentargets.org/web-interface/target-prioritisation), [tractability](https://platform-docs.opentargets.org/target/tractability), [Ochoa 2021](https://academic.oup.com/nar/article/49/D1/D1302/5983621)) · Genetics ([Nelson 2015](https://www.nature.com/articles/ng.3314), [King 2019](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1008489), [Minikel 2024](https://www.nature.com/articles/s41586-024-07316-0), [Ochoa 2022](https://www.nature.com/articles/d41573-022-00120-3)) · Pharos ([TCRD](https://academic.oup.com/nar/article/49/D1/D1334/5958490)) · Methods ([Squair 2021](https://www.nature.com/articles/s41467-021-25960-2), [Zimmerman 2021](https://www.nature.com/articles/s41467-021-21038-1), [scPerturb 2024](https://www.nature.com/articles/s41592-023-02144-y), [pertpy 2025](https://www.nature.com/articles/s41592-025-02909-7), [Augur 2021](https://www.nature.com/articles/s41587-020-0605-1), [SCENIC+ 2023](https://www.nature.com/articles/s41592-023-01938-4), [Ota 2025](https://www.nature.com/articles/s41586-025-09866-3), [GPS-DOE 2023](https://www.nature.com/articles/s41588-023-01609-2)) · Models ([Evo 2](https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1.full), [Boltz-2](https://github.com/jwohlwend/boltz), [AF3 license](https://github.com/google-deepmind/alphafold3/blob/main/LICENSE), [ESM](https://github.com/facebookresearch/esm), [scFM critique](https://www.nature.com/articles/s41592-025-02772-6), [BioNeMo](https://blogs.nvidia.com/blog/claude-science-bionemo-agent-toolkit/)) · Strategy ([Cerebral Valley](https://cerebralvalley.ai/e/built-with-claude-life-sciences), [Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench), [MIT Tech Review](https://www.technologyreview.com/2026/06/30/1139987/claude-science-is-anthropics-newest-flagship-product/), [Fast Company](https://www.fastcompany.com/91567549/claude-science), [Silas](https://gladstone.org/people/sukrit-silas)) · Datasets ([Schmidt 2022](https://www.science.org/doi/10.1126/science.abj4008), [Shifrut 2018](https://www.cell.com/cell/fulltext/S0092-8674(18)31333-3), [Frangieh 2021](https://www.nature.com/articles/s41588-021-00779-1), [scPerturb Zenodo](https://zenodo.org/records/13350497)).
