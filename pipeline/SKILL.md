---
name: tcell-perturb-causal-targets
description: >
  Causal target discovery from T-cell perturbation (Perturb-seq/CRISPR) data. Use when a
  user has a single-cell perturbation dataset (.h5ad with per-cell guide/perturbation calls)
  and wants to rank perturbations by causal effect size and nominate drug targets. Runs
  QC -> normalize -> power-equalized E-distance + permutation E-test -> viability & knockdown
  checks -> donor-aware pseudobulk DE -> transparent gated ranking. Load this skill in
  Claude Science to run the pipeline and produce auditable, reproducible artifacts.
---

# T-cell Perturb-seq causal-target pipeline

## When to use
A user has a T-cell (or other) single-cell perturbation screen and asks to find which
perturbations causally move cell state, and which genes to nominate as targets.

## Inputs
- An `.h5ad` with raw counts and `.obs['perturbation']` (guide/target per cell) and a
  control label (e.g. `NT`), ideally `.obs['donor']`. Default dataset: Shifrut & Marson 2018
  (GSE119450) via the scPerturb harmonized file `ShifrutMarson2018.h5ad`.

## Steps (run each as its own message so each gets its own provenance artifact)
1. **Load & audit** — read the `.h5ad`; report cells×genes, perturbations, guides/gene,
   donors, and controls. **Confirm it is a perturbation screen** (per-cell guide calls +
   non-targeting controls). If not, stop and tell the user.
2. **QC** — MAD-based filtering (counts, genes, %mito); keep raw counts in `layers['counts']`.
3. **Normalize** — CP10k → log1p → 2k HVG → scale → 50 PCs (seed=0).
4. **Effect size** — for each perturbation vs control, **power-equalized E-distance**
   (subsample to common n) + permutation E-test. **Rank by E-distance magnitude; use the
   permutation q only as a gate** (significance scales with cell count).
5. **Viability & knockdown** — per-perturbation cell recovery vs control (flag <0.5 =
   toxicity/dropout); target-gene expression drop vs control (on-target proof).
6. **Donor-aware pseudobulk DE** — aggregate raw counts per (perturbation × donor) →
   pydeseq2 with donor in the design; require ≥2 concordant guides/gene and (where possible)
   ≥3 donors; report per-donor consistency.
7. **Direction-of-effect funnel** (top hits only) — via the Open Targets connector, for each
   hit count: any GWAS → genome-wide-significant → strand/direction assignable → concordant
   with the perturbation's direction. Report coverage honestly; treat "no direction" as
   missing, not negative.
8. **Score & nominate** — transparent gates (significant, viable, on-target, replicated) then
   rank within tier by E-distance; nominate one novel, tractable, concordant "hero" target +
   a proposed wet-lab experiment.
9. **Export** — write `outputs/ranked_perturbations.csv` + figures to the shared folder;
   save this pipeline as a reusable skill so future sessions inherit it.

## Scripts
- `edistance_core.py` — dependency-free E-distance + E-test (unit-tested via `make smoke`).
- `run_pipeline.py` — steps 1–6 + gated ranking; `--synthetic` for a self-test.
- `environment.yml`, `Makefile` (`make smoke|synthetic|hero`).

## Rigor (do not skip — these are how you earn a judge's trust)
Rank by effect size not p; flag viability (it reverses naive ranking); prove on-target
knockdown; report donors and use them as replicates (not cells); pre-register the genetic
concordance coverage funnel; fix seeds; ship a lockfile and one-command `make hero`.
