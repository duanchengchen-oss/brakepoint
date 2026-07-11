# CONTEXT — Built with Claude: Life Sciences (research track, solo)
**Single-source project handoff. Any Claude Science / Claude Code session should read this first.** Last updated Day 3 (2026-07-09).

## 1. What & why
Solo entry, **research track**, causal **target discovery from T-cell perturbation (Perturb-seq/CRISPR)** data, run through **Claude Science**. Aim: **Top-3**. Partner: **Gladstone Institutes** (special prize: "most potential to advance science that can overcome disease").

## 2. Event mechanics (hard facts)
- **Dates:** Jul 7–13 2026. **Submission deadline: Mon Jul 13, 9:00 PM ET** on the CV platform.
- **Three deliverables:** demo video **≤3 min** · **open-source repo** (approved license) · written summary **100–200 words**.
- **Judging:** Stage 1 async (Jul 14–15) → **Top 6**; Stage 2 live (Jul 16) plays each finalist's pre-recorded 3-min demo → 1st/2nd/3rd. **No live pitch** — the video is the whole score.
- **Rules:** New Work Only (build during event; public data ok; don't paste a pre-built private pipeline) · everything open-source · teams 1–2.
- **Prizes (research):** 1st $30k, 2nd $10k, 3rd $5k (Usage Credits) + Gladstone Award.
- **Track brief:** "Using Claude Science, start from a biological question … submit a finding/model/analysis others can reproduce — and **show us how Claude Science got you there**." → make the CS provenance + reviewer visible in the demo.

## 3. Status (Day 3)
- ✅ Pipeline built + **bug-fixed** (E-distance diagonal-bias → now unbiased, null≈0 at all n).
- ✅ **Datlinger (Jurkat) validation run** (real, Claude Science): recovers TCR-signaling hierarchy (ZAP70/LAT + SHP1/2 + AP-1/NFAT/NF-κB). Top druggable hit **PTPN11/SHP-2** (36 trials incl. Ph3).
- ✅ **Shifrut (primary human CD8⁺ T) headline run** (real): 24,998 cells, 20 perts, 2 donors. Recovers TCR core (CD3D, LCP2); re-nominates **RASA2** (Nature-2022 CAR-T enhancer) from effect size; lead = **CBLB** (genome-wide-sig `risk_lof` brake, oral CBL-B inhibitors NX-1607/HST-1011 in trials). Honest concordance funnel: 8→2→1→1→**0** strictly-novel-concordant (panel is all known brakes).
- 🔜 **Genome-scale run** (in progress path): larger primary-T-cell Perturb-seq via **scvi-tools** integration on the **DGX Spark** (see §7) to nominate a truly novel hero.

## 4. The pipeline (`pipeline/`)
- `edistance_core.py` — power-equalized E-distance + permutation E-test (unbiased U-statistic; `make smoke` passes anywhere).
- `run_pipeline.py` — load → QC (MAD) → normalize → **embedding** (PCA *or* provided `X_scVI`) → E-distance ranking → viability + modality-aware on-target gates → gated ranking. Flags: `--data --control --modality {KO,CRISPRi,CRISPRa} --embedding X_pca|X_scVI --max-cells-per-group N --outdir`.
- `concordance.py` — direction-of-effect funnel (uses OT `directionOnTarget`/`directionOnTrait`; snapshot in `dossiers/concordance_snapshot.json`).
- `SKILL.md` (reusable Claude Science skill), `environment.yml`, `Makefile` (`make smoke|synthetic|hero`), `LICENSE` (MIT), `SOURCES.md`.
- Outputs → `pipeline/outputs/ranked_perturbations.csv` (+ figure). Dossiers → `pipeline/dossiers/`. Live status → `pipeline/WAR_LOG.md`. Findings → `pipeline/real-finding.md`.
- **Git repo initialized** (local). Public remote needs Sam's GitHub.

## 5. Rigor decisions (don't regress these)
Rank by **E-distance magnitude**, permutation q only a gate (significance scales with cell count). **Viability** flag computed before any low-cell drop (catches toxic KOs). **On-target** is modality-aware (KO mRNA-FC uninformative → NaN). **Donors as replicates** (pseudobulk next). **Concordance** is a differentiator + honest coverage funnel, not the primary sort. Fixed seeds + lockfile + one-command repro.

## 6. Target-assessment framework (`target-assessment-framework.md`)
5 axes: **Confidence** (causal + genetics direction; genetic support ≈2.6× success), **Druggability** (Open Targets tractability, ChEMBL), **Safety** (gnomAD LOEUF, DepMap, HPA/GTEx), **Novelty** (Pharos TDL), **Development/Clinical** (ChEMBL max-phase, ClinicalTrials). Data sources are free/open; **DrugBank excluded** (CC-BY-NC, incompatible with OSS submission).

## 7. Compute
- **Primary (preferred): DGX Spark over SSH** — see `dgx-spark-claude-science.md`. It's a supported Claude Science **workstation host (no Slurm needed)**; ARM64 + Blackwell GPU + 128 GB unified. Use for scVI + genome-scale. *Pending: Sam's `~/.ssh/config` Host alias.*
- Fallback: **Modal** GPU (in Claude Science) or the laptop (small runs only).

## 8. Tools / skills / connectors available
- **bio-research plugin** (installed): skills `single-cell-rna-qc`, `scvi-tools`, `nextflow-development`, `scientific-problem-selection`; MCPs **Open Targets (ot)**, **ChEMBL**, **ClinicalTrials (c-trials)**, **PubMed**, **Consensus**, **bioRxiv**. (BioRender/Synapse/Wiley/Owkin need OAuth.)
- Other MCPs: alphaXiv (reads GitHub), LatchBio (nf-core — not used, not a fit).
- Use PubMed/Consensus/bioRxiv for the **novel-hero literature + novelty check** (not yet done — waiting on the genome-scale hero).

## 9. Open items / NEEDS SAM
- **Genome-scale run on the Spark** → nominate a novel, genetically-concordant hero (the current headline gap).
- Wire `concordance.py` into `make hero`; add donor-aware **pseudobulk DE** (pydeseq2).
- **Bidirectional replication**: Schmidt CRISPRa should move the hero's program opposite to KO (best demo figure; "never cut").
- **GitHub handle** → public OSS remote + index prior code (alphaXiv).
- **3-min demo video** + final 100–200 word summary (submission).
- Confirm the official **judging rubric** (platform/Discord).

## 10. How to run (quick)
- Local smoke (anywhere): `cd pipeline && make smoke`.
- Real run (Claude Science / Spark): `python run_pipeline.py --data <h5ad> --control <label> --modality <KO|CRISPRi|CRISPRa> [--embedding X_scVI --max-cells-per-group 300]`.
- After outputs land, the scheduled **results-watcher** (every 6h) + Sam's session enrich dossiers and draft the finding/demo.
