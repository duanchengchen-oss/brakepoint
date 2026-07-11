# Submission checklist — Built with Claude: Life Sciences (research track)
Deadline: **Mon 2026-07-13 21:00 ET**. Everything an agent could finish is done; the items below need Sam.

## Done (in this repo)
- [x] **Demo video (silent 1080p cut):** `deliverables/IL2RB_demo.mp4` — 6 beats, 2:24, real numbers.
- [x] **Narration deck:** `deliverables/IL2RB_demo_deck.pptx` — verbatim voiceover in the speaker notes.
- [x] **One-page infographic:** `deliverables/IL2RB_infographic.png` (+ Canva source linked).
- [x] **Landing page:** `deliverables/index.html` (video embedded).
- [x] **Written summary:** `deliverables/summary.md` — Version A (IL2RB, 155 words) is the submission text; B is the fallback.
- [x] **Open-source pipeline:** `pipeline/` — MIT license, `make smoke` green, real outputs tracked.
- [x] Local git history current (commits through the video rebuild).

## Needs Sam (hard walls — an agent can't do these)
- [ ] **Record the 3-min narrated video.** Open `IL2RB_demo_deck.pptx`, record the voiceover from the speaker notes (one take), and screen-capture the **live Claude Science** run for beat 2 (provenance + reviewer) and beat 5 (hero) — that "how Claude Science got you there" moment is the scored differentiator. Cut to ≤3:00. (`IL2RB_demo.mp4` works as the silent version / b-roll.)
- [ ] **Create the public GitHub repo and push.** Then replace `REPO_URL` in `README.md` and `deliverables/index.html` (3 occurrences: hero button, clone command, footer).
- [ ] **Set the hosted `DEMO_URL`** (upload the final video) if the platform wants a link rather than a file.
- [ ] **Submit on the CV platform** before the deadline.

## Optional polish (nice-to-have, not blocking)
- [ ] Claude Science `run_pipeline.py --direction` re-run to populate the **real** 2-axis figure — `pipeline/direction.py` is authored + unit-tested; `deliverables/direction_axis.svg` is a labeled schematic until then.
- [ ] Authorize BioRender (currently 401) if you want the scientific-figure styling.
- [ ] Swap `deliverables/IL2RB_infographic.png` for the Canva `DAHPEnceXZE` PNG export if you prefer that layout (the sandbox couldn't download it).
