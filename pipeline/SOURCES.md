# SOURCES — datasets, evidence, tools, licenses (open-source compliance)
All sources are snapshotted with the dates below; no non-OSS / non-commercial data is bundled into the repo.

## Datasets
| Dataset | Use | Accession | License | Snapshot date |
|---|---|---|---|---|
| **Gladstone genome-scale CD4⁺ T-cell CRISPRi Perturb-seq** (Marson lab) | **primary (the finding)** | CZI Virtual Cells Platform `genome-scale-tcell-perturb-seq`; build `GWCD4i_Stim8hr_D1D2.built.h5ad` (donors D1+D2, Stim 8 h); bioRxiv 10.64898/2025.12.23.696273 | MIT (data-sharing) | 2026-07-10 |
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
These are **public annotation layers applied on top of** the provided data; where seeded
from the screen (e.g. STRING diffusion) they are add-on layers, **not independent validation**.
- **STRING v12** (human interactome, high-confidence edges ≥700) — public PPI used for the
  network-propagation layer. CC BY 4.0. Accessed 2026-07-10.
- **Open Targets** (permissive) — human-genetics / disease-association layer. Accessed 2026-07-11.
- **ChEMBL v34** (CC BY-SA) · **ClinicalTrials.gov API v2** (public domain) · gnomAD · DepMap (CC BY) · GTEx · Human Protein Atlas (CC BY-SA) · Pharos/TCRD. MCP-verified dossiers in `dossiers/*.json`; accessed 2026-07-11.

**NOT used:** DrugBank full dataset — CC BY-NC + application-gated, incompatible with an open-source submission.

## Tools
scanpy · pertpy · scperturb · pydeseq2 · decoupler · anndata · numpy/pandas/scipy/scikit-learn (see `environment.yml`). All OSI/permissive. The E-distance magnitude statistic + permutation E-test follow the scPerturb / Peidli et al. (Nat Methods 2024) standard (implemented as in PertPy); no new statistic is claimed.

## Run manifest (reproducibility)
- Build: `GWCD4i_Stim8hr_D1D2.built.h5ad` · embedding `X_scVI` · control label `control`.
- Global `seed = 0`; E-test `n_perm = 1000`, one-sided empirical p, Benjamini–Hochberg FDR over the 11,438 tested perturbations.
- Environment pinned in `environment.yml`; heavy compute on the DGX Spark (NVIDIA GB10).
- Outputs: `outputs_gladstone/ranked_perturbations.csv`, `direction_scores_raw.csv`, `run_meta.json`, `direction_meta.json`.

## This repo
Licensed MIT (see `LICENSE`).
