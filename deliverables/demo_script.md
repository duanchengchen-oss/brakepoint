# Demo video — narration script + optional enhancements

**The submission video is complete and narrated:** `deliverables/demo.mp4`
(1920×1080, ~2:45, 8 beats, real voiceover generated with edge-tts
`en-GB-SoniaNeural`). The script below is exactly what is narrated (also in each
slide's speaker notes in `demo_deck.pptx`). Everything here regenerates from
`_video/`: `gen_tts.py` (voiceover) → `build_narrated.py` (assembles the cut).

---

### Slide 0 · Title (~10s)
> What if the biggest hit in your screen is the worst drug target? This is
> Brakepoint — a signed causal map of T-cell function, built with Claude Science.

### Slide 1 · The question (~17s)
> Our question: in human T cells, which knockdowns make the cell a better
> effector, and which just break it? The better-effector genes are the brakes —
> release them, and you boost immunity. But they hide among twelve thousand
> knockdowns, across two and a half million cells.

### Slide 2 · How Claude Science got us there (~27s)
> Everything here was built with Claude Science, and every number carries its
> provenance. Each result is a versioned artifact — its code, its environment, the
> conversation behind it. A background reviewer checks every claim against what
> actually ran; it caught a real statistical bug before it reached a figure. The
> heavy compute runs on a DGX Spark — the map over two-point-six million cells, in
> forty seconds.

### Slide 3 · The method — two axes (~25s)
> The method has two axes. Effect size — an energy distance — tells you how much a
> knockdown changes the cell. But magnitude can't separate a drug target from
> essential machinery; both land far from control. So we add direction: a per-cell
> score. Positive, the knockdown pushes cells toward the effector program — a
> brake. Negative, it's required machinery.

### Slide 4 · Validation (~23s)
> And the map validates itself. Unsupervised, eight of the nine largest effects are
> the T-cell-receptor module — ZAP70, the CD3 complex, LAT. The direction axis flags
> fourteen of the top fifteen as machinery, not targets — and both donors agree,
> every time. That machinery result is the load-bearing one.

### Slide 5 · The signed causal map (~21s)
> This is the map. Effect size across the bottom, direction up the side. In teal,
> the largest, most consistent effects — the machinery: knock it down, you cripple
> the cell. Up top, in amber, the sparse positive quadrant: knockdowns that enhance
> effector function — the therapeutic hypothesis space a magnitude-only ranking
> would never have looked at.

### Slide 6 · The positive quadrant, honestly (~25s)
> And we report that quadrant honestly. Known brakes like CD5 and DGKA do land
> there, donor-consistent — a consistency check. But at two donors it isn't yet
> enriched for known brakes, and its strongest raw hits include likely artifacts.
> So the positive side is a prioritized hypothesis space for the full cohort; the
> validated result is the machinery axis.

### Slide 7 · Close (~10s)
> Fully open source — fixed seeds, one command to reproduce. The whole map, from
> raw cells to this figure, built with Claude Science.

---

## Optional enhancement (only if you want it — the video is already complete)
For an extra "how Claude Science got you there" punch, screen-capture ~15 s of the
live Claude Science workspace and picture-in-picture it over **slide 2**
(a versioned run artifact + the reviewer catching the bug) and **slide 5** (the run
that produced `ranked_perturbations.csv`). The narrated cut stands on its own
without this.
