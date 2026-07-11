# Demo video — voiceover script + shot list (≤3:00)

**Format:** 8 slides, 1920×1080, ~2:36 silent cut already rendered at
`deliverables/demo.mp4`. Record the voiceover below (one take) onto
`deliverables/demo_deck.pptx` — the same script is in each slide's speaker notes.
Recommended voice: calm, confident, ~150 wpm. Target total ≈ 2:40.

For beats **2** and **5**, overlay a short **live Claude Science screen-capture**
(shot list at the bottom) — that "how Claude Science got you there" moment is the
scored differentiator.

---

### Slide 0 · Title (~7s)
> What if the biggest hit in your screen is the worst drug target? This is a
> signed causal map of T-cell function — built with Claude Science.

### Slide 1 · The question (~22s)
> We started from a simple question: in human T cells, which genes — when you
> knock them down — make the cell a *better* effector, and which just break it?
> The better-effector genes are the brakes: release them and you boost the immune
> response. But in a genome-scale screen, those brakes hide among twelve thousand
> knockdowns across two and a half million cells.

### Slide 2 · How Claude Science got us there (~24s)  ⟵ overlay live CS capture
> Everything you're about to see was built with Claude Science, and every number
> carries its provenance. Each result is a versioned artifact — its exact code,
> environment, and the conversation that produced it. A background reviewer checks
> every claim against what actually ran; it caught a real statistical bug in our
> effect-size metric before it ever reached a figure. The heavy compute runs on an
> NVIDIA DGX Spark — the signed map over 2.6 million cells finishes in about forty
> seconds.

### Slide 3 · The method — two axes (~24s)
> The method has two axes. First, causal effect size — a power-equalized energy
> distance — tells you how *much* a knockdown changes the cell. But magnitude
> alone can't tell a drug target from essential machinery: both land far from
> control. So we add a second axis: a per-cell direction-of-effect score. Positive
> means the knockdown pushes cells *toward* the effector program — a brake.
> Negative means it pushes them away — required machinery.

### Slide 4 · Validation (~22s)
> And the map validates itself. Completely unsupervised, the largest effects are
> the entire TCR-signalling module — ZAP70, the CD3 complex, LAT, PLCG1. The
> direction axis then flags fourteen of the top fifteen as machinery, not
> targets — and it agrees across both donors, every time. A map that gets the
> machinery right is one you can trust to point at the brakes.

### Slide 5 · The signed causal map (~27s)  ⟵ overlay live CS capture
> This is the map. Effect size across the bottom, direction up the side. Down in
> the teal — the largest, most consistent effects — is the machinery: knocking it
> down cripples the cell. The drug signal is the sparse quadrant up top, in amber:
> knockdowns that *enhance* effector function. That's where the real targets
> live — and where a magnitude-only ranking would never have looked.

### Slide 6 · The therapeutic quadrant (~22s)
> In that quadrant the map recovers real drug-target biology. CD5 and DGKA —
> classic inhibitory brakes, consistent across donors, and already being drugged.
> Higher-magnitude candidates like the TGF-beta node SMAD3 are donor-split at two
> donors, so we present them honestly, as a prioritized shortlist for the full
> four-donor cohort. The method is validated; the leads are exactly that — leads.

### Slide 7 · Close (~13s)
> It's fully open source — fixed seeds, one command to reproduce. And the whole
> map, from raw cells to this figure, was built with Claude Science.

---

## Live Claude Science capture — shot list (Sam only)
Record 15–20 s of screen for each; overlay on the matching slide (picture-in-
picture or a quick cut). This is the provenance the judges explicitly reward.

**For slide 2 (provenance):**
1. The Claude Science workspace with a **run/job artifact** open — show the code +
   environment attached to a result.
2. The **reviewer** panel commenting on a claim (ideally the E-distance bug catch,
   or any claim-vs-code check).
3. A glimpse of the **DGX Spark remote run** (the terminal/job log finishing).

**For slide 5 (the hero result):**
4. The run that produced `ranked_perturbations.csv` / the `make direction` step, or
   opening `causal_map.png` as a Claude Science artifact — showing the figure
   traces back to versioned code.

## Recording notes
- One continuous take is fine; leave ~0.5 s between slides.
- If a beat runs long, the silent cut's slide hold can be stretched to match
  (durations in `_video/build_video.py`).
- Keep it honest — the donor-split caveat on slide 6 is a strength, not a hedge.
