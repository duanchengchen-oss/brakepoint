# Demo video — narration script (target discovery)

**The submission video is complete and narrated:** `deliverables/demo.mp4`
(1920×1080, ~2:57, a **Remotion motion-graphics build** — animated signed causal
map, a significance-wall beat, a vs-traditional comparison, target-shortlist and
donor-consistency plots) with a natural voiceover (edge-tts
`en-US-AndrewMultilingualNeural`; gene/acronym pronunciations are respelled in
`_video/gen_tts.py` and verified by round-tripping each clip through Whisper). The
script below is what is narrated. Reproduce: `deliverables/_remotion/`
(`npm i && npm run render`); voiceover from `_video/gen_tts.py`.

---

### 1 · Title
> Checkpoint immunotherapy works by releasing the brakes on a T cell. So we went
> looking for those brakes — genome-wide. This is Brakepoint, built with Claude
> Science.

### 2 · The thesis
> Those brakes matter beyond checkpoint therapy — they also throttle engineered
> CAR-T. So across the genome, which genes are the brakes — which knockdowns push a
> human T cell toward a stronger effector state?

### 3 · The screen
> We started from a genome-scale CRISPR-interference screen: over twelve thousand
> gene knockdowns, across 2.6 million primary human CD4 T cells, from the Gladstone
> Institutes. Two donors, out of an intended four.

### 4 · The trap — significance can't rank a million-cell screen
> How do you find the brakes in twelve thousand knockdowns? The reflex is to rank by
> significance — but at two million cells that breaks down: over ninety-seven percent
> of the tested knockdowns clear the bar. So we rank by causal effect size instead.

### 5 · The discovery engine — the signed causal map
> But effect size alone still points at the wrong genes — the biggest hits are the
> cell's own signaling machinery. So we add what a magnitude ranking leaves out:
> direction — toward the effector program, or away. Now the machinery falls away,
> and the candidate brakes rise into view.

### 6 · Why it's different — vs the usual playbook
> And that's the edge. Differential expression finds correlations — not what to drug.
> Genetics points to a locus, rarely a direction. We measure what a knockdown
> actually does, and which way it pushes — then weigh it against genetics and the
> clinic.

### 7 · The target shortlist
> From that map, five prior-informed candidates: CBLB, CD5, DGKA, SMAD3, and UBASH3A
> — each scored across seven lines of evidence, from causal effect and direction to
> human genetics and clinical precedent.

### 8 · The lead — CBLB
> Our lead is CBLB. It's a natural off-switch for T-cell activation, and inhibitors
> are already in early-phase trials. Its genetics point the same way, and it lands
> in our brake quadrant. CD5 and DGKA come next — and both hold up across donors.

### 9 · Reported honestly
> And we're honest about what two donors can support. CD5 and DGKA hold up in both;
> the other three ride on one donor. As a group, known brakes aren't significantly
> enriched — so this is a ranked shortlist for the full cohort, a hypothesis to test,
> not a finished answer.

### 10 · Close
> Every number traces back to versioned code — and to a self-check that caught a real bias in our energy-distance statistic: a null scoring five instead of zero. Open source; every figure regenerates with one command. Brakepoint, built with Claude Science.
