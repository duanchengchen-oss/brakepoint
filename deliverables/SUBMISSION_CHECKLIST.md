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
- [x] **Demo video — narrated motion-graphics, 1080p** — `deliverables/demo.mp4`
      (2:48, built with **Remotion**): an **animated data map** (points fly in, the
      14/15 callout, quadrant reveals), count-up KPIs, kinetic type, spring
      transitions, and a synced **real voiceover** (edge-tts `en-GB-SoniaNeural`).
      Source + reproducible render in `deliverables/_remotion/` (`npm i && npm run
      render`); narration from `_video/gen_tts.py`.
- [x] **Narration deck + script** — `deliverables/demo_deck.pptx` (VO in speaker
      notes) + `deliverables/demo_script.md` (matches the narrated audio).
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

## NEEDS SAM (the one human-only step)
- [ ] **Submit on the CV platform** before Mon 21:00 ET — attach `demo.mp4`
      (or the DEMO_URL landing page), the repo URL, and the summary
      (`deliverables/summary.md`, Version A). This is the only step an agent can't
      do (no platform credentials).

## Optional (the video already stands on its own)
- [ ] Re-record the voiceover in **your own voice** if you prefer it to the TTS
      narration — the deck (`demo_deck.pptx`) has the verbatim script in the notes.
- [ ] Overlay a short **live Claude Science screen-capture** on slides 2 and 5 for
      extra provenance punch (shot list in `demo_script.md`).
- [ ] Fetch the provided **DESeq2 DE result** (CZI VCP) to corroborate the ranking;
      run the full **4-donor / Stim-48 h** cohort to firm up the donor-split brakes.
