# T-cell Perturb-seq → causal targets — the pipeline (Claude Science handoff)

This folder is the **cooperation contract with Claude Science**. It contains a runnable,
red-team-hardened pipeline. The division of labor:

| Role | Who | What |
|---|---|---|
| **Engine** | **Claude Science** (your Mac) | runs the real single-cell analysis in its sandbox, on the datasets you grant; emits auditable artifacts (code+env+provenance) and reviewer checks |
| **Co-pilot** | **me (Cowork)** | writes/updates this pipeline + skill + tests + scoring in the shared `~/Claude Hackathon` folder; reads Claude Science's artifacts back from the folder; verifies & critiques; iterates |

I can't sign into Claude Science or run its sandbox (that's your account + its process),
but everything up to and after it flows through this shared folder. The E-distance **core is
already unit-tested** here (`make smoke`); the full pipeline runs in Claude Science.

## Cooperate — the loop
1. **You:** open Claude Science, sign in (Max), grant it this folder (`~/Claude Hackathon`).
2. **You:** "Load the skill in `pipeline/SKILL.md` and run it on `data/ShifrutMarson2018.h5ad`."
   (Or drag `run_pipeline.py`; Claude Science will `pip install` the env and execute it.)
3. **Claude Science:** runs it, writes `outputs/ranked_perturbations.csv` + figures back here,
   with a provenance trail + reviewer findings.
4. **Me:** I read `outputs/`, sanity-check the numbers, red-team the hero call, and hand back
   fixes / the next step. Repeat.

> Prefer me to drive the Claude Science GUI directly (verify install, load the skill, kick off
> the run)? Say so and I'll request desktop-control access — **except sign-in, which is yours**
> (I never enter credentials).

## Run it
```bash
make smoke       # dependency-free: unit-tests the E-distance core (works anywhere, incl. here)
make synthetic   # tiny end-to-end on synthetic AnnData (needs scanpy/anndata -> Claude Science)
make hero        # full pipeline on real data -> outputs/ranked_perturbations.csv
```
`make smoke` already passes in the Cowork sandbox (proof the core statistic is correct).
`synthetic`/`hero` need the `environment.yml` stack, i.e. Claude Science or your own env.

## Data (verified)
- **Primary:** Shifrut & Marson 2018, primary human CD8⁺ T cells, 48 sgRNAs, 2 donors ×
  stim/nostim — **GEO GSE119450**, via the scPerturb harmonized `ShifrutMarson2018.h5ad`
  (~871 MB, **CC-BY-4.0**, guide calls already in `.obs['perturbation']` so you never parse
  feature barcodes). [scPerturb Zenodo 13350497](https://zenodo.org/records/13350497)
- **Smoke/fallback:** Datlinger 2017 CROP-seq Jurkat (**GSE92872**, ~39 MB) — same pipeline,
  runs in minutes; expected biology (ZAP70/LCK/LAT KO blunt TCR signature) validates the code.
- **The story:** Shifrut's hits include **RASA2**, later independently validated as a CAR-T
  enhancer ([Carnevale 2022, *Nature*](https://www.nature.com/articles/s41586-022-05126-w)) —
  so "our minimal pipeline re-nominates a clinically-relevant target" is a real recover-then-extend narrative. Nominate a fresh, under-studied hit the same way for the novel "hero".
- *Note:* Schmidt 2022 CRISPRa (GSE190604) is **not** in scPerturb → forces raw-GEO guide
  parsing; keep as a Day-6 stretch only, not primary.

## Rigor — the red-team fixes that are baked in (this is what wins trust)
1. **Rank by E-distance magnitude, power-equalized** — not by p (permutation significance
   scales with cell count; a `make smoke`-style demo shows a strong 120-cell hit outranking a
   trivial 500-cell one).
2. **Viability flag** — per-perturbation cell recovery vs control; toxic KOs deplete and
   silently drop out, which reverses a naive ranking. Flagged, not hidden.
3. **On-target knockdown check** — target-gene expression drop vs control; proof the guide worked.
4. **Donors as replicates, not cells** — report donors/perturbation; pseudobulk per
   (perturbation × donor); require ≥2 concordant guides/gene. (Shifrut has 2 donors — a real
   limitation to state, with per-donor concordance shown.)
5. **No double-dipping** — DE on all guide-assigned cells (intention-to-treat); mixscape is a
   *sensitivity* analysis, not the selection step you then test on.
6. **Direction-of-effect concordance = a pre-registered funnel**, not a claim — only ~1% of
   gene–disease pairs have a genome-wide-significant directional call, so count coverage
   honestly and treat "no direction" as missing. ([npj Drug Discovery 2025](https://www.nature.com/articles/s44386-025-00027-0))
7. **Reproducible** — fixed seeds, `environment.yml` + `make lock`, one-command `make hero`.

## The 3-minute demo this is designed to feed
Open on the *result*: "recovered known T-cell regulators (SOCS1/CBLB/RASA2), then flagged one
novel concordant target with a testable prediction — KO it in CD8 T cells, cytotoxicity rises."
Then show **how Claude Science got you there** (provenance trail on the hero → reviewer agent
challenging then hardening it → `make hero` regenerating the ranked causal shortlist from a
clean clone (the concordance + hero-nomination module lands D3–D5, then joins `make hero`).
Close with the wet-lab experiment (the Gladstone hook). No live agent runs on camera.

## 6-day solo timeline
- **D1** env + `make smoke` + run on Datlinger (39 MB) → validate E2E on real data.
- **D2** download Shifrut (871 MB); QC/normalize/PCA; check perturbation/donor labels.
- **D3** power-equalized E-distance + E-test → ranking; reproduce Shifrut ordering (finding #1).
- **D4** donor-aware pseudobulk DE + viability/knockdown; lock the reproducible finding.
- **D5** novel-target path + Open Targets concordance funnel + tractability/safety; pick the hero.
- **D6** reproducibility (seeds/lock/one-command), write-up (100–200w), record the 3-min demo, buffer.
