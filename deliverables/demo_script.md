# Demo video — narration script (target discovery)

**The submission video is complete and narrated:** `deliverables/demo.mp4`
(1920×1080, **~2:57**, an **11-scene Remotion motion-graphics build** — animated
signed causal map, a significance-wall beat, a **live screen-recording of the
interactive explorer**, a vs-traditional comparison, target-shortlist and
donor-consistency plots, and a result-first close). The voiceover is a **natural
human-voice model** (F5-TTS, open source, cloned from a reference sample) rendered
on the **NVIDIA DGX Spark** via Claude Science remote compute, paced for a natural
cadence; measured naturalness UTMOS ≈ 4.2–4.5, and every gene pronunciation was
verified by round-tripping each clip through Whisper. Captions
(`deliverables/demo.vtt`) are per-sentence and on-brand styled in the landing
player. Reproduce: `deliverables/_remotion/` (`npm i && npm run render`); rebuild
the voiceover + timing with `_video/build_from_human_vo.py`.

---

### 1 · Title / hook
> Checkpoint drugs work by releasing the brakes on a T cell — but they help only a
> minority of patients, because only a handful of those brakes are drugged. So we
> went looking for the rest, genome-wide. This is Brakepoint, built with Claude
> Science.

### 2 · The thesis
> Those brakes matter beyond checkpoint therapy — they also throttle engineered
> CAR-T. So across the genome: which genes are the brakes? And which knockdowns push
> a human T cell toward a stronger effector state?

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

### 6 · Explore it live — the interactive leaderboard
> And this isn't a static picture. Every one of the eleven thousand that passed our
> testing threshold is here to explore — search any gene, hover any point, and read
> its causal effect and its direction. It's the real leaderboard, live.

### 7 · Why it's different — vs the usual playbook
> And that's the edge. Differential expression finds correlations — not what to drug.
> Genetics points to a locus, rarely a direction. We measure what a knockdown
> actually does, and which way it pushes — then weigh it against genetics and the
> clinic.

### 8 · The target shortlist
> From that map, five prior-informed candidates: CBLB, CD5, DGKA, SMAD3, and UBASH3A
> — each scored across seven lines of evidence, from causal effect and direction to
> human genetics and clinical precedent.

### 9 · The lead — CBLB
> Our lead is CBLB. It's a natural off-switch for T-cell activation, and inhibitors
> are already in early-phase trials. Its genetics point the same way, and it lands
> in our brake quadrant. CD5 and DGKA come next.

### 10 · Reported honestly
> We're honest about what two donors can support. CD5 and DGKA hold up in both; the
> other three ride on one donor. Known brakes aren't significantly enriched — but
> that's a two-donor power limit, not a null result. So this stays a ranked shortlist
> for the full cohort, a hypothesis to test, not a finished answer.

### 11 · The result / close
> Five candidate brakes, led by CBLB — a target the industry already drugs, so
> recovering it validates our method. Every figure regenerates from cached outputs
> with one command, checked against a real bug we caught ourselves. Explore the live
> map, clone the code, and help find the brakes today's drugs still miss. Built with
> Claude Science.
