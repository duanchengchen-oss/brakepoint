# Demo video — narration script (target discovery)

**The submission video is complete and narrated:** `deliverables/demo.mp4`
(1920×1080, ~2:58, a **Remotion motion-graphics build** — animated signed causal
map + significance-wall beat, target-shortlist and donor-consistency plots) with a
natural voiceover (edge-tts `en-US-AndrewMultilingualNeural`; gene/acronym
pronunciations are respelled in `_video/gen_tts.py` and verified by round-tripping
each clip through Whisper). The script below is what is narrated. Reproduce:
`deliverables/_remotion/` (`npm i && npm run render`); voiceover from
`_video/gen_tts.py`.

---

### 1 · Title
> Checkpoint immunotherapy works by releasing the brakes on a T cell. So we went
> looking for those brakes — genome-wide. This is Brakepoint, built with Claude
> Science.

### 2 · The thesis
> Those brakes matter beyond checkpoint therapy — they also throttle engineered
> CAR-T cells, so taking them off could help there too. So here's the question we
> asked: across the genome, which genes are the brakes? Which knockdowns push a
> human T cell toward a stronger effector state?

### 3 · The screen
> We started from a genome-scale CRISPR-interference screen: over twelve thousand
> gene knockdowns, across 2.6 million primary human CD4 T cells, from the Gladstone
> Institutes. Two donors, out of an intended four.

### 4 · The discovery engine — the signed causal map
> Now, the usual way to rank a screen is by p-value. But at two million cells, the
> statistics call almost everything significant — so instead, we rank by causal
> effect size. There's a catch: the biggest effects are the cell's own signaling
> machinery. Knock those down, and you cripple the very response you're trying to
> boost. So we added a second axis the magnitude ranking leaves out — direction. It
> asks whether a knockdown lifts the cell's effector program, or drops it. And with
> that, the machinery drops to the bottom, and the candidate brakes we're after
> come into view.

### 5 · The target shortlist
> From there, we put forward five prior-informed candidates: CBLB, CD5, DGKA, SMAD3,
> and UBASH3A.
> Each one is scored across seven lines of evidence — the causal effect, its
> direction, whether it holds across donors, viability, druggability, human
> genetics, and whether anyone has taken it into clinical trials.

### 6 · The lead — CBLB
> Our lead is CBLB. It's a natural off-switch for T-cell activation, and inhibitors
> are already in early-phase trials. Its genetics point the same way, and it lands
> in our brake quadrant. CD5 and DGKA come next — and both hold up across donors.

### 7 · Reported honestly
> And we're honest about what two donors can support. CD5 and DGKA are consistent in
> both. The other three ride on a single donor — and as a group,
> known brakes aren't significantly enriched yet. So this is a ranked shortlist for
> the full four-donor cohort — a hypothesis to test, not a finished answer.

### 8 · Close
> Every number here traces back to versioned code — and to an adversarial self-check
> that caught a real bias in how we computed the effect size, before it ever reached
> a figure. Open source — every figure regenerates with one command. This is
> Brakepoint, built with Claude Science.
