# SOURCES — datasets, evidence, tools, licenses (open-source compliance)
Snapshot everything on Day 1 and fill the dates. Do NOT bundle non-OSS / non-commercial data into the repo.

## Datasets
| Dataset | Use | Accession | License | Snapshot date |
|---|---|---|---|---|
| Shifrut & Marson 2018 (primary human CD8⁺ T, CRISPR KO) | primary | GEO GSE119450 via scPerturb `ShifrutMarson2018.h5ad` (Zenodo 13350497) | CC-BY-4.0 | _fill_ |
| Datlinger 2017 (CROP-seq Jurkat) | smoke / fallback | GEO GSE92872 | NCBI public | _fill_ |
| Frangieh 2021 (Perturb-CITE-seq, melanoma+TIL) | IO fallback | Broad SCP1064 | study terms — verify before redistribution | _fill_ |
| Schmidt 2022 (CRISPRa/i primary human T) | bidirectional replication (stretch) | GEO GSE190604 | NCBI public | _fill_ |

## Evidence APIs (free / open)
Open Targets (permissive) · ChEMBL (CC BY-SA) · ClinicalTrials.gov (public domain) · gnomAD · DepMap (CC BY) · GTEx · Human Protein Atlas (CC BY-SA) · Pharos/TCRD.
**NOT used:** DrugBank full dataset — CC BY-NC + application-gated, incompatible with an open-source submission.

## Tools
scanpy · pertpy · scperturb · pydeseq2 · decoupler · anndata · numpy/pandas/scipy/scikit-learn (see `environment.yml`). All OSI/permissive.

## This repo
Licensed MIT (see `LICENSE`).
