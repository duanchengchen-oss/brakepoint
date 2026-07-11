# GOAL — autonomous 12-hour push (Sam away)

**North star:** by ~T+12h, a **polished, submission-ready package** for Built with Claude: Life Sciences (research track, hero = **IL2RB**), with everything done except the two hard walls only Sam can clear.

## Definition of done (drive toward all of these)
1. **3-min video** — real, tool-made (HeyGen HyperFrames project `29939a8d-a6ab-47a8-82ab-e521034f5189`; Canva mp4 fallback). MP4 URL saved to `deliverables/VIDEO_URL.txt` + `pipeline/WAR_LOG.md`. Iterate on it if the first cut is weak.
2. **Infographic** — Canva design `DAHPEnceXZE` (PNG exported); refine and reference it in the landing page.
3. **Direction-axis method upgrade** — author `pipeline/direction.py` (per-cell cytotoxic-vs-exhaustion module scoring → signed `direction_score` + tier), unit-test the pure logic, wire into `run_pipeline.py`, add the 2-axis figure spec. (Regenerating the CSV needs a Claude Science re-run — flag it, don't fake it.)
4. **Dossiers** — enrich IL2RB, VAV2, BLNK (+ CBLB) via Open Targets / ChEMBL / ClinicalTrials / PubMed (cached, backoff); keep `real-finding-genomescale.md` accurate.
5. **Deliverables tight + committed** — README, summary, landing page, storyboard consistent with IL2RB; `make smoke` green; commit after every meaningful change.
6. **WAR_LOG current** — every run appends what it did + decisions + open items.

## Autonomy rules (make the calls yourself)
- **Decide and act.** Pick sensible defaults (design candidate, wording, scope) and **log the decision** in `WAR_LOG.md`. Don't wait for Sam.
- **Hard walls — never cross without Sam:** submitting to the CV platform; pushing to a public GitHub remote; entering any credential/password; authorizing connectors. Put these under `### NEEDS SAM`.
- **Honesty:** if a claim can't be verified, mark it. Keep the "recover-then-extend" framing and the honest caveats (STRING/OT substitutes; 2/4 donors; direction axis).
- Prefer the smallest high-impact change; don't add bloat.

## How this runs
Scheduled tasks run **only while the Cowork app is open** (laptop awake). Loop: `results-watcher-dossiers` every ~3h (polish + video-poll + dossiers + verify), `hackathon-self-critique` every 8h (red-team). If the app was closed, they run on next launch.

## State pointers
`CONTEXT.md` · `pipeline/real-finding-genomescale.md` · `deliverables/` · `pipeline/WAR_LOG.md` · deadline **Mon 2026-07-13 21:00 ET**.

## Still needs Sam (blocking, flagged)
- One ~20–40 min **Claude Science re-run** to regenerate the ranking CSV with the new `direction_score` column.
- **GitHub handle** → create/push the public repo.
- Record/overlay the **live Claude Science provenance screen-capture** for demo beat 2 (I can't drive the CS browser tab).
- **Authorize BioRender** (401) if you want the scientific-figure style.
- The **final submission** click.
