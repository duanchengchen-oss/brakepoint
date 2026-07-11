# Handoff prompt — paste into a fresh session (with ~/Claude Hackathon connected)

You are continuing a **solo** entry in the **"Built with Claude: Life Sciences"** hackathon (**research track**), working in this folder (`~/Claude Hackathon`). Your job is to **finish a Top-3-caliber submission**. Hard deadline: **Mon Jul 13, 9:00 PM ET**, submitted on the CV platform. The **≤3-minute demo video is the entire score** (both judging rounds run on it); the other two deliverables are an **open-source repo** and a **100–180 word written summary**. There's also a **Gladstone Institutes special prize** for the project with the most potential to advance disease-overcoming science.

## STEP 0 — Orient (read these first, in order)
`CONTEXT.md` (full project state) · `pipeline/real-finding.md` (real results so far) · `gladstone-datasets-integration.md` (the provided-datasets plan) · `research-track-target-discovery-plan.md` · `pipeline/WAR_LOG.md` (open items, newest first) · `dgx-spark-claude-science.md`. Then check `pipeline/outputs/` and `pipeline/outputs_gladstone/` for analysis results.

## Where things stand
- Pipeline built + **bug-fixed** (E-distance is now an unbiased U-statistic). `make smoke` passes.
- **Real runs done:** Datlinger (Jurkat validation) and **Shifrut primary-CD8** (recovers TCR core; re-nominates RASA2; lead = CBLB). 
- **In progress (user runs it in Claude Science on their DGX Spark):** the **genome-scale Gladstone CRISPRi Perturb-seq** + integrated **PPI-network propagation** + **regulatory-model** support → to nominate a **novel** hero. Results will appear in `pipeline/outputs_gladstone/`.

## Hard boundaries (do not violate)
- The heavy single-cell analysis runs in **Claude Science on the user's Spark**. You **cannot drive the Claude Science browser tab** — the user does that. You do everything *around* it: enrichment, figures, writing, packaging.
- **Never** submit/publish/send, change settings, or enter credentials without the user's explicit "yes." **Pause and ask before the final submission.**
- **Don't regress the rigor** (these are load-bearing): rank by **E-distance magnitude** (permutation q is only a gate); **viability** flag before any low-cell drop; **modality-aware** on-target check; **donors as replicates**; concordance is a **differentiator + honest coverage funnel**, not the primary sort; fixed seeds + lockfile + one-command repro.

## Remaining work (in priority order — use a task list)
1. **Ingest results.** When `pipeline/outputs*/ranked_perturbations.csv` exist, read them. Sanity-check that known biology is recovered (validates the method).
2. **Enrichment + NOVEL HERO.**
   - Run `pipeline/concordance.py` (Open Targets `directionOnTarget`/`directionOnTrait`) on the real hits.
   - **PPI network propagation** (personalized PageRank / random-walk-with-restart, `networkx`) on the Gladstone protein-interaction graph, seeded by the E-distance effect sizes → high-diffusion **non-hit neighbors = novel nominations**; keep those in a druggable complex (Open Targets tractability / ChEMBL).
   - **Regulatory support** (Decima/Performer-type) for the top hero: T-cell expression + autoimmune-variant ref-vs-alt effect.
   - Enrich the top hits + hero with **Open Targets, ChEMBL, ClinicalTrials, PubMed, Consensus, bioRxiv** (MCPs rate-limit → one gene at a time, cache to `pipeline/dossiers/<GENE>.json`, exponential backoff). Write `pipeline/outputs_gladstone/hero_dossier.md`: causal + network + regulatory + druggability + a **proposed wet-lab experiment** (e.g. arrayed CRISPR + opposite-modality CRISPRa replication).
3. **Build the three deliverables.**
   - **Demo video (≤3:00, the whole score).** Produce `deliverables/demo_storyboard.md` = shot list + timed voiceover script (build on the demo beats in `pipeline/real-finding.md`): 0:00 disease question → rigor → validation (recovers TCR biology) → the novel concordant druggable hero → **provenance (show Claude Science artifacts + the reviewer agent) + reproducibility**. Assets: a **hero evidence-convergence figure** (SVG/matplotlib, or BioRender MCP), a clean **deck** (pptx or `theme-factory` skill or Canva/SlidesGPT MCP), and a plan to screen-capture the live Claude Science moment (Jam MCP). No live pitch — the recorded video is everything.
   - **Open-source repo.** Polished `README.md` + an **HTML landing page** built to **taste-skill standards** (real design system, grid layout, phosphor-style icons, restrained motion, **no** purple-gradient/centered-hero/emoji slop). Ensure `LICENSE` (MIT), `SOURCES.md`, one-command `make hero`, tests. `git add -A && git commit`.
   - **Written summary:** 100–180 words, from `real-finding.md`, real numbers.
4. **Compliance + reproducibility check.** New-Work-Only (analysis built during the event); OSS license; rights to all data; seeds/lockfile/snapshots; `make smoke` passes.
5. **Verify (high-stakes).** Re-read every claimed number against the CSVs; run `make smoke`; **spawn a red-team subagent** to attack the finding, the stats, and the demo; fix what it finds. Append a dated entry to `pipeline/WAR_LOG.md`.
6. **Submit.** Assemble the three artifacts, then **STOP and ask the user to confirm** before uploading to the CV platform (deadline **Mon Jul 13, 9 PM ET** — submit hours early).

## Tools available
- **Data/evidence MCPs (bio-research plugin):** Open Targets, ChEMBL, ClinicalTrials, PubMed, Consensus, bioRxiv.
- **Design/media MCPs:** BioRender (scientific figures), Canva, HeyGen HyperFrames (HTML→motion graphics), SlidesGPT, Jam (screen recording).
- **Skills:** `pptx`, `docx`, `pdf`, `theme-factory`, `canvas-design`, `deep-research`, and the project's `tcell-perturb-causal-targets`. (The external **Taste Skill**, tasteskill.dev, is worth installing for the landing page; if not installed, apply its principles by hand.)
- MCPs and the sandbox can be flaky — cache, retry with backoff, and prefer snapshots over live-querying near the deadline.

## Quality bar
Substance over flash. Narrative = **recover-then-extend**: the method recovers known T-cell biology, then nominates a **novel, genetically-concordant, druggable** hero from the *provided Gladstone datasets*. Make **"how Claude Science got you there"** visible. One killer figure. State limitations honestly — judges reward it.

Start by reading `CONTEXT.md`, then set up a task list and go. Ask at most 1–2 clarifying questions, and only if genuinely blocked.
