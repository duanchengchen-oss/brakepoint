# Brakepoint methods: how it works, end to end

Brakepoint turns a genome-scale perturbation screen into a map of candidate T-cell brakes: not only how much each gene shutoff changes the cell, but whether that change makes the cell a stronger or weaker fighter. It is a computational discovery pipeline applied to the public Marson lab (Gladstone) and Pritchard lab (Stanford) screen (bioRxiv 10.64898/2025.12.23.696273), built to nominate the next functional experiments rather than declare finished targets.

## The data, and how we cleaned it

The starting point is causal at the gene level: switch genes down, then read the resulting cell state. We used the CZI Virtual Cells Platform dataset `genome-scale-tcell-perturb-seq`, build `GWCD4i_Stim8hr_D1D2.built.h5ad`: primary human CD4+ T cells from donors D1 and D2, stimulated for 8 hours, with non-targeting guides labeled `control`.

The build contains 2,638,736 single cells and 4,816 measured highly variable genes, with gene identities stored as Ensembl IDs. It covers 12,449 gene knockdowns; 11,438 had at least 30 cells pooled across both donors and entered the E-distance test.

Quality control used median-absolute-deviation gates on total counts, genes detected per cell, and mitochondrial content, with `pct_mt < 15`. The magnitude leaderboard ran on 2,436,881 QC-passing cells; the roughly 202,000-cell difference from the full dataset is QC, not unexplained attrition. The signed direction axis scored all 2,638,736 cells.

The unit of analysis is the target gene. Guides were pooled to gene level, while the authors' per-guide knockdown-efficiency measurements were reserved for a nomination QC gate. Perturbations below the fitness threshold remain visible with a depletion flag instead of disappearing from the evidence.

## One map for millions of cells

Every comparison happens in one donor-integrated map of cell state. We used the scVI latent already supplied in the build at `adata.obsm['X_scVI']`; it places D1 and D2 cells in a shared deep-learning coordinate system after removing donor and batch structure.

That choice matters because raw expression differences can mix biology with technical structure. The supplied latent makes knockdown and control cells directly comparable while preserving a genome-scale representation of state. We did not retrain scVI here: the pipeline consumes the integrated latent in the public build and makes every distance calculation on that fixed representation.

## Axis 1 — how hard each shutoff hits the cell

The first axis asks one clean question: how far does a knockdown move the cell away from control? We measure that displacement with the power-equalized energy distance used in scPerturb and Peidli et al. (Nature Methods, 2024), implemented as in PertPy. Brakepoint claims no new Perturb-seq statistic; the advance is how magnitude is paired with direction and evidence.

For knockdown cells `X` and control cells `Y`, both subsampled to a common count `n`, the squared-Euclidean energy distance is the cross-group mean squared distance, taken twice, minus each cloud's own within-group mean squared distance:

```
E  =  2 · mean‖xᵢ − yⱼ‖²  −  mean_{i≠j}‖xᵢ − xⱼ‖²  −  mean_{i≠j}‖yᵢ − yⱼ‖²
```

Read plainly: how far apart the two clouds of cells sit, corrected for how spread out each cloud is on its own. One detail turns out to matter enormously — the within-group terms average over pairs of *different* cells only (divide by `n(n−1)`), excluding the zero self-distance of a cell with itself. That is the unbiased U-statistic; the biased `n²` form silently corrupts the ranking, which is exactly the bug the pipeline later caught itself making (see "The pipeline that caught its own bug").

Coverage varies sharply across knockdowns, so raw distance estimates would have unequal power. Each group, including control, is capped to a few hundred cells. For every knockdown-versus-control comparison, both sides are subsampled without replacement to `n = min(n_pert, n_ctrl)`, with `seed=0`. The result is an effect-size leaderboard built from matched comparison power.

Significance comes from a 1,000-permutation label-shuffle E-test. Its one-sided empirical p-value is `(1 + number of shuffles with E ≥ observed) / (1 + 1000)`, followed by Benjamini-Hochberg correction across exactly 11,438 tested knockdowns to produce `e_qval`.

The q-value is a gate, not the ranking. At this scale, the standard test lights up for almost everything: 11,149 of 11,438 knockdowns, or 97.5%, clear `q < 0.05`, and 9,802 pile up at the exact permutation floor, the smallest p-value the test can return (about 1/1001). Significance has saturated and cannot separate the targets that matter. Brakepoint therefore ranks by E-distance magnitude.

Fitness remains explicit. `viability_ratio` is the knockdown cell count divided by the median knockdown cell count; values below 0.5 raise a depletion or toxicity flag. Nomination requires `q < 0.05`, viability at least 0.5, and the authors' per-guide knockdown-efficiency confirmation. The raw leaderboard remains intact.

## Axis 2 — which way it pushes the cell

Magnitude says that a cell changed; direction says whether the change is useful. For each cell, we normalized total counts to 10,000, applied a log transform (`log1p`), and took one signed score:

```
direction_score  =  mean(effector genes)  −  mean(dysfunction genes)
```

We compared that score with control, aggregated it for each knockdown and donor, then averaged D1 and D2. A separate sign-agreement flag records whether both donors point the same way. The donors are the biological replicates; with only two of them, this is a consistency check, not donor-population inference.

**Effector / activation module**

| Genes | Coverage |
|---|---:|
| IFNG, IL2, TNF, CSF2, LTA, XCL1, XCL2, CCL3, CCL4, GZMB, TNFRSF9, CD69, MYC, IRF4, BATF, TBX21 | 16/16 |

**Dysfunction / exhaustion module**

| Genes | Coverage |
|---|---:|
| PDCD1, CTLA4, LAG3, HAVCR2, TIGIT, BTLA, CD160, VSIR, ENTPD1, TOX, NR4A1, NR4A2, NR4A3 | 13/13 |

A positive score means the shutoff pushes cells toward the effector program: a candidate brake has been released. A negative score means the shutoff removes essential machinery or an enhancer of function.

The genome-scale signed pass scored all 2,638,736 cells in 38.9 seconds on an NVIDIA DGX Spark (GB10) through Claude Science, excluding preprocessing and model fitting. The implementation streams the matrix in row chunks and densifies only the 29 module columns, so memory stays flat as cell count grows. Both modules resolved completely.

The distribution is left-shifted: its 50th, 75th, 95th, and 99th percentiles are -0.037, +0.029, +0.144, and +0.312. Featured brakes at +0.05 to +0.15 therefore sit in roughly the upper 5-25% of the direction distribution.

## Why this beats the usual approach

The decisive comparison is simple: significance alone cannot rank this screen, while effect size alone promotes the genes a T cell needs most. Of the top 20 knockdowns by effect size, 18 push the cell toward a weaker fighter state when switched off; their mean direction is -0.43. Fourteen of the top 15 are negative. Eight of the nine largest effects are the T-cell receptor signaling module itself: ZAP70, LCP2, CD3E, CD3G, PLCG1, LAT, VAV1, and CD3D. A naive hit list hands you genes you must never inhibit.

The signed axis changes the search. Every one of those TCR-module genes is strongly negative and donor-consistent, so the machinery drops out while candidate brakes rise into the positive quadrant. Among the 11,438 tested knockdowns, 2,016 exceed the +0.05 neutral band, and 1,286 of those point positive in both donors. That is a candidate-brake search space an unsigned pipeline cannot see. The contrast is shown in [`naive_vs_signed.png`](../deliverables/figures/naive_vs_signed.png).

- **Significance or DE-count ranking:** saturated and unsigned; it detects that something changed, not whether inhibition helps.
- **Differential expression:** finds correlations, not a causal target or a therapeutic direction.
- **GWAS:** points to loci, but rarely identifies the operative cell type or which direction to move the gene.
- **Bulk viability screening:** cannot distinguish “kills the cell” from “makes a better fighter.”

Brakepoint fills each blind spot by joining causal perturbation, effect magnitude, functional direction, donor consistency, and fitness in the same target-level record.

## Reading the evidence: seven convergent axes

No single score is allowed to bury the biology. Each candidate is read across seven independent lines of evidence: **Causal effect**, **Brake direction**, **Donor consistency**, and **Viability (fitness)** are measured in the screen; **Druggability**, **Immune genetics**, and **Clinical precedent** are curated from public dossiers in Open Targets, ChEMBL v34, ClinicalTrials.gov v2, and STRING v12.

Each axis is summarized from 0 to 1. These values are not fitted weights and are not added into a composite winner. The correct reading is across a candidate's row: where the evidence converges, where it conflicts, and what the next experiment must resolve.

## The pipeline that caught its own bug

The pipeline's strongest quality-control result was catching a ranking error before it became a biological result. An adversarial self-critique reproduced an n-dependent bias in the original E-distance code: the within-group terms averaged all `n²` pairs, including the zero self-distance diagonal. That biased V-statistic adds an offset of roughly `4d/n` — about 5.0 at n = 40 in the 50-dimensional case the regression test pins.

Because each knockdown was power-equalized at its own available `n`, the offset varied by target and corrupted the magnitude ranking itself. A pure-null knockdown with 40 cells could score `E ≈ 5` on bias alone and outrank a real effect.

The correction was exact: exclude the diagonal and divide within-group sums by `n(n−1)`, yielding the unbiased U-statistic. After the fix, the null converges on zero and no longer depends on sample size: n = 40 gives `E = −0.28` and n = 500 gives `E = 0.009`, instead of roughly 5.0 at n = 40. The real effect remains intact at `E = 43.9`, close to the analytic `2‖μ‖² = 45`, with `p = 0.002`.

That correction now lives behind a regression assertion in `edistance_core._smoke`. It was caught by the active self-critique loop, not a passive reviewer after publication.

## Reproduce it

Reproduction is tiered so every claim can be checked at the lightest sufficient level. All stochastic steps use `seed=0`, and the environment is version-pinned in `environment.yml`.

| Tier | Command | What it verifies |
|---:|---|---|
| 1 | `make smoke` | Runs anywhere with NumPy only; tests the E-distance core, signed direction axis, figure logic, and diagonal-bias regression guard. |
| 2 | `make figure` | Rebuilds the target matrix and full figure set from shipped results, with no data download or GPU. |
| 3 | `python brake_enrichment.py` | Recomputes the curated known-brake enrichment test. |
| 4 | `make direction DATA=... LIB=... CONTROL=control` | Recomputes the signed axis on the public genome-scale build; requires the built h5ad, sgRNA-library metadata, and a GPU environment. This is the 2.64-million-cell, 38.9-second pass. |

Every result is a versioned Claude Science artifact containing code, environment, and conversation trail. A provenance reviewer checks each claim against its run and outputs. Heavy computation ran remotely on the DGX Spark over SSH.

## The result, and its honest edges

Brakepoint nominates five candidate T-cell brakes for the next experiment:

- **CBLB**, the lead, rediscovered blind from the raw screen; oral CBL-B inhibitors are already in trials, including NX-1607 Phase 1 (`NCT05107674`) and HST-1011 Phase 1/2 (`NCT05662397`).
- **CD5**, donor-consistent.
- **DGKA**, donor-consistent; Bayer's oral DGKalpha inhibitor BAY2862789 is in Phase 1.
- **SMAD3**, the highest-effect-size positive candidate among the five and a TGF-beta pathway node.
- **UBASH3A**, an autoimmune-GWAS phosphatase that is currently undrugged, making it a genetics-led candidate.

The boundary is precise: this analysis covers D1 and D2 at Stim 8 h, two of four available donors. The broad curated set of 29 known brakes is not yet statistically enriched in the positive quadrant against the matched two-donor background (one-sided Mann-Whitney p = 0.70). That is a power limit and an inconclusive result, not evidence of no effect; the estimate sharpens at full scale in the four-donor cohort. CBLB, SMAD3, and UBASH3A are donor-split, while CD5 and DGKA are donor-consistent.

All read-outs are transcriptional. These five candidates are rigorous hypotheses for functional testing, not validated drugs or finished targets.

---
**Chengchen (Sam) Duan** · duanchengchen@gmail.com · github.com/duanchengchen-oss
