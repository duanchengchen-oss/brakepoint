# Research Track Plan v4 — Causal Target Discovery from T-cell Perturb-seq (kickoff-aligned)
**Built with Claude: Life Sciences · July 7–13, 2026 · solo · Claude Max 20x + Claude Science + $200 API**
**Partners:** Anthropic × Gladstone Institutes × Cerebral Valley · ~500 participants · teams ≤2 · fully virtual · prize pool $100k

---

## What changed in v4 (folding in the kickoff video)
Your v3 science is strong and stays. v4 aligns it to how the event *actually* scores you. Six things move the needle:

1. **A pre-recorded ≤3-min demo video IS your score — there is no live pitch.** Both rounds run on the same recorded demo: Stage 1 (async, Jul 14–15) uses it to pick the **Top 6**; Stage 2 (Jul 16) *replays* it to decide 1st/2nd/3rd. No live Q&A to rescue a weak video. For a solo entrant this is the single highest-leverage artifact — promote it from a Day-6 afterthought to a first-class deliverable with the narrative locked by mid-week.
2. **"Show us how Claude Science got you there" is in the track brief — treat it as scored.** Anthropic is showcasing Claude Science (Wed's whole session is a Claude Science overview). Don't just *use* it — make the workflow *visible*: auditable artifacts, the pipeline saved as a reusable skill, the agentic journey. This is free differentiation most entrants will skip.
3. **Use the provided Gladstone dataset, not an arbitrary public one.** Gladstone is handing participants real **immune T-cell sequencing** data (plus DNA regulatory-activity and protein-interaction datasets). Using the blessed data de-risks compliance/novelty and maximizes Gladstone-prize resonance. **Caveat that gates everything:** your causal design assumes a *perturbation* screen. Day-1 audit must first confirm the T-cell set is Perturb-seq/CRISPR — if it's observational scRNA-seq, the causal core breaks and you pivot framing (see §0).
4. **Aim at two prizes, not one.** Placement (1/2/3) is judged on *standardized criteria* — the rubric wasn't shown in the kickoff; **get it Day 1 from the platform/Discord/office hours** and re-weight effort to it. The **Gladstone Institutes Award** is hand-selected for the project with "the most potential to advance science that can overcome disease" — position your disease framing + proposed experiment explicitly for it.
5. **Compliance is a disqualifier, so bake it in Day 1.** *New Work Only:* analysis must happen during the event; you may reuse public datasets and open-source tools, but **do not paste in your own pre-built private pipeline** — rebuild it live. *Open Source:* everything ships under an approved OSS license.
6. **Real deadline: Mon Jul 13, 9:00 PM ET via the CV platform** — earlier than an "end of Day 7" read. Effective build window is Tue 12:30 PM → Mon 9 PM (~6.5 days; Day 1 is a half-day). Plan to be done Sunday; Monday is buffer + submit.

> **Deep-research addendum (v4.1) — see `AIDD-target-discovery-report.md`:** method spine confirmed = **pertpy** (mixscape → E-distance/E-test → **donor-aware pseudobulk DE** → Augur → cNMF/SCENIC). The centerpiece (direction-of-effect concordance) is backed by **genetic support ≈2.6× clinical success** (Minikel 2024). Dataset shortlist, accessions verified: **Schmidt 2022 CRISPRa Perturb-seq (GEO GSE190604)**, **Shifrut 2018 (GSE119450)**, **Frangieh 2021 immuno-oncology (Broad SCP1064)**, harmonized via **scPerturb (Zenodo)**. Cautions folded in: single-cell foundation models (scGPT/Geneformer) often **don't beat PCA/scVI** — don't stake the project on them; **Open Targets prioritisation** already scores most assessment axes — call it, don't rebuild; shared MCP endpoints **rate-limit under load** — snapshot Day 1.

---

## Event mechanics (authoritative — from the kickoff)

**Two tracks.** You're in **Researcher — "Build *From* the Bench":** *Using Claude Science, start from a biological question you've been thinking through and find the existing datasets and tools needed to answer it. Submit something discrete — a finding, a trained model, an analysis others can reproduce — and show us how Claude Science got you there.* (Builder track = "Build Beyond the Bench" with Claude Code — not you.)

**Rules.** New Work Only (from scratch during the event; researchers may start from an existing question + public datasets, but the analysis happens during the event) · Open Source (approved license) · Banned if it violates legal/ethical/platform policy or uses code/data/assets you lack rights to · Team size 1–2, all members approved.

**Submission (due Mon Jul 13, 9 PM ET on the CV platform), exactly three artifacts:**
- **Demo video — 3 minutes maximum** (hard cap).
- **Open-source project repository / code.**
- **Written summary — 100–200 words** (hard range).

**Stage 1 — Asynchronous judging (Jul 14–15).** Judges independently review the three artifacts via the platform using standardized criteria. Output: **Top 6 teams** announced Jul 16 (#announcements).
**Stage 2 — Final round (Jul 16, 12 PM ET).** Each finalist's **pre-recorded 3-min demo is played** during the live session; judges deliberate to set 1st/2nd/3rd + special prizes; winners announced at the closing ceremony. **Judges = Anthropic + Gladstone reps.**

**Prizes — Researcher track:** 1st **$30,000**, 2nd **$10,000**, 3rd **$5,000** (Usage Credits). **Special: Gladstone Institutes Award** — most potential to advance science that can overcome disease, hand-selected by Gladstone.

**Events to attend (each is a strategic tool, not just content):**
- **Tue Jul 7, 12 PM ET — Kickoff** (rules/prizes/judging/technical talks). *→ capture the rubric if shown.*
- **Wed Jul 8, 12–1 PM ET — Claude Science overview (Alexander Tarashansky, MTS).** *→ learn platform features that save you days (skills, connectors, BioNeMo tools: Evo 2, Boltz-2, OpenFold3) and read what Anthropic wants showcased in the demo.*
- **Fri Jul 10, 12–1 PM ET — Sukrit Silas (Assistant Investigator, Gladstone): "From genome to inference without touching a pipette: virtual genome-wide PPI screening leads to real discoveries."** *→ this is a live read on the Gladstone judges' taste: purely computational, genome-scale, yielding real, translatable discoveries. Mirror this framing in your finding + demo.*
- **Daily 5–6 PM ET — Anthropic office hours (#office-hours).** *→ your channel to get the rubric, confirm dataset details, and unblock. Use Day 1.*

---

## 0. Data audit — DO THIS FIRST (Day 1, gating)
Before committing, establish from the actual (ideally the provided Gladstone T-cell) dataset:
- **Is it even a perturbation screen?** (NEW, top gate) Confirm CRISPR/Perturb-seq vs. observational scRNA-seq. *If observational, the causal-perturbation design is invalid — pivot to a defensible non-causal framing (e.g., state-defining programs + genetics + tractability) or fold in the provided PPI dataset.*
- **Perturbation modality** — knockout / CRISPRi (repression) / CRISPRa (activation)? *Sets your direction logic. If CRISPRa, invert everything: activation ≈ gain of function → nominate genes whose activation drives the therapeutic state.*
- **Library composition + size** — which genes are perturbed; how many are **established drug targets** for your indication (decides validation strategy — see §4).
- **Structure** — #donors, stimulation/culture conditions, timepoints, cells per perturbation, guides per gene, control (non-targeting) design.
- **Guide→cell assignment quality** and knockdown-efficiency readout.
- **Provenance + license** (NEW) — record dataset source/terms so the submission is compliant and citable.

→ **Deliverable:** a one-page data-audit note that confirms or rewrites this plan.

## 0b. The finding + a living abstract (draft Day 1, revise daily)
Treat your headline as a *living abstract* you update as evidence lands:
> "[KO/activation] of **Gene X** causally drives the [therapeutic] T-cell state; it carries human-genetic support with **concordant direction** and is druggable yet under-explored — nominated as a target, with a proposed validation experiment."

**Novelty, operationalized (state exact thresholds):** no approved drug (Open Targets known-drugs) AND few/no clinical programs AND below-median publication count for the gene.
**Success criterion:** powered method validation (§4) + a convergent-evidence hero target + one-command reproduction.
**Feed the deliverables now (NEW):** the living abstract is the seed of your **100–200 word summary**; the evidence ladder is the spine of your **3-min demo**. Keep both in view from Day 1 so nothing is retrofitted at the deadline.

---

## 1. Indication + phenotype axis (Day 1)
- **Indication** where your depth is deepest *and* the T-cell data fits (autoimmune or immuno-oncology). *Bias toward a clear disease-overcoming story for the Gladstone award.*
- **Phenotype axis — pre-commit it before looking at results.** Anchor with a published signature, but require robustness across **2–3 orthogonal signatures** and cross-check against a **data-driven axis** (principal axis of perturbation variation). Record the signatures now.
- **Gold set** — established in-screen targets for the recovery eval (N determined in the audit).

---

## 2. Causal core — pseudobulk first, then single-cell
**Fast path (Day 2) — pseudobulk.** Collapse each perturbation to pseudobulk (per gene, per perturbation, per donor), DE vs non-targeting, crude axis score, crude ranking. Purpose: an end-to-end result + first validation number *fast*.

**Full resolution (Day 3) — single-cell.** mixscape-style filtering of non-perturbed (escaped) cells; E-distance for effect magnitude; per-cell signature scoring; per-perturbation shift along the axis (direction + magnitude).

**Controls (critical):**
- **Viability/essentiality** — per-perturbation cell depletion; separate "shifts state" from "kills/arrests cells"; flag/penalize essential genes (bad targets).
- **Donor/batch** — model donor explicitly (per-donor then meta-analyze, or a mixed model); require effects to **replicate across donors** — cross-donor replication is itself validation.
- **Effect size vs. significance** — rank by effect size with significance as a gate (many cells make trivial effects "significant").

**Modality logic:** KO/CRISPRi ≈ loss of function ≈ inhibitor/degrader → genes whose LOF yields the therapeutic state = **inhibitable targets**. (CRISPRa → agonist logic; invert.)

**Toolkit:** scanpy + pertpy (E-distance/`etest`, mixscape) or Seurat + mixscape; AUCell/`score_genes`; pseudobulk via decoupler/edgeR-style. *Run the heavy analysis inside **Claude Science** and save it as a reusable skill so the workflow is auditable and demo-able (§6, and the brief's "show us how Claude Science got you there").*

---

## 3. Enrichment via tiered gates (not a tunable weighted sum)
Replace the weighted score with interpretable gates; rank within tier:
- **Gate A — causal:** significant, robust, viability-clean shift toward the therapeutic axis, replicated across donors.
- **Gate B — human genetics:** genetic support for the indication (Open Targets Genetics / GWAS Catalog) **and direction-of-effect concordance** where available (§3b).
- **Gate C — tractable:** Open Targets tractability / ChEMBL (small molecule / antibody / degrader).
- **Gate D — specificity:** not broadly essential/tox-prone (Human Protein Atlas / GTEx).

**Shortlist = passes A+B+C** (D as tie-break/flag); rank within by causal effect size. **Report sensitivity to gate thresholds** — top nominations should be stable. (Prefer gates over a score for defensibility; if you must score, learn weights on a train split and evaluate held-out.)

## 3b. Direction-of-effect concordance (centerpiece differentiator)
Where human genetics gives a direction (eQTL/pQTL sign, coding LOF vs GOF, Mendelian direction), test whether the perturbation's causal direction **agrees** with the disease-risk direction. Concordant genes are your strongest, most translatable nominations — this is how serious target-ID triages (e.g., the LOF-protective logic behind PCSK9). Be explicit about **coverage** (only some loci carry a usable direction) and report the concordance rate as a validation signal. *This is also your most demo-able single figure — see §5.*

---

## 4. Validation — chosen by the data
Pick based on the audit's gold-set N:
- **If adequately powered** (enough in-screen established targets): known-target recovery (precision@k, AUROC), and report the **library base rate** so recovery isn't trivially inflated.
- **If underpowered** (few known targets in library): lean on (a) direction-of-effect concordance, (b) held-out perturbation prediction / cross-validation of the ranking, (c) cross-donor replication of top hits.

**Always:** ablations (leave-one-gate-out), null baseline (non-targeting / permutation), robustness (signature-swap, threshold sensitivity, donor-holdout).

**The hero (novel) target is a *hypothesis*, not a proven target** — recovery never validates it. Strengthen it with convergent orthogonal evidence and a **credibility ladder**, ending in a **concrete proposed validation experiment** (arrayed CRISPR + phenotypic readout, or a tool-compound assay). Honest hypothesis + next step beats fake certainty with these judges — and the proposed experiment is exactly the "path to overcome disease" the **Gladstone award** rewards.

---

## 5. Reproducibility bundle (= your open-source submission)
- Pin the **dataset snapshot AND the external evidence tables** (Open Targets/GWAS) early — download, don't live-query at the deadline.
- Lockfile + seeds; **one-command regenerate** (ranking + figures); narrative notebook top-to-bottom; README a judge follows blind.
- **Ship a tiny subsampled/synthetic test fixture + `make test`** so a judge can smoke-test in minutes without the full dataset.
- Figures from code. Include the **hero-target evidence-convergence figure** as the key visual — and reuse it as the anchor shot of the demo.
- **Add an approved OSS `LICENSE` + `SOURCES.md` on Day 1** (NEW) — required, and cheap if done early.
- **A short "How Claude Science got us here" section/notebook** (NEW) — the saved skill, auditable artifacts, and the agentic trail. Directly answers the brief and feeds the demo.

Layout: `/data` (snapshots + SOURCES.md) · `/src` (audit, qc, perturbation_effects, concordance, scoring, dossier_agent) · `/notebooks` · `/outputs` · `/tests` (fixture) · README · LICENSE · lockfile · `run_pipeline.py` · `Makefile`.

---

## 5b. The 3-minute demo video (NEW — your highest-leverage artifact)
It carries *both* judging rounds; there is no live pitch. Budget it like a deliverable, not a screen-recording.
- **Lock the narrative by Day 3** with a throwaway 60-sec rough cut, so the story drives the science, not vice-versa.
- **Structure (≈3:00):** (0:00–0:20) the disease question + why it matters → (0:20–0:50) the data + the causal idea → (0:50–1:50) the result: ranked shortlist, the **concordance figure**, the validation number → (1:50–2:30) the **hero target** + proposed experiment (the Gladstone hook) → (2:30–3:00) **reproducibility + how Claude Science got you there** (one-command rerun, the saved skill).
- **Show, don't tell:** live one-command regen and the auditable Claude Science artifacts beat talking-head claims.
- **Overruns are the default for solo editors** — rough-cut Day 5–6, final by Sunday night, Monday is contingency.

---

## 6. Tool mapping
- **Claude Science (Max 20x):** the Perturb-seq/scRNA-seq analysis, QC, signature scoring, perturbation effects, compute; runs on your own infra, **saves the pipeline as a reusable skill** and emits **auditable artifacts** — make both visible in the repo and demo (the brief scores this).
- **Claude Code:** the reproducible repo, scoring/gates, packaging, one-command runner, test fixture, LICENSE/README.
- **$200 API:** agentic per-target dossiers + evals; tier models (Haiku 4.5 extraction / Sonnet 5 reasoning / Opus 4.8 hard synthesis) + prompt caching + batching. Pricing: docs.claude.com. *($200 is the same allotment every participant gets — spend it on dossiers/evals, not brute-forcing analysis Claude Science can do on Max.)*

---

## 7. Seven-day plan (mapped to real dates; fast path + go/no-go gates)
**Day 1 — Tue Jul 7 (½ day; hacking 12:30 PM ET).** Attend kickoff; **grab the rubric + confirm the T-cell dataset in #office-hours (5–6 PM ET).** Data audit (gating, incl. "is it a perturbation screen?") → indication + pre-committed axis + eval design + living abstract + novelty thresholds. Repo scaffold **+ LICENSE + SOURCES.md**. Download/pin external evidence tables. *No pipeline code beyond load/QC — and start it live (New Work Only).*

**Day 2 — Wed Jul 8 (Claude Science talk 12–1 PM ET).** Thin vertical slice (pseudobulk): crude effect → crude ranking → first validation number, end-to-end. **GO/NO-GO:** any signal (recovery trending, or genetic-direction concordance above chance)? If not, narrow scope / re-check the axis. Apply platform tips from the talk.

**Day 3 — Thu Jul 9.** Single-cell upgrade: mixscape, E-distance, per-cell axis, direction + viability + donor controls + cross-donor replication. Refine ranking. **Record a throwaway 60-sec demo to lock the narrative (NEW).**

**Day 4 — Fri Jul 10 (Silas talk 12–1 PM ET — absorb the Gladstone framing).** Enrichment gates + hero target: genetics + direction concordance + tractability + specificity → shortlist; dossiers (API) for top targets; operationalize novelty; pick the hero. **GO/NO-GO:** defensible, novel, concordant hero target? If not, pivot the headline to the method + best-supported known target.

**Day 5 — Sat Jul 11.** Validation & write: powered validation + ablations + null + robustness (signature-swap, donor-holdout); freeze snapshot; write finding + credibility ladder + proposed experiment. **Draft the 100–200 word summary from the living abstract.**

**Day 6 — Sun Jul 12.** Package: runnable README, one-command regen, test fixture/`make test`, convergence figure, "how Claude Science got us here" section. **Rough-cut → near-final 3-min demo.** Aim to be effectively done tonight.

**Day 7 — Mon Jul 13 (deadline 9 PM ET).** Finalize + submit **with hours to spare.** Confirm a clean blind rerun; final demo cut; upload all three artifacts to the CV platform; stop. *Don't test the 9 PM wall.*

> Re-weight this plan toward the official rubric the moment you have it. Everything above is the defensible default if the rubric is generic.

---

## 8. Cut-lines (if behind)
Drop in order: stretch layers (V2G, program-neighbor extension) → fewer dossiers (top 5) → specificity gate → the single-cell upgrade (stay pseudobulk). **Never cut:** a causal ranking, the powered validation, direction concordance (your differentiator), one-command reproduction, the written finding + proposed experiment, the "how Claude Science got you there" thread, and **the 3-min demo** (it is the score).

---

## 9. Submission checklist
**Compliance (Day 1)**
- [ ] Built live during the event (no pre-existing private pipeline pasted in)
- [ ] Approved open-source LICENSE in repo
- [ ] Dataset source/terms recorded (SOURCES.md); rights to all data/code/assets

**Science**
- [ ] Data-audit note (incl. perturbation-screen confirmation)
- [ ] Ranked shortlist via tiered gates (causal + genetics + tractable)
- [ ] Direction-of-effect concordance analysis
- [ ] Hero target: convergent-evidence dossier + credibility ladder + proposed experiment + inhibition/activation flag
- [ ] Validation (recovery if powered, else concordance / held-out / replication) + ablations + null + robustness
- [ ] Hero-target convergence figure

**Deliverables (the three scored artifacts)**
- [ ] Open-source repo: runnable README + pinned snapshots + one-command regen + test fixture/`make test`
- [ ] "How Claude Science got us here" (saved skill + auditable artifacts)
- [ ] Written summary — **100–200 words**
- [ ] Demo video — **≤3:00**, narrative locked by mid-week, disease + hero + reproducibility on screen

**Positioning & logistics**
- [ ] Framed for the Gladstone award (disease impact + proposed experiment)
- [ ] Official rubric checked; effort re-weighted to it
- [ ] Submitted early on the CV platform (well before **Mon Jul 13, 9 PM ET**)
