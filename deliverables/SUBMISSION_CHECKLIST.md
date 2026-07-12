# Submission checklist — Built with Claude: Life Sciences (research track)
Deadline: **Mon 2026-07-13 21:00 ET.** Everything an agent can finish is done; the
item under **NEEDS SAM** is the one human-only step.

## Done (in this repo)
- [x] **The science is real — and independently verified.** Signed
      direction-of-effect axis computed on the full **2,638,736-cell** Gladstone
      CD4⁺ build (DGX Spark), merged into the power-equalized E-distance leaderboard.
      All five targets + their trial/genetics claims re-checked against
      ClinicalTrials.gov + PubMed on 2026-07-12 — zero corrections. `make smoke`
      (E-distance core + signed axis + figure) is green.
- [x] **Figures (5)** — `figures/` : `target_matrix`, `causal_map`,
      `significance_wall` (why effect size, not p-value), `donor_consistency`,
      `direction_dist` (+ `brakepoint_onepager.png`). Rendered from real data by
      `pipeline/figure_*.py`; categorical palette validated colorblind-safe.
- [x] **Demo video — narrated motion-graphics, 1080p, ~2:57** — `deliverables/demo.mp4`
      (10-scene **Remotion** build): animated signed causal map, a significance-wall
      beat, a vs-traditional comparison, the target shortlist and donor plots, with a
      synced natural voiceover (edge-tts `en-US-AndrewMultilingualNeural`; gene
      pronunciations verified via Whisper). **Captions:** `deliverables/demo.vtt`
      (shown by default on the landing player). Source + reproducible render in
      `deliverables/_remotion/` (`npm i && npm run render`); narration from
      `_video/gen_tts.py`.
- [x] **Interactive explorer** — the landing embeds a live canvas scatter of all
      **11,438 tested knockdowns**; hover or search any gene (`data/causal_map_points.json`).
- [x] **Narration deck + script** — `demo_deck.pptx` (10 slides, verbatim VO in
      speaker notes) + `demo_script.md` (matches the narrated audio).
- [x] **Landing page** — `deliverables/index.html`: premium dark build, the target
      shortlist, the CBLB lead, a 3-step "how it works" engine, the interactive
      explorer, a "vs traditional discovery" comparison, the honest rigor section, the
      demo video, and the reproduce block. Root `/index.html` redirects to it.
- [x] **Written summary (100–200 words)** — `deliverables/summary.md` (**187 words**).
- [x] **Open-source pipeline** — `pipeline/` (MIT), one-command reproduce
      (`make smoke` anywhere; `make figure` regenerates every figure).
- [x] **Honesty pass (multi-round, Codex-reviewed)** — "candidate" not blanket
      "druggable"; effect-size ranking credited to scPerturb (novelty = the signed
      axis + combination, not a new statistic); the positive quadrant's **null**
      (p = 0.70) and 3-of-5 donor-split are stated plainly; the bug catch is
      attributed to adversarial self-critique, not the passive reviewer; and we say
      plainly **"we generated no data"** — Brakepoint is the downstream analysis of
      the Marson-lab Perturb-seq (bioRxiv 10.64898/2025.12.23.696273).
- [x] **Public repo pushed + live** — github.com/duanchengchen-oss/brakepoint;
      landing live at duanchengchen-oss.github.io/brakepoint/deliverables/ ; fresh-clone
      `make smoke` verified.

## NEEDS SAM (the one human-only step)
- [ ] **Submit on the CV platform** before Mon 21:00 ET — attach `demo.mp4`
      (or the DEMO_URL landing page), the repo URL, and the summary
      (`deliverables/summary.md`, 187 words). This is the only step an agent can't
      do (no platform credentials).

## Optional (the submission already stands on its own)
- [ ] Re-record the voiceover in **your own voice** (or a premium TTS) if you prefer
      it to edge-tts — `demo_deck.pptx` / `demo_script.md` have the verbatim script.
- [ ] Pull the provided **DESeq2 DE result** (CZI VCP) to corroborate the ranking;
      run the full **4-donor / Stim-48 h** cohort to firm up the donor-split brakes.
