# Submission checklist — Built with Claude: Life Sciences (research track)
Deadline: **Mon 2026-07-13 21:00 ET.** Everything an agent can finish is done; the
items under **NEEDS SAM** are the human-only steps.

## Done (in this repo)
- [x] **The science is real.** Signed direction-of-effect axis computed on the full
      **2,638,736-cell** Gladstone CD4⁺ build (DGX Spark), merged into the E-distance
      leaderboard. `pipeline/outputs_gladstone/ranked_perturbations.csv` carries
      `direction_score` + `direction_tier`; `make smoke` (E-distance core + signed
      axis + figure) is green.
- [x] **Hero figure** — `deliverables/figures/causal_map.png` (+ .svg), rendered
      from real data by `pipeline/figure_causal_map.py`. Donor-consistency encoded.
- [x] **Demo video (silent 1080p cut)** — `deliverables/demo.mp4` (2:36, 8 beats,
      keynote-grade slides from `_video/slides.html`).
- [x] **Narration deck** — `deliverables/demo_deck.pptx` (verbatim VO in speaker
      notes) + script `deliverables/demo_script.md` (with the live-capture shot list).
- [x] **Landing page** — `deliverables/index.html` (premium rebuild, real figure,
      honest data framing).
- [x] **Written summary (100–200 words)** — `deliverables/summary.md` Version A
      (167 words) is the submission text.
- [x] **Open-source pipeline** — `pipeline/` (MIT), one-command reproduce.
- [x] **Honesty pass** — the "Gladstone-provided PPI/regulatory model" claim was
      false and is corrected everywhere; the IL2RB druggability wording is corrected;
      donor-split brakes are flagged, not hidden.
- [x] **Public repo pushed** — REPO_URL + DEMO_URL filled; fresh-clone `make smoke`
      verified.

## NEEDS SAM (human-only — hard walls)
- [ ] **Record the 3-min narrated video.** Open `deliverables/demo_deck.pptx`,
      record the voiceover from the speaker notes (one take, ~2:40), and overlay a
      short **live Claude Science screen-capture** for slide 2 (provenance +
      reviewer) and slide 5 (the run behind the figure) — the shot list is in
      `demo_script.md`. Export and replace `deliverables/demo.mp4` (the silent cut
      is the backup / b-roll).
- [ ] **Publish the final video** where the CV platform wants it (or rely on the
      GitHub Pages landing page, already the DEMO_URL) and update the link if needed.
- [ ] **Enable GitHub Pages** on the repo (Settings → Pages → main branch) if it
      isn't auto-enabled, so the landing-page DEMO_URL is live.
- [ ] **Submit on the CV platform** before the deadline.

## Optional polish (nice-to-have)
- [ ] Fetch the provided **DESeq2 DE result** (CZI VCP) and corroborate the
      E-distance ranking against it — a further "used the provided data" win.
- [ ] Run the full **4-donor / Stim-48 h** cohort to firm up the donor-split brakes.
