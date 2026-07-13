# Record the narration in your own voice (optional — the strongest voiceover)

The demo ships with a metric-validated Azure Dragon-HD voice (UTMOS ~4.37, human
range). If you'd rather use a genuine human read, that's the one thing that beats
any TTS — and it's a 5-minute job:

1. Record each of the 10 lines below as a separate file in this folder:
   `deliverables/_video/human_vo/slide_0.mp3` … `slide_9.mp3`
   (any of .mp3/.m4a/.wav/.aac works; phone voice memo is fine — just record in a
   quiet room, hold a steady pace, leave ~0.3 s of silence at the start/end).
2. Run: `python deliverables/_video/build_from_human_vo.py`
   That copies your clips in, recomputes the per-scene timing, rebuilds the
   captions, and re-renders `demo.mp4` — one command, no other edits needed.

Read naturally, like explaining it to a smart colleague. Gene names are spelled
phonetically in brackets only as a hint — say them normally.

---

**slide_0 · Title**
Checkpoint immunotherapy works by releasing the brakes on a T cell. So we went looking for those brakes — genome-wide. This is Brakepoint, built with Claude Science.

**slide_1 · The thesis**
Those brakes matter beyond checkpoint therapy — they also throttle engineered CAR-T. So across the genome, which genes are the brakes — which knockdowns push a human T cell toward a stronger effector state?

**slide_2 · The screen**
We started from a genome-scale CRISPR-interference screen: over twelve thousand gene knockdowns, across two-point-six million primary human CD4 [cee-dee-four] T cells, from the Gladstone Institutes. Two donors, out of an intended four.

**slide_3 · The trap (significance)**
How do you find the brakes in twelve thousand knockdowns? The reflex is to rank by significance — but at two million cells that breaks down: over ninety-seven percent of the tested knockdowns clear the bar. So we rank by causal effect size instead.

**slide_4 · The engine (signed map)**
But effect size alone still points at the wrong genes — the biggest hits are the cell's own signaling machinery. So we add what a magnitude ranking leaves out: direction — toward the effector program, or away. Now the machinery falls away, and the candidate brakes rise into view.

**slide_5 · Why it's different**
And that's the edge. Differential expression finds correlations — not what to drug. Genetics points to a locus, rarely a direction. We measure what a knockdown actually does, and which way it pushes — then weigh it against genetics and the clinic.

**slide_6 · The shortlist**
From that map, five prior-informed candidates: CBLB [cee-bee-el-bee], CD5 [cee-dee-five], DGKA [dee-gee-kay-alpha], SMAD3 [smad-three], and UBASH3A [you-bash-three-A] — each scored across seven lines of evidence, from causal effect and direction to human genetics and clinical precedent.

**slide_7 · The lead (CBLB)**
Our lead is CBLB [cee-bee-el-bee]. It's a natural off-switch for T-cell activation, and inhibitors are already in early-phase trials. Its genetics point the same way, and it lands in our brake quadrant. CD5 and DGKA come next — and both hold up across donors.

**slide_8 · Reported honestly**
And we're honest about what two donors can support. CD5 and DGKA hold up in both; the other three ride on one donor. As a group, known brakes aren't significantly enriched — so this is a ranked shortlist for the full cohort, a hypothesis to test, not a finished answer.

**slide_9 · Close**
Every number traces back to versioned code — and to a self-check that caught a real bias in our energy-distance statistic: a null scoring five instead of zero. Open source; every figure regenerates with one command. Brakepoint, built with Claude Science.
