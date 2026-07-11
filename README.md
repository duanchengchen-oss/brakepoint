# Causal T-cell Target Discovery — Built with Claude Science

**Built with Claude: Life Sciences · research track (solo).** A reproducible pipeline that ranks CRISPR perturbations in **primary human T cells** by **causal effect size**, validates itself against known biology, and nominates a novel, genetically-concordant, **druggable** target — every step carrying Claude Science provenance.

> **Demo (≤3 min):** `DEMO_URL` · **Landing page:** `deliverables/index.html` · **Written summary:** `deliverables/summary.md`

## The finding
On the **genome-scale Gladstone CRISPRi Perturb-seq** (2.44M primary human CD4⁺ T cells, 12,449 perturbations, scVI-integrated, knockdown-gated), the pipeline — **unsupervised** — recovers the entire TCR-signaling module (ZAP70, CD3D/E/G, PLCG1, LAT, VAV1). Diffusing the causal signal over the human interactome then re-discovers **IL2RB** (the IL-2/IL-15 receptor β): never a direct hit, yet network-central among causal nodes, carrying multiple-sclerosis and type-1-diabetes genetics, and drug-adjacent via IL-2-pathway agonists — a real, actionable immune node surfaced from raw data. Genuinely undrugged **VAV2** and **BLNK** mark the novel frontier. (Public-data validation first re-nominated **RASA2**, a *Nature*-2022 CAR-T enhancer, and lead **CBLB**, an immune brake already in trials.) Full write-ups: [`pipeline/real-finding-genomescale.md`](pipeline/real-finding-genomescale.md) · [`pipeline/real-finding.md`](pipeline/real-finding.md).

## Why it's trustworthy
- **Ranks by causal effect size** (power-equalized energy distance + permutation E-test), not p-values — significance inflates with cell count.
- **Gated:** viability (catches toxic knockouts), modality-aware on-target, **donors as replicates**.
- **Differentiator:** human-genetics **direction-of-effect concordance** — reported as an honest coverage funnel, not a cherry-picked hit.
- **Self-checking:** we found and fixed a real statistical bug (an n-dependent bias in the effect-size metric) that Claude Science's reviewer helped surface — see [`pipeline/WAR_LOG.md`](pipeline/WAR_LOG.md).

## Reproduce
```bash
cd pipeline
make smoke                 # dependency-free unit test of the core statistic (runs anywhere)
make hero DATA=<h5ad> CONTROL=<label> MODALITY=<KO|CRISPRi|CRISPRa>
```
Fixed seeds, pinned `environment.yml`, one-command regeneration. For genome-scale runs use `--embedding X_scVI --max-cells-per-group 300`.

## How Claude Science got us there
Every result is a versioned artifact carrying its exact code, environment, and conversation trail; a background reviewer checks claims against what actually ran. The heavy genome-scale analysis runs on an **NVIDIA DGX Spark** over Claude Science's SSH remote-compute ([`dgx-spark-claude-science.md`](dgx-spark-claude-science.md)).

## Repository
```
pipeline/            edistance_core.py · run_pipeline.py · concordance.py · SKILL.md · Makefile · environment.yml · LICENSE (MIT) · SOURCES.md
pipeline/outputs*/   ranked_perturbations.csv + figures (real runs)
pipeline/real-finding.md   the finding, with real numbers
deliverables/        demo_storyboard.md · summary.md · index.html · hero_convergence.svg
CONTEXT.md           full project handoff · gladstone-datasets-integration.md · research-track-target-discovery-plan.md · target-assessment-framework.md
```

## Data & license
Code: **MIT** ([`pipeline/LICENSE`](pipeline/LICENSE)). Datasets: Gladstone-provided immune T-cell Perturb-seq, protein-interaction network, and regulatory-activity model; public validation sets (Shifrut/Marson, Datlinger) via scPerturb. Provenance and licenses in [`pipeline/SOURCES.md`](pipeline/SOURCES.md). Only openly-licensed evidence sources are bundled (no DrugBank).

---
*Replace `REPO_URL` and `DEMO_URL` before submission.*
