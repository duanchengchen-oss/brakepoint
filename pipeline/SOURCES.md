# SOURCES — datasets, evidence, tools, licenses (open-source compliance)
Snapshot everything on Day 1 and fill the dates. Do NOT bundle non-OSS / non-commercial data into the repo.

## Datasets
| Dataset | Use | Accession | License | Snapshot date |
|---|---|---|---|---|
| **Gladstone genome-scale CD4⁺ T-cell CRISPRi Perturb-seq** (Marson lab) | **primary (the finding)** | CZI Virtual Cells Platform `genome-scale-tcell-perturb-seq`; bioRxiv 10.64898/2025.12.23.696273 | MIT (data-sharing) | 2026-07-10 |
| Shifrut & Marson 2018 (primary human CD8⁺ T, CRISPR KO) | public validation / fallback | GEO GSE119450 via scPerturb `ShifrutMarson2018.h5ad` (Zenodo 13350497) | CC-BY-4.0 | 2026-07-09 |
| Datlinger 2017 (CROP-seq Jurkat) | smoke / fallback | GEO GSE92872 | NCBI public | 2026-07-09 |
| Frangieh 2021 (Perturb-CITE-seq, melanoma+TIL) | IO fallback | Broad SCP1064 | study terms — verify before redistribution | _n/a (not used)_ |
| Schmidt 2022 (CRISPRa/i primary human T) | bidirectional replication (stretch) | GEO GSE190604 | NCBI public | _n/a (not used)_ |

**What the Gladstone share actually contains** (per `data_sharing_readme.md`):
per-cell + pseudobulk Perturb-seq expression, a genome-wide **DESeq2 differential-
expression result**, and supplementary signature/validation tables (Th1/Th2
polarization, autoimmune-cluster enrichment, arrayed validation, aging). **It does
NOT include a protein-interaction network or a regulatory-activity model** — those
were never provided; the event page's "three datasets" framing did not match the
delivered share.

## Evidence layers (free / open — public, NOT provided by Gladstone)
- **STRING v12** (human interactome, edges ≥700) — public PPI used for the
  network-propagation convergence layer. CC BY 4.0.
- **Open Targets** (permissive) — human-genetics / disease-association layer.
- ChEMBL (CC BY-SA) · ClinicalTrials.gov (public domain) · gnomAD · DepMap (CC BY) · GTEx · Human Protein Atlas (CC BY-SA) · Pharos/TCRD.

**NOT used:** DrugBank full dataset — CC BY-NC + application-gated, incompatible with an open-source submission.

## Tools
scanpy · pertpy · scperturb · pydeseq2 · decoupler · anndata · numpy/pandas/scipy/scikit-learn (see `environment.yml`). All OSI/permissive.

## This repo
Licensed MIT (see `LICENSE`).
