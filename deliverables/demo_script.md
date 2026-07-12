# Demo video — narration script (target discovery)

**The submission video is complete and narrated:** `deliverables/demo.mp4`
(1920×1080, ~2:10, a **Remotion motion-graphics build** — animated causal map +
target-shortlist and donor-consistency plots) with a natural voiceover (edge-tts
`en-US-AndrewMultilingualNeural`). The script below is exactly what is narrated
(also in `demo_deck.pptx` speaker notes). Reproduce: `deliverables/_remotion/`
(`npm i && npm run render`); voiceover from `_video/gen_tts.py`.

---

### 1 · Title (~11s)
> A T cell's brakes are its best drug targets. This is Brakepoint — druggable-brake
> discovery from a two-and-a-half-million-cell screen, built with Claude Science.

### 2 · The thesis (~19s)
> The most powerful immunotherapies — checkpoint blockade, CAR-T — all work by
> releasing brakes on T cells. So we asked a simple question: across the entire
> genome, which druggable genes are those brakes? Which knockdowns make a human
> T cell a stronger effector?

### 3 · The screen (~12s)
> We started from a genome-scale CRISPR-interference screen — twelve thousand gene
> knockdowns, across two and a half million primary human CD4 T cells, from the
> Gladstone Institutes.

### 4 · The discovery engine — the signed causal map (~19s)
> Ranking by effect size alone points at the wrong genes: the biggest hits are the
> cell's own essential signaling machinery. So we added a direction-of-effect axis.
> Now the machinery drops to the bottom, and the drug-relevant brakes rise to the
> top. This map is our discovery engine.

### 5 · The target shortlist (~14s)
> From that map, a shortlist of five druggable brakes — each scored across seven
> axes of convergent evidence: causal effect, direction, donor consistency,
> druggability, human genetics, and clinical precedent.

### 6 · The lead — CBLB (~21s)
> Our lead is CBLB — a brake that's already a drug. Two oral CBL-B inhibitors are
> in trials, losing it causes autoimmunity in people, and it sits squarely in our
> brake quadrant. CD5 and DGKA follow — both consistent across donors, both
> clinically tractable.

### 7 · Reported honestly (~19s)
> And we report it honestly. With two donors, CD5 and DGKA hold up in both; CBLB
> and the higher-effect candidates are driven by one donor, and known brakes aren't
> yet enriched as a group. So this is a prioritized shortlist for the full cohort —
> not a finished target list.

### 8 · Close (~8s)
> Every target traces back to code — open source, one command to reproduce, built
> with Claude Science.
