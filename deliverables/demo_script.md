# Demo video — narration script (target discovery)

**The submission video is complete and narrated:** `deliverables/demo.mp4`
(1920×1080, ~2:28, a **Remotion motion-graphics build** — animated causal map +
target-shortlist and donor-consistency plots) with a natural voiceover (edge-tts
`en-US-AndrewMultilingualNeural`). The script below is exactly what is narrated
(also in `demo_deck.pptx` speaker notes). Reproduce: `deliverables/_remotion/`
(`npm i && npm run render`); voiceover from `_video/gen_tts.py`.

---

### 1 · Title
> A T cell's brakes are its most validated drug targets. This is Brakepoint —
> druggable-brake discovery from a 2.6-million-cell screen, built with Claude Science.

### 2 · The thesis
> Checkpoint blockade works by releasing the brakes on T cells; CAR-T engineers
> T cells to attack. Both point to the same prize. So we asked: across the genome,
> which druggable genes are the brakes — which knockdowns push a human T cell
> toward a stronger effector state?

### 3 · The screen
> We started from a genome-scale CRISPR-interference screen — over twelve thousand
> gene knockdowns, across 2.6 million primary human CD4 T cells, from the Gladstone
> Institutes. Two donors, of an intended four.

### 4 · The discovery engine — the signed causal map
> Ranking by effect size alone points at the wrong genes: the biggest hits are the
> cell's own essential signaling machinery. So we added a direction-of-effect axis —
> an 8-hour transcriptional readout. Now the machinery drops to the bottom, and the
> drug-relevant brakes rise to the top.

### 5 · The target shortlist
> From that map, five candidate brakes — CBLB, CD5, DGKA, SMAD3, and UBASH3A — each
> scored across seven axes of convergent evidence: causal effect, direction, donor
> consistency, viability, druggability, human genetics, and clinical precedent.

### 6 · The lead — CBLB
> Our lead is CBLB. Its inhibitors are already in early-phase trials, its human
> genetics are directionally consistent with a T-cell brake, and it sits squarely in
> our brake quadrant. CD5 and DGKA follow — consistent across both donors, with
> external tractability evidence.

### 7 · Reported honestly
> And we report it honestly. With just two donors, CD5 and DGKA hold up in both;
> CBLB and the higher-effect candidates are driven by one, and known brakes show
> no significant enrichment as a group. So this is a prioritized shortlist for the
> full four-donor cohort — a hypothesis to validate, not a finished target list.

### 8 · Close
> Every candidate traces back to code — open source, one command to reproduce, built
> with Claude Science.
