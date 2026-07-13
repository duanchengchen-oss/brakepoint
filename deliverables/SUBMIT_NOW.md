# Brakepoint — SUBMIT NOW (copy-paste fill sheet)

**Built with Claude: Life Sciences** (Anthropic × Cerebral Valley × Gladstone Institutes) · **Research track**.
Field-by-field. Paste each fenced block into the matching field on the Cerebral Valley form. CV field names vary slightly — map by meaning; everything you need is below.

---

## ⚠️ HUMAN STEPS (only you can do)

1. **Log in** to the Cerebral Valley platform (Google/email) and open the *Built with Claude: Life Sciences* project-submission form. It is login-gated, so this part can't be automated.
2. **Paste each field** below in order. Copy the text inside each fenced block (not the field label).
3. **Upload the cover image**: `deliverables/figures/brakepoint_onepager.png` (2.6 MB, in the repo). If the form wants a wider hero shot instead, use a screenshot of the live project page.
4. **Video field**: the direct link below plays fine as a URL. *Only if the form strictly demands a YouTube/Vimeo/Loom link*, upload `deliverables/brakepoint_video.mp4` there first, then paste that URL. Otherwise use the gh-pages link as-is.
5. **Team size** is 2 max — this is a **solo** submission; add only yourself.
6. Click **Submit**.

> Note: the event page currently shows "Event Closed" for the public listing. If the private submission form is also closed, use the contact/organizer channel from your acceptance email — the content below is final either way.

---

## LINK STATUS (verified live — HTTP 200 on 2026-07-13)

| Link | Status |
|---|---|
| Repo — https://github.com/duanchengchen-oss/brakepoint | ✅ 200 |
| Live project page + walkthrough + explorer — https://duanchengchen-oss.github.io/brakepoint/deliverables/ | ✅ 200 |
| Video (direct .mp4) — https://duanchengchen-oss.github.io/brakepoint/deliverables/brakepoint_video.mp4 | ✅ 200 |
| Written summary — https://github.com/duanchengchen-oss/brakepoint/blob/main/deliverables/summary.md | ✅ 200 |
| Methods deep-dive — https://github.com/duanchengchen-oss/brakepoint/blob/main/pipeline/METHODS.md | ✅ 200 |
| Self-audit / bug war-log — https://github.com/duanchengchen-oss/brakepoint/blob/main/pipeline/WAR_LOG.md | ✅ 200 |

All six were re-checked after the latest push. (Every link is now live — the earlier METHODS.md gap is fixed.)

---

## Project name
```
Brakepoint
```

## Tagline / one-liner  (≤120 chars — this one is 102)
```
Genome-scale engine that rediscovers CBLB blind and names five candidate T-cell brake targets to test.
```
Alternates if you prefer (all ≤120):
- `Brakepoint reads a 2.6M-cell T-cell screen to tell candidate drug targets from essential machinery.` (99)
- `2.6M cells, zero hints: Brakepoint rediscovers CBLB blind and names five candidate T-cell brake targets.` (104)

## Track
```
Research — "build from the bench." A reproducible finding from the Gladstone T-cell Perturb-seq dataset: a ranked, testable list of candidate cancer-immunotherapy targets.
```

## Team / participants (max 2 — solo)
```
Chengchen (Sam) Duan — solo
duanchengchen@gmail.com
github.com/duanchengchen-oss
```

## Dataset used
```
The genome-scale primary human CD4+ T-cell CRISPRi Perturb-seq screen from the Marson lab (Gladstone Institutes) with the Pritchard lab (Stanford) — 2,638,736 cells, 12,449 gene knockdowns (bioRxiv 10.64898/2025.12.23.696273; released via the CZI Virtual Cells Platform). Brakepoint is a computational discovery on this public data: the analysis that turns the screen into a ranked, testable target list.
```

---

## Elevator pitch (short description — 2–3 sentences)
```
The best cancer immunotherapies cut the brakes off a patient's T cells, but only a handful of those brakes have ever been drugged. Brakepoint reads a public 2.6-million-cell, genome-wide human T-cell screen and tells a real candidate target from the machinery a cell needs to survive — with zero prior hints it rediscovered CBLB, already advancing through clinical trials, then surfaced four more candidates. One person built the fully reproducible system in one week, running the genome-scale analysis on an NVIDIA DGX Spark through Claude Science.
```

## Description / About (long — the form usually gives plenty of room; use it)
```
Brakepoint is a genome-scale discovery engine for the next generation of cancer-immunotherapy drug targets.

THE FINDING. Brakepoint delivers five candidate T-cell "brake" targets for the next experiment — genes whose shutdown pushes human T cells toward a stronger fighter state, the direction checkpoint drugs exploit:
• CBLB (lead, the face-validity proof) — rediscovered from raw data with zero prior hints. Oral CBL-B inhibitors NX-1607 (Phase 1) and HST-1011 (Phase 1/2) are already in trials.
• CD5 — donor-consistent; deleting it enhances CAR-T cells preclinically.
• DGKA — donor-consistent; Bayer has advanced an oral inhibitor into Phase 1.
• SMAD3 — a high-effect control point in the TGF-β suppression pathway.
• UBASH3A — a currently undrugged phosphatase backed by type-1-diabetes and rheumatoid-arthritis genetics.

WHY IT'S HARD, AND WHAT'S NEW. At 2.6 million cells, ~97.5% of knockdowns clear q<0.05, so significance can no longer rank targets — and ranking by raw effect size points straight at essential machinery. The comparative proof: of the top 20 knockdowns by raw effect size, 18 push the cell toward a WEAKER fighter state when switched off (the 8 of the 9 very largest are the T cell's own TCR-signaling core — genes you must never inhibit). Brakepoint fixes both failures at once: it ranks by a coverage-equalized effect size (significance demoted to a quality gate) and adds a SIGNED direction axis — stronger-fighter vs weaker-state — that separates a candidate brake from essential machinery. Each of the five finalists is then scored across seven independent lines of evidence: causal effect, direction, donor consistency, screen fitness, target tractability, immune genetics, and clinical precedent.

BUILT WITH CLAUDE. Claude Science ran the genome-scale analysis remotely on an NVIDIA DGX Spark — signed direction scoring across all 2,638,736 cells in ~40 seconds — and an adversarial self-critique caught and fixed a real n-dependent bias in the effect-size math (a pure null scoring ~5 instead of ~0) before it could reach any figure. Claude Code built the complete research product: the reproducible pipeline, the figures, the interactive explorer, the landing page, and the narrated video walkthrough. Every result is a versioned artifact carrying its exact code, environment, and conversation trail, with a background reviewer agent checking each claim against what actually ran.

The payoff: five candidate T-cell targets to test — and a blueprint for AI-native drug discovery.
```

## How it works (method — if there's a dedicated field)
```
For every one of the 12,449 knockdowns, Brakepoint asks two questions inside one donor-integrated map (scVI latent):
1) How hard did the shutoff hit the cell? A coverage-equalized energy distance (E-distance), with every knockdown compared at a matched cell count and a 1,000-permutation E-test used only as a gate — not as the ranker.
2) Which way did it push the cell? A single signed axis — a 16-gene fighter program (IFNG, IL2, TNF, GZMB, TBX21, …) minus a 13-gene exhaustion program (PDCD1, CTLA4, LAG3, TOX, …) — scoring whether switching the gene off moved cells toward a stronger or weaker state.
Together these give both the size and the meaning of every effect: a large shift toward a weaker state flags essential machinery; a shift toward a stronger state drops the gene into the candidate-brake search space (2,016 of 11,438 tested knockdowns, 1,286 donor-consistent). Donor agreement, fitness, knockdown quality, and public evidence (Open Targets, ChEMBL, ClinicalTrials.gov, STRING) then turn a signal into a testable target case. Full walkthrough: pipeline/METHODS.md.
```

## Reproducibility (if there's a field; otherwise fold into Description)
```
Tiered and offline-friendly. `make smoke` runs dependency-free core tests (E-distance + signed axis + figure) anywhere. `make figure` regenerates every figure and the interactive dataset from the shipped leaderboard — no download or GPU. `python brake_enrichment.py` reproduces the honest enrichment null. `make direction` recomputes the genome-scale signed axis (needs a GPU workstation + the public built h5ad). Fixed seed (0); version-pinned environment (environment.yml); MIT-licensed.
```

## Limitations (put the honest caveats HERE, not in the pitch)
```
• The direction score is an 8-hour transcriptional readout, not a functional assay — cytokine / proliferation / killing assays are the required next step, and we say "candidate," never "validated drug."
• This submission uses two of the four available donors (D1 + D2, Stim 8h). Against that two-donor background, a broad curated 29-gene known-brake set is not statistically enriched in the positive quadrant (one-sided Mann–Whitney p = 0.70) — an inconclusive two-donor power limit, not a null result about the specific calls. The machinery axis is unanimous in both donors, and CBLB (plus donor-consistent CD5 and DGKA) still land positive.
• Three of the five candidates are donor-split (n = 2): a prioritized shortlist for the full four-donor cohort, not a finished target list.
Next: run the full 4-donor / Stim-48h cohort, corroborate against the dataset's provided DESeq2 result, then functional validation on the top candidates.
```

---

## Links (paste into the matching link fields)
```
GitHub repository:        https://github.com/duanchengchen-oss/brakepoint
Live project page:        https://duanchengchen-oss.github.io/brakepoint/deliverables/
Video walkthrough (~2:54): https://duanchengchen-oss.github.io/brakepoint/deliverables/brakepoint_video.mp4
Interactive explorer:     https://duanchengchen-oss.github.io/brakepoint/deliverables/index.html
Written summary:          https://github.com/duanchengchen-oss/brakepoint/blob/main/deliverables/summary.md
Methods deep-dive:        https://github.com/duanchengchen-oss/brakepoint/blob/main/pipeline/METHODS.md
Self-audit / bug war-log: https://github.com/duanchengchen-oss/brakepoint/blob/main/pipeline/WAR_LOG.md
```

## Built with (tools / "tech used" tags)
```
Claude Science · Claude Code · Anthropic Claude · Python (scanpy, scVI, energy-distance / E-test as in scPerturb, pandas, numpy, matplotlib) · NVIDIA DGX Spark (remote GPU compute) · Open Targets · ChEMBL · ClinicalTrials.gov · STRING · Remotion (video) · F5-TTS (narration) · GitHub Pages
```

## Cover / thumbnail image (upload)
```
deliverables/figures/brakepoint_onepager.png   (2.6 MB, in the repo)
```

---
*Chengchen (Sam) Duan · duanchengchen@gmail.com · github.com/duanchengchen-oss · Built with Claude: Life Sciences (Research track).*
