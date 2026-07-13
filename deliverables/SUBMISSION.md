# Brakepoint — submission form answers

**Built with Claude: Life Sciences (Anthropic × Cerebral Valley × Gladstone Institutes) · Research track.**
Copy each block into the matching field on the Cerebral Valley submission form. (Field names below are the common CV/hackathon set — map them to whatever the live form asks; everything you need is here.)

---

### Project name
Brakepoint

### Tagline / one-line description (≤120 chars)
Brakepoint scans the genome for T-cell brakes and tells drug targets from essential machinery.

### Track
Research ("build from the bench") — a reproducible finding from a Gladstone dataset.

### Participant / team (max 2)
Chengchen (Sam) Duan — solo · duanchengchen@gmail.com · github.com/duanchengchen-oss

### Dataset used
The genome-scale primary human CD4⁺ T-cell CRISPRi Perturb-seq screen from the **Marson lab (Gladstone)** with the **Pritchard lab (Stanford)** — 2,638,736 cells, 12,449 knockdowns (bioRxiv 10.64898/2025.12.23.696273; CZI Virtual Cells Platform). Brakepoint is a computational discovery on this public data — the analysis that turns the screen into a ranked, testable target list.

---

### Elevator pitch (2–3 sentences)
The best cancer immunotherapies cut the brakes off T cells, but only a handful of those brakes have ever been drugged. Brakepoint reads a public 2.6-million-cell, genome-wide human T-cell screen and tells a real candidate target from the machinery a cell needs to survive — with zero prior hints, it rediscovered CBLB, already advancing through clinical trials, and surfaced four more candidates. One person built the fully reproducible system in one week, running the analysis on an NVIDIA DGX Spark through Claude Science.

### What it does / the finding
Brakepoint delivers a ready-to-test pipeline of **five candidate T-cell brake targets**, each scored across seven independent lines of evidence — genes whose shutdown pushes human T cells toward a stronger fighter (the direction checkpoint drugs exploit):
- **CBLB (lead) — the face-validity proof.** Brakepoint rediscovered it from raw data with zero prior hints. Oral CBL-B inhibitors NX-1607 (NCT05107674, Phase 1) and HST-1011 (NCT05662397, Phase 1/2) are already in trials.
- **CD5** — deleting it enhances CAR-T cells in preclinical studies.
- **DGKA** — Bayer has advanced an oral inhibitor into Phase 1.
- **SMAD3** — a high-effect control point in the TGF-β pathway.
- **UBASH3A** — a currently undrugged phosphatase backed by type 1 diabetes and rheumatoid arthritis genetics.

### How it works (the method)
1. **Rank genes by how hard switching them off hits the cell, not by p-value.** At 2.6 million cells, about 97.5% of knockdowns clear q<0.05, so significance can no longer rank targets. Brakepoint compares every perturbation at a common cell count and uses a 1,000-permutation test only as a gate (power-equalized E-distance).
2. **Measure which way each gene pushes the cell.** A signed direction score — toward a stronger fighter or a weaker state (per-cell effector-vs-dysfunction axis) — unmasks the 14 of the 15 largest effects that are essential machinery the T cell can't live without, and surfaces the real candidate brakes.
3. **Demand convergent support before naming a candidate.** Brakepoint scores the final five (CBLB, CD5, DGKA, SMAD3, UBASH3A) across seven independent lines of evidence: causal effect, direction, donor consistency, screen fitness, target tractability, immune genetics, and clinical precedent.

### Novelty (stated honestly)
The statistic (energy-distance / E-test) is the **scPerturb standard — not a new method.** Brakepoint's contribution is the **combination**: genome-scale, coverage-equalized effect-size ranking **plus** a signed effector-vs-dysfunction axis **plus** an IO-brake druggability shortlist, reported with its null. The signed axis is the piece an unsigned effect-size ranking omits, and it's what tells a brake from the machinery.

### How I used Claude Science & Claude Code
- **Claude Science ran the genome-scale analysis on a remote NVIDIA DGX Spark.** It scored the direction of all 2,638,736 cells in about 40 seconds and built the E-distance leaderboard on 2.44 M post-QC cells with scVI donor integration.
- **Every result is auditable and reproducible.** Each output is a versioned artifact carrying its exact code, environment, and conversation trail, and a background **reviewer agent** checks every claim against what actually ran.
- **Claude caught a real bug before it could reach a conclusion.** An adversarial self-critique found an n-dependent bias in the E-distance — a pure null scoring ~5 instead of ~0 — and fixed it (biased V-statistic → off-diagonal U-statistic) before it reached any figure.
- **Claude Code built the complete research product:** the reproducible pipeline, the figures, the interactive explorer, the landing page, and the narrated video walkthrough.

### Rigor & honesty (the moat)
- The direction score is an **8-hour transcriptional readout, not a functional assay** — cytokine/proliferation/killing assays are the required next step.
- At two donors the positive quadrant is **not brake-enriched** (a curated 29-gene brake set, one-sided Mann–Whitney p = 0.70) — but the machinery axis is unanimous in both donors, and CBLB (+ donor-consistent CD5/DGKA) land positive. The null is a **two-donor power limit, not a null result about these calls.**
- Three of five candidates are **donor-split (n = 2)** — a prioritized shortlist for the full four-donor cohort, not a finished target list. We say "candidate," never blanket "druggable."

### Reproducibility (in tiers)
- `make smoke` — dependency-free core tests (E-distance + signed axis + figure), runs anywhere.
- `make figure` — regenerates every figure and the interactive dataset offline from the shipped leaderboard.
- `python brake_enrichment.py` — the honest p = 0.70 null, anywhere.
- `make direction` — the genome-scale signed-axis scoring (needs a GPU workstation + the public built h5ad).
Fixed seeds; version-pinned environment; MIT-licensed.

### What's next
Run the full **4-donor / Stim-48 h** cohort to firm up the donor-split brakes; corroborate the ranking against the dataset's provided **DESeq2** result; then functional validation (cytokine / proliferation / cytotoxicity) on the top candidates.

---

### Links
- **GitHub repository:** https://github.com/duanchengchen-oss/brakepoint
- **Project page (live) + video walkthrough + interactive explorer:** https://duanchengchen-oss.github.io/brakepoint/deliverables/
- **Video walkthrough (direct, ~2:54, 1080p/4K):** https://duanchengchen-oss.github.io/brakepoint/deliverables/brakepoint_video.mp4
- **Written summary:** https://github.com/duanchengchen-oss/brakepoint/blob/main/deliverables/summary.md

> Note: if the form requires a YouTube/Vimeo/Loom video URL specifically, upload `deliverables/brakepoint_video.mp4` (in the repo) and paste that link; the gh-pages links above work for direct playback.

### Built with (tools / tech)
Claude Science · Claude Code · Anthropic Claude · Python (scanpy, scVI, energy-distance / E-test as in scPerturb, pandas, numpy, matplotlib) · NVIDIA DGX Spark (remote compute) · Open Targets · ChEMBL · ClinicalTrials.gov · STRING · Remotion (video) · F5-TTS (narration) · GitHub Pages.

---
*Chengchen (Sam) Duan · duanchengchen@gmail.com · github.com/duanchengchen-oss · Built with Claude: Life Sciences (Research track).*
