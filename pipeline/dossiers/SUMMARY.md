# Target Dossier SUMMARY — PRE-REGISTERED EXPECTATION (NOT a result)

**Pass:** 2026-07-09 (results-watcher, CS-independent prep) · **Modality:** KO · **Concordance rule:** concordant = `protective_lof`
**Status:** ⚠️ Provisional. No real `ranked_perturbations.csv` exists yet. Genes below are the **pre-registered expected** top hits for Shifrut/Marson primary-human CD8⁺ T-cell CRISPR-KO screens — they are **NOT** ranked by observed effect size. Ordering is a transparent multi-axis prior (tractability + genetic direction + novelty + safety), to be **overwritten by E-distance ranking** once real results land.

**Data provenance:** ChEMBL v34 and ClinicalTrials.gov v2 columns are **REAL** (queried live this pass via bio-research MCP). Genetic direction + tractability calls are **literature expectation** — Open Targets was unreachable this pass (persistent global rate-limit); OT confirmation is deferred to a future run.

## Concordance funnel (computed via `concordance.py` on `concordance_snapshot.json`)

| genes | any_gwas | genome_wide_sig | directional | concordant |
|------:|---------:|----------------:|------------:|-----------:|
| 8 | 5 | 4 | 4 | **1** |

Only **UBASH3A** is strictly concordant (`protective_lof`) under the KO rule. Three genome-wide-significant genes (SOCS1, CBLB, TNFAIP3) are `risk_lof` → they score **discordant** under a cancer-anchored "LoF-is-protective" rule, yet `risk_lof`-for-autoimmunity is exactly the human proof that these are genuine T-cell brakes (removing them amplifies immunity). The direction convention must be read with the disease anchor in mind — this tension is the honest headline the funnel is designed to surface.

## Ranked table (provisional prior)

| # | Gene | ChEMBL target | Tractability (expected) | Genetic dir → KO concordance | Clinical validation | Safety flag | Provisional call |
|--:|------|---------------|-------------------------|------------------------------|---------------------|-------------|------------------|
| 1 | **CBLB** | CHEMBL4879459 | Small-molecule — **clinically validated** | `risk_lof` → discordant* | 2 oral CBL-B inhibitors (NX-1607 Ph1; HST-1011 Ph1/2) | IRAEs (mechanism-based) | **Positive control / most de-risked** (not novel) |
| 2 | **UBASH3A** | CHEMBL6067628 | Candidate — His-phosphatase + SH3 handle | **`protective_lof` → concordant** | none (novel) | IRAEs plausible | **Expected HERO** — sole concordant + novel + druggable class (direction nuanced) |
| 3 | **CD5** | CHEMBL3712888 | Biologic / cell-therapy (surface antigen) | `risk_lof` (not gw-sig) → no_direction | 15 active CD5 CAR-T/CAR-NK; immunotoxins Ph2 | Tolerance/fratricide | Tractable, but clinical use is anti-tumor-antigen; KO-to-boost is an adjacent hypothesis |
| 4 | **RASA2** | none | Hard (RasGAP) → ex vivo KO only | `none` → no_direction | none (Nature 2022 preclinical CAR-T) | Ras-pathway theoretical | **Highest novelty**, high risk (undruggable, no genetics) |
| 5 | **SOCS1** | none | Hard (SH2 adaptor) → ex vivo KO | `risk_lof` → discordant* | none (KO in cell-therapy programs) | Autoimmunity + lymphoma TS | Strong biology; durability/safety window needed |
| 6 | **TNFAIP3** (A20) | CHEMBL4523200 | Partial (OTU DUB), agonism is hard | `risk_lof` → discordant* (very strong genetics) | none | **Tumor suppressor → lymphoma** | De-prioritize for durable KO despite best genetics |
| 7 | **ARID1A** | CHEMBL6066172 | Low direct; synthetic-lethal (ATR/EZH2) | `none` → no_direction | SL agents in ARID1A-mut tumors | **Tumor suppressor → transformation** | De-prioritize (oncogenic-safety) |
| 8 | **TCEB2** (ELOB) | CHEMBL3259468 | **Misleading** — 100+ PDB are VHL/PROTAC ternary scaffolds, not an ELOB pocket | `none` → no_direction | none | **Likely pan-essential** | De-prioritize (narrow therapeutic window); hit may reflect fitness |

\* `risk_lof` "discordant" = LoF raises autoimmune risk; mechanistically supportive for an IO-enhancing KO but scored discordant under the strict cancer-anchored rule. See per-gene `interpretation_note`.

## Reading guide for the real run
- Rank by **E-distance** (gated: significant · viable · on-target · replicated), then use this concordance layer as the **differentiator**, not the primary sort.
- Join results to this snapshot via `concordance.py`; **map `TCEB2` ↔ `ELOB`** when matching the CSV's gene symbol.
- Re-run Open Targets enrichment to replace the literature-expectation genetic/tractability calls with OT-confirmed values.

*Per-gene detail: see `dossiers/<GENE>.json`. Machine-readable directions: `dossiers/concordance_snapshot.json`.*
