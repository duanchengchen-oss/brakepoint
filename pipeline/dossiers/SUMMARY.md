# Target Dossier SUMMARY — ✅ REAL RESULT (E-distance ranked)

**Pass:** 2026-07-09 (results-watcher, STEP 1 — real results detected) · **Modality:** KO · **Concordance rule:** concordant = `protective_lof`
**Data:** Shifrut & Marson 2018, primary human CD8⁺ T cells, CRISPR-KO (GSE119450), **24,998 cells / 20 perturbations / 2 donors**, seed=0.
**Source:** `outputs/ranked_perturbations.csv` (Claude Science; mtime 2026-07-09T07:25:41Z). Ordering below is the **real power-equalized E-distance ranking** (permutation-gated), no longer a prior.

**Data provenance:** E-distance + gates are REAL (pipeline). ChEMBL v34 and ClinicalTrials.gov v2 columns are REAL (queried live via bio-research MCP). Genetic direction is literature/PubMed expectation — **Open Targets remained globally rate-limited this run (3rd consecutive)**; OT variant-level direction-of-effect confirmation is still pending.

## Concordance funnel (verified live via `concordance.py` on `concordance_snapshot.json`, over the 8 gate-passing hits)

| genes | any_gwas | genome_wide_sig | directional | concordant |
|------:|---------:|----------------:|------------:|-----------:|
| 8 | 2 | 1 | 1 | **0** |

Only **CBLB** is genome-wide-significant + directional (`risk_lof`). Under the strict cancer-anchored KO rule (`concordant = protective_lof`) it scores **discordant / 0 concordant** — but `risk_lof`-for-autoimmunity is precisely the human-genetic signature of a real T-cell brake: if losing the gene causes autoimmunity, inhibiting it boosts anti-tumor immunity. **The sparse funnel is the honest headline** — this 20-gene panel is pre-enriched for known immune brakes, so strict protective_lof concordance correctly returns 0. Direction depends on the disease anchor; surfacing that is the point.

## Ranked table (REAL E-distance order)

| # | Gene | E-dist | q | viab. | Gate | Role | ChEMBL / tractability | Clinical validation | Call |
|--:|------|-------:|--:|------:|:----:|------|----------------------|---------------------|------|
| 1 | **CD3D** | 9.42 | 0.003 | 0.86 | ✅ | TCR-core (accelerator) | CD3 complex CHEMBL2364168; approved T-cell engagers (wrong modality) | Approved class (243 active engager trials) | **Positive control** — validates method, not a KO nominee |
| 2 | **LCP2** (SLP-76) | 6.65 | 0.003 | 0.98 | ✅ | Proximal TCR adaptor (accelerator) | CHEMBL6196086; 0 drugs, undruggable adaptor | none | **Positive control** — not a nominee |
| 3 | **RASA2** | 4.30 | 0.003 | 0.90 | ✅ | RasGAP brake | No ChEMBL target — hard-to-drug → ex vivo KO | none (Nature 2022 CAR-T preclinical) | **Novelty / high-upside** — re-nominated from effect size alone |
| 4 | **CBLB** | 4.07 | 0.003 | 1.32 | ✅ | E3 ligase brake | CHEMBL4879459; small-molecule, clinically validated | 2 oral CBL-B inhibitors (NX-1607 Ph1; HST-1011 Ph1/2) | **LEAD** — sole gw-sig directional hit + druggable + positive control |
| 5 | **CD5** | 3.85 | 0.003 | 1.08 | ✅ | Inhibitory receptor brake | CHEMBL3712888; biologic / cell-therapy | 15 active CD5 CAR-T/CAR-NK (anti-tumor-antigen context) | Supporting; `risk_lof` (not gw-sig) → no_direction |
| 6 | **TCEB2** (ELOB) | 3.66 | 0.003 | 0.93 | ✅ | Elongin B / CBC complex | CHEMBL3259468 — PDBs are VHL/PROTAC scaffolds, not an ELOB pocket | none | De-prioritize — **likely pan-essential** (hit may reflect fitness) |
| 7 | **CDKN1B** (p27) | 1.79 | 0.032 | 0.75 | ✅ | Cell-cycle brake | low direct tractability | none | De-prioritize — **tumor-suppressor** transformation risk |
| 8 | **DGKA** | 0.61 | 0.029 | **2.30** | ✅ | DAG kinase brake | small-molecule inhibitors exist | preclinical IO | Weak effect + **high viability_ratio (2.30) flag** — over-proliferation |
| 9 | ARID1A | 0.82 | 0.169 | 0.62 | ❌ sig | SWI/SNF | synthetic-lethal only | SL agents in ARID1A-mut tumors | Did **not** pass significance gate here |
| 10 | LAG3 | 0.60 | 0.149 | 0.84 | ❌ sig | Checkpoint | antibody (approved class) | relatlimab approved (blockade) | Below gate — checkpoint effect is functional, not transcriptional at rest |

## Reading guide
- The top-2 (CD3D, LCP2) are TCR-signaling **positive controls** — largest effects because their KO ablates signaling; recover-then-extend validation, not nominees.
- The actionable brakes are **RASA2, CBLB, CD5, (TCEB2)**. **Lead = CBLB** (druggable + genetics + positive control); **novelty = RASA2** (Nature-2022-validated, undruggable → ex vivo KO).
- **Prior-run expected hero UBASH3A is NOT in this 20-gene panel** (nor TNFAIP3); SOCS1 is present but scored a **negative** E-distance (did not pass gates). Pre-registered expectations were correctly superseded by real data.
- Next run: retry **Open Targets** for variant-level direction-of-effect (still pending); if the genome-scale Shifrut/Schmidt arm lands, re-rank + rebuild the funnel for a shot at a truly novel hero.

*Per-gene detail: `dossiers/<GENE>.json`. Machine-readable directions: `dossiers/concordance_snapshot.json`. Authoritative narrative: `../real-finding.md`.*

---

## Watcher addendum — 2026-07-10 (results-watcher run 4) — APPEND-ONLY

**No new analysis results this pass** (`outputs/ranked_perturbations.csv` mtime still 2026-07-09T07:25:41Z, unchanged since run 3). The ranked table above is still current. This addendum only **completes dossier coverage** and logs one clinical correction.

**Two missing gate-passing dossiers built this run (REAL ChEMBL v34 + ClinicalTrials.gov v2):** the gate-passing set now has **8/8 dossiers** (`dossiers/*.json`).

| # | Gene | E-dist | Built this run | Real tractability finding | Call |
|--:|------|-------:|:--------------:|---------------------------|------|
| 7 | **CDKN1B** (p27) | 1.79 | ✅ new | ChEMBL SINGLE PROTEIN CHEMBL3758070 (~20 PDBs) but intrinsically-disordered endogenous CDK-inhibitor → **no direct drug, 0 trials**; germline LoF = MEN4 tumor-predisposition | **De-prioritize** — tumor-suppressor transformation risk + low tractability |
| 8 | **DGKA** | 0.61 | ✅ new | **CORRECTION:** not "preclinical" — a **completed Bayer Phase 1** oral DGKα inhibitor **BAY 2862789 (NCT05858164)**, first-in-human in advanced solid tumors/NSCLC, primary completion 2025-09-26 | **De-prioritize as lead** (weakest effect E=0.61 + over-proliferation viab 2.30), but most **clinically de-risked** of the tail |

**Concordance funnel unchanged — re-verified live via `concordance.py`: 8 / 2 / 1 / 1 / 0.** Both CDKN1B and DGKA carry `any_gwas=false` / `no_direction`, so neither enters the directional layer. Lead remains **CBLB**; novelty remains **RASA2**.

**Open Targets: still globally rate-limited (4th consecutive run, 0 successful calls this pass despite 12s+25s backoff).** All genetic directions remain literature/PubMed-grounded, OT variant-level direction-of-effect still unconfirmed.

---

## Watcher addendum — 2026-07-11 (results-watcher run 5) — APPEND-ONLY — ✅ Open Targets recovered (hero)

**No new analysis results** (`outputs/ranked_perturbations.csv` mtime still 2026-07-09T07:25:41Z). Ranked table above is current. This addendum logs the **first successful Open Targets pull in 5 watcher runs** plus a newly-found clinical program.

**Open Targets — REAL, live 2026-07-11 (CBLB, ENSG00000114423):**

| Field | OT value | Read |
|-------|----------|------|
| Tractability (SM) | Structure-with-Ligand ✅, High-Quality-Ligand ✅; Approved/Advanced/Phase-1 buckets ❌ | Small-molecule tractable; clinical buckets lag (OT snapshot predates CBL-B inhibitor trials) |
| Genetic association | hypothyroidism 0.81, urticaria 0.74, myxedema 0.69, multiple sclerosis 0.65 (414 diseases total) | **OT-confirms genome-wide-sig autoimmune genetic association** — the `risk_lof` brake signature, PubMed-only until now |
| Direction of effect | not returned (OT association endpoint = strength, not sign) | `risk_lof` stays mechanism/PubMed-grounded |

OT **re-throttled** before the other 7 gate-passing genes (all currently `any_gwas=false` or non-gw-sig → cannot change the funnel).

**New clinical program (ClinicalTrials.gov, live):** **APN401** (NCT06172894, invIOs GmbH) — ex vivo autologous immune cells transfected with CBL-B-silencing siRNA — **COMPLETED Phase 1** in advanced solid tumors (2024-10-01). The CBLB lead now has **3 clinical programs across 2 modalities** (oral SM: NX-1607, HST-1011; RNAi cell therapy: APN401).

**Concordance funnel unchanged — re-verified live via `concordance.py`: 8 / 2 / 1 / 1 / 0.** Lead **CBLB** (OT-corroborated); novelty **RASA2**.
