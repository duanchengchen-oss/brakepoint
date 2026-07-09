# Target Assessment Framework — beyond the perturbation
**What makes a *good* nominated target, and how to score it defensibly**
Companion to `research-track-target-discovery-plan.md` (expands §3 gates and §4 hero target).

---

## The core idea
Perturbation biology answers *one* question: "does modulating gene X move the therapeutic phenotype?" That's **necessary but not sufficient**. A target a serious drug-hunter would back must also survive **Druggability, Safety, Novelty, and Confidence**, and be placed in its **development / clinical context**. This framework turns "interesting hit" into "credible, defensible nomination" — and gives the judges (esp. Gladstone's translational eye) the multi-axis rigor that separates a Top-3 finding from a nice scatter plot.

**Design rules (consistent with the plan's philosophy):**
1. **Interpretable gates + within-tier ranking, not one opaque weighted sum.** Each axis yields explicit flags + a small sub-score with evidence links.
2. **Missing data = "unknown," never silently 0.** Report per-axis coverage.
3. **Confidence ≠ truth.** The novel hero target stays a *hypothesis*; the framework's job is to make the hypothesis maximally credible and to say exactly how sure you are.
4. **Everything links to a public, citable source** (also satisfies the open-source / rights rules).

---

## The five axes

### 1. Confidence — how sure are we the target drives the disease biology?
Convergent, orthogonal evidence beats any single line.
| Signal | Metric | Source |
|---|---|---|
| **Causal (your screen)** | effect size along the therapeutic axis; significance as a *gate*; cross-donor replication; viability-clean | your Perturb-seq analysis (pertpy E-distance / mixscape) |
| **Human genetics** | disease association + **direction-of-effect concordance** (the differentiator) | Open Targets Genetics, GWAS Catalog, gnomAD (coding LOF/GOF), Helix GenoSphere (variant freq) |
| **Orthogonal omics** | eQTL/pQTL, co-expression module membership, other screens | GTEx/eQTL Catalogue, Open Targets |
| **Prior biology** | mechanistic literature consistent with your direction | PubMed / Consensus / Scite MCP |

**Score:** 0–3 by number of *concordant, independent* lines (screen only = 1; screen + genetics-direction = 2; + orthogonal/mechanistic = 3). **Calibrate** the causal axis with known-target recovery (plan §4).

> **Why this axis dominates (evidence):** genetically-supported mechanisms succeed clinically **~2.6×** more often ([Minikel/King 2024, Nature](https://www.nature.com/articles/s41586-024-07316-0); ~66% of 2021 FDA approvals had genetic support, [Ochoa 2022](https://www.nature.com/articles/d41573-022-00120-3)) — and the benefit rises with confidence in the *causal* gene and *direction*. Direction-of-effect concordance is formalized in [GPS-DOE (Nat Genet 2023)](https://www.nature.com/articles/s41588-023-01609-2). Open Targets' disease-agnostic **target prioritisation** already scores most of the other axes (constraint, essentiality, tractability, safety) — call it and extend, don't rebuild. See `AIDD-target-discovery-report.md`.

### 2. Druggability / Tractability — can we actually drug it, and how?
| Signal | Metric | Source |
|---|---|---|
| **Modality buckets** | small-molecule / antibody / PROTAC-degrader / other-clinical tractability tiers | **Open Targets tractability** (the canonical, pre-computed call) |
| **Ligandability (structure)** | pocket detectability; DrugEBIlity 0–0.7; AlphaFold-based pockets when no holo structure | canSAR, fpocket/DrugEBIlity, PDB, AlphaFold DB |
| **Existing chemical matter** | known ligands/tool compounds; ChEMBL max phase; probes | ChEMBL, Probes&Drugs, Guide to Pharmacology (GtoPdb) |
| **Modality fit** | subcellular localization (antibody needs cell-surface/secreted; SM for intracellular) | HPA subcellular, UniProt |

**Score:** 0–3 by best available modality (0 = no tractable modality → *fails Gate C*; 3 = precedented SM/Ab with chemical matter). **Note the *chosen* modality** — it must match your perturbation direction (LOF hit → inhibitor/degrader; GOF → agonist/activator).

### 3. Safety — how likely is on-/off-target toxicity?
The axis most hits fail. Reward **narrow, non-essential** biology.
| Signal | Metric | Source |
|---|---|---|
| **Genetic constraint** | gnomAD **LOEUF** / pLI (high constraint ≈ intolerant ≈ tox risk if inhibited) | gnomAD |
| **Cellular essentiality** | DepMap common-essential / pan-dependency (broad essential = bad target) | DepMap (Chronos) |
| **Organismal essentiality** | mouse KO lethality / severe phenotype | IMPC / MGI |
| **Expression breadth** | tissue specificity (narrow = safer); expression in heart/CNS/liver (anti-targets) | GTEx, Human Protein Atlas |
| **Known liabilities** | curated adverse events, anti-targets (hERG etc.), close paralogs (selectivity risk) | Open Targets safety, Pharos |

**Score:** 0–3 (0 = pan-essential / ubiquitously critical → *hard flag*; 3 = non-essential, tissue-restricted, no known liability). Treat pan-essential genes as **degrader-only or drop**.

### 4. Novelty — how explored / crowded is it?
Your headline claims "druggable yet under-explored" — *operationalize it*.
| Signal | Metric | Source |
|---|---|---|
| **Target illumination** | **Pharos TDL**: Tdark / Tbio (novel) vs Tchem / Tclin (precedented) | Pharos / TCRD |
| **Literature volume** | below-median gene publication count (state the threshold) | PubMed counts, Open Targets |
| **Patent landscape** | composition/method patents naming the target | **Solve Intelligence MCP**, Google Patents |
| **Pipeline density** | # active programs / companies for the target | Open Targets known-drugs, ClinicalTrials.gov |

**Score:** novelty is a **differentiator, not a gate** — a precedented target with a *new indication/mechanism* can still win. Report TDL + pub-count + program-count explicitly so novelty is auditable, not asserted.

### 5. Development & clinical status — the context axis (orthogonal to the score)
Not "good/bad" per se — it *frames* the nomination and adds credibility or opportunity.
| Question | Metric | Source |
|---|---|---|
| Highest clinical phase for **this** indication? | Open Targets known-drugs; ChEMBL `max_phase` | Open Targets, ChEMBL |
| Any drug approved/trialed for **another** indication? (repurposing angle) | drug–target–indication links | DrugBank, GtoPdb, ChEMBL |
| Active trials right now? | recruiting/active studies, sponsors | **ClinicalTrials.gov** API |
| Approved anywhere? | approval status | DrugBank, FDA |

**Use it two ways:** (a) *precedent* — "targets in this family are clinically validated" strengthens confidence; (b) *whitespace* — "Tdark, no programs, but strong causal + concordant genetics" is the high-risk/high-reward hero. State which story you're telling.

---

## Turning axes into a decision (the scoring model)
**Stage 1 — hard gates (pass/fail):**
- **G1 Causal:** significant, robust, viability-clean shift, replicated across donors.
- **G2 Tractable:** ≥1 credible modality (Druggability ≥1).
- **G3 Not disqualifying-unsafe:** not pan-essential/ubiquitously critical *unless* rescued by a degrader/precision modality.

**Stage 2 — rank the survivors:**
1. Primary sort: **Confidence** (causal effect size + concordant lines).
2. Differentiators: **Safety** (favor narrow/non-essential) and **Novelty** (favor under-explored *when* confidence is high).
3. Context tag: **Development/clinical status** (precedent vs whitespace).

**Reporting rules:** show per-axis sub-scores + evidence links + **coverage** (how many axes had data); run **threshold-sensitivity** so the top nominations are stable; never hide an "unknown" as a zero. Prefer this transparent scheme to a tuned weighted sum — it's what a judge (and a real target-review committee) can actually interrogate.

---

## The per-target dossier (what the API agent auto-fills)
For each shortlisted gene, emit a structured dossier — this is your `$200-API` deliverable (Haiku extraction → Sonnet reasoning → Opus synthesis) and the spine of the hero-target figure.

```yaml
gene: SYMBOL (Ensembl/UniProt)
indication: <disease>, phenotype_axis: <signature>
confidence:
  causal: {effect_size, sig, donors_replicated, viability_clean, modality_direction: LOF|GOF}
  genetics: {assoc_source, direction: concordant|discordant|unknown, coverage}
  orthogonal: [eQTL|pQTL|coexpr|other]
  score: 0-3
druggability:
  modalities: {small_molecule, antibody, degrader, other}   # OT tractability tiers
  structure: {pdb|alphafold, pocket: yes|no}
  chemical_matter: {chembl_max_phase, tool_compounds}
  chosen_modality: <>, score: 0-3
safety:
  constraint_loeuf: , depmap_common_essential: bool, mouse_ko: , 
  tissue_specificity: , anti_targets: , score: 0-3, hard_flag: bool
novelty:
  pharos_tdl: Tdark|Tbio|Tchem|Tclin, pub_count: , patents: , programs: 
dev_clinical_status:
  max_phase_indication: , active_trials: [NCT...], approved_elsewhere: , story: precedent|whitespace
gates: {G1: pass|fail, G2:, G3:}
overall: {tier, rank_reason, coverage, key_uncertainties}
proposed_experiment: <arrayed CRISPR + readout | tool-compound assay>
sources: [urls...]
```

---

## Hackathon-scoped subset (what to actually compute in ~6 days, solo)
Don't build all of this by Day 6. **Minimum viable dossier that still reads as rigorous:**
1. **Confidence:** your causal score + **Open Targets genetics & direction** (one API) + 1 mechanistic citation (PubMed/Consensus MCP).
2. **Druggability:** **Open Targets tractability** (one field, pre-computed — highest ROI) + ChEMBL max phase.
3. **Safety:** gnomAD **LOEUF** + DepMap common-essential flag + GTEx/HPA tissue breadth (three cheap, high-signal numbers).
4. **Novelty:** Pharos **TDL** + gene pub-count.
5. **Dev/clinical:** ChEMBL `max_phase` + one ClinicalTrials.gov query.

That's **five APIs**, all free/public, each a single call per gene — batch across your shortlist. Everything else (canSAR pockets, patents, IMPC, paralog selectivity) is a labeled stretch layer you add only if ahead.

---

## Data sources (all public; note licenses for the OSS submission)
| Resource | Gives you | Access | License note |
|---|---|---|---|
| **Open Targets Platform** | tractability, safety, genetics, known-drugs, associations | GraphQL API + BigQuery + bulk | permissive; cite |
| **ChEMBL** | max_phase, ligands, bioactivity | API + bulk | CC BY-SA |
| **Pharos / TCRD** | Target Development Level, illumination | API + bulk | public |
| **gnomAD** | LOEUF/pLI constraint | API + bulk | free |
| **DepMap** | essentiality (Chronos) | bulk (CSV) | CC BY |
| **GTEx / Human Protein Atlas** | tissue expression, localization | API/bulk | free (HPA CC BY-SA) |
| **ClinicalTrials.gov** | trials, phases, sponsors | REST API v2 | public domain |
| **DrugBank / GtoPdb** | approved drugs, pharmacology | GtoPdb open; DrugBank academic | check DrugBank terms |
| **IMPC / MGI** | mouse KO phenotypes | API/bulk | free |
| **PubMed / Consensus / Scite** (MCP) | literature evidence, novelty | MCP connectors | per-source |
| **Solve Intelligence** (MCP) | patents / competitive novelty | MCP connector | per-source |
| **Helix GenoSphere** (MCP) | human variant freq + clinical | MCP connector | per-source |

> **Pin snapshots on Day 1** (don't live-query at the deadline) and record every source in `SOURCES.md`.

---

## How this plugs into the plan
- Replaces plan **§3 Gates B–D** with the fuller Druggability/Safety/Novelty treatment above (Gate A causal is unchanged).
- Feeds plan **§4** hero target: the dossier *is* the credibility ladder; `proposed_experiment` is the Gladstone hook.
- The **five-API minimum** is your realistic Day-4 build; the dossier schema is what the API agent fills; the multi-axis figure is your demo's money shot.

## Honest limitations (say these out loud in the writeup — judges reward it)
- Confidence axis is calibrated by known-target recovery; the *novel* hero is never validated by recovery — it's a ranked hypothesis.
- Tractability/safety calls are database-derived priors, not experimental truth; they de-risk, they don't prove.
- Genetics direction has partial coverage; report the concordance rate, not a cherry-picked locus.
