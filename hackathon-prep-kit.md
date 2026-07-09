# Hackathon Prep-Kit — tools, MCPs, skills & prior research
**Everything worth wiring up *before* the clock matters. Curated for the T-cell causal-target-discovery project.**

---

## 1. MCP connectors — status & what's left
**Connected & working (verified):** ✅ PubMed · ✅ Consensus · ✅ alphaXiv (also reads GitHub repos) · ✅ LatchBio.
**Skip these two — both are paid/enterprise, not free:** 💲 Helix GenoSphere (enterprise-only; needs a Helix-provisioned account for approved partners — no self-serve) · 💲 Solve Intelligence (contact-sales, ~$9,300/user/yr, no free trial). **Free substitutes cover the same axes:**
- *Genetics/variant + clinical* (Helix's job) → **gnomAD** (variant freq/constraint, free), **Open Targets Genetics** + **ClinicalTrials.gov** (both now yours via the `bio-research` plugin), **GWAS Catalog** (free).
- *Patents/novelty* (Solve's job) → **Google Patents**, **Lens.org**, **PatentsView API** (all free) + **Pharos TDL** + PubMed counts (already in the framework).

| Connector | What it gives | Serves | Status |
|---|---|---|---|
| **PubMed** (Anthropic) | biomedical literature search + full text | Confidence (mechanism), Novelty | ✅ |
| **Consensus** | evidence-grounded answers over papers | Confidence, quick lit triage | ✅ |
| **alphaXiv** | arXiv/bioRxiv full text **+ read GitHub repos** | methods, and reading *your* GitHub | ✅ |
| **LatchBio** | launch bioinformatics workflows, pull results | heavy compute / pipeline execution | ✅ |
| **Helix GenoSphere** | human variant frequency + longitudinal clinical | Safety, Confidence (genetics) | ⬜ retry |
| **Solve Intelligence** | patent search/analytics | Novelty / competitive landscape | ⬜ retry |

### ⭐ Big win — the `bio-research` plugin (install this)
Surfaced by a skills/plugins search (card in chat). It bundles **both analysis skills and the exact data MCPs my framework needs**, in one install:
- **Bundled MCPs:** **Open Targets (`ot`)**, **ChEMBL**, **ClinicalTrials.gov (`c-trials`)**, PubMed, Consensus, bioRxiv, plus Synapse, Owkin, Benchling, BioRender, Wiley.
- **Why it matters:** the five-API "minimum viable dossier" (Open Targets tractability/genetics, ChEMBL max-phase, ClinicalTrials status) becomes **native MCP calls** instead of hand-rolled REST clients — big time-saver, and cleaner provenance for the demo.

> Still no MCP for: **gnomA​D, DepMap, GTEx, HPA, Pharos** — hit these via public REST/bulk from Claude Science / the Agent SDK. A thin `evidence/` client for just these is worth writing Day 1 (much smaller now that OT/ChEMBL/c-trials are covered by the plugin).

## 2. Skills (searched — here's the honest result)
- **Standalone skills to add:** searched the catalog with life-sciences keywords → **none beyond what you already have.** No new addable standalone skill matched.
- **Already available here:** `docx`, `pptx`, `xlsx`, `pdf` (deliverables), `deep-research` (multi-source fact-checked reports — good for a target's literature dossier), `skill-creator`, `schedule`.
- **The relevant skills live inside the `bio-research` plugin** (§1 ⭐): `single-cell-rna-qc`, `scvi-tools`, `nextflow-development`, `scientific-problem-selection`. Installing the plugin *is* how you "load" them.

**Two custom skills still worth building** (`bio-research` doesn't cover these), and they double as the "how Claude Science got you there" evidence:
- **`perturb-seq`** — audit → pseudobulk → single-cell effects (mixscape/E-distance) → axis scoring → gated ranking.
- **`dossier`** — fills the target-assessment YAML schema per gene (drives the headless Agent SDK batch).

> ⚠️ **I can't author/register skills from this session** (the skill cache here is read-only). Two ways to create the custom ones: (a) build them **inside Claude Science** as reusable skills as you run the analysis (recommended — also satisfies the brief), or (b) add them via **Settings → Capabilities**. I *can* draft their `SKILL.md` contents into this repo (`skills/perturb-seq/`, `skills/dossier/`) as ready-to-install files — say the word.

## 3. Open-source stack (pin versions Day 1)
**Single-cell / perturbation:** `scanpy`, `pertpy` (E-distance/`etest`, mixscape, augur), `scvi-tools`, `anndata`; R alt: `Seurat` + `mixscape`.
**DE / pseudobulk:** `decoupler`, `edgeR`/`DESeq2` (via `pydeseq2`), `limma`.
**Signatures / enrichment:** `AUCell`/`score_genes`, `gseapy`, `blitzgsea`.
**Evidence clients:** `opentargets` (GraphQL), `chembl_webresource_client`, gnomAD GraphQL, DepMap bulk CSVs, `pytrials`/ClinicalTrials.gov API v2, Pharos/TCRD API.
**Repro:** `uv`/`conda-lock` (lockfile), `snakemake` or `make`, `papermill` (parameterized notebooks), `dvc` (data snapshots), fixed seeds.

## 4. Public data (cross-ref `target-assessment-framework.md` §Data sources)
Open Targets · ChEMBL · Pharos/TCRD · gnomAD · DepMap · GTEx · Human Protein Atlas · ClinicalTrials.gov · IMPC/MGI · GWAS Catalog / Open Targets Genetics. **All public** — snapshot & record in `SOURCES.md` for the open-source submission.

## 5. Your prior research  ⟵ *pending your GitHub handle*
> The connected local folder `~/Claude Hackathon` is currently empty, so your prior work must be on GitHub. Tell me your **handle + repo names** (or connect the GitHub connector for private repos) and I'll pull and index:
> - reusable **methods/code** (perturbation analysis, scoring, evidence clients) you can lift in *as public/own code* — but remember **New Work Only**: rebuild the pipeline live during the event; don't paste a finished private pipeline.
> - prior **target lists / findings / notebooks** to seed hypotheses and the phenotype axis.
> - anything reusable as a **skill** (e.g., an existing dossier or QC routine).
>
> I'll drop an annotated index here (`prior-research-index.md`) and flag what's safe to reuse vs. what must be rebuilt for compliance.

## 6. How the project folder assembles
```
~/Claude Hackathon/
  research-track-target-discovery-plan.md     # the v4 plan
  target-assessment-framework.md              # what makes a good target + scoring
  claude-science-automation.md                # how to run CS / headless agent
  hackathon-prep-kit.md                       # this file
  prior-research-index.md                     # (pending GitHub) annotated prior work
  agent/                                       # headless dossier agent (Tier C)
  evidence/                                    # Open Targets/ChEMBL/gnomAD/... clients
  data/  outputs/  notebooks/  src/  tests/    # the reproducible repo (plan §5)
```

## 7. Do-now checklist
- [x] Connected: PubMed, Consensus, alphaXiv, LatchBio
- [x] **Installed `bio-research` plugin** → Open Targets, ChEMBL, ClinicalTrials, bioRxiv now live (BioRender/Synapse/Wiley need OAuth — skip, not needed)
- [x] Decided: **skip Helix GenoSphere + Solve Intelligence** (paid/enterprise) → use free gnomAD / Open Targets Genetics / GWAS Catalog / Lens.org / PatentsView
- [ ] Install Claude Science (Max) + grant `~/Claude Hackathon` (automation doc, Tier A)
- [ ] Give me your **GitHub handle + repos** → I index prior research here
- [ ] Say the word → I draft `skills/perturb-seq/` + `skills/dossier/` SKILL.md files into the repo
- [ ] Confirm installs → I scaffold `agent/` + a slimmer `evidence/` (only gnomAD/DepMap/GTEx/HPA/Pharos now)
