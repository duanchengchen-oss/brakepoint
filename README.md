# Brakepoint · druggable-brake target discovery in human T cells — Built with Claude Science

*Checkpoint-blockade therapy works by releasing **brakes** on T cells (CAR-T, separately, is engineered antigen recognition that brake-removal can enhance). Brakepoint screens the genome for the druggable brakes.*

**Built with Claude: Life Sciences · research track (solo).** From a
2.6-million-cell CRISPRi Perturb-seq screen, Brakepoint prioritizes a shortlist of
**candidate targets** whose knockdown shifts human CD4⁺ T cells toward an effector
transcriptional state — led by **CBLB**, whose inhibitors are in early-phase trials. Every target traces
back to versioned, Claude-Science-provenanced code.

> **Demo (≤3 min):** [`deliverables/demo.mp4`](deliverables/demo.mp4) · narration deck with verbatim VO in the speaker notes: [`deliverables/demo_deck.pptx`](deliverables/demo_deck.pptx) · script: [`deliverables/demo_script.md`](deliverables/demo_script.md) · **Landing page:** [`deliverables/index.html`](deliverables/index.html) · **Written summary:** [`deliverables/summary.md`](deliverables/summary.md)

![Target shortlist — convergent-evidence matrix](deliverables/figures/target_matrix.png)

## The finding — a shortlist of druggable T-cell brakes
A T-cell "brake" is a gene whose knockdown makes the cell a stronger effector.
From the **genome-scale Gladstone CRISPRi Perturb-seq** (**2,638,736 CD4⁺ T cells,
12,449 knockdowns**), Brakepoint prioritizes **five candidate targets for validation** by convergent
evidence (causal effect · direction · donor consistency · druggability · immune
genetics · clinical precedent):

- **CBLB** *(lead)* — E3-ligase brake; its inhibitors are in early-phase trials (NX-1607 Ph1, HST-1011 Ph1/2); autoimmune genetic association.
- **CD5, DGKA** — donor-consistent; DGKA is clinically tractable (Bayer oral DGKα inhibitor, Ph1), CD5 is biologically supported (deletion enhances CAR-T preclinically).
- **SMAD3, UBASH3A** — a high-effect TGF-β node and a genetics-led (autoimmune-GWAS), currently-undrugged phosphatase.

**How we find them.** Ranking by causal effect alone points at the wrong genes: 8
of the 9 largest effects are the cell's own TCR machinery — activation-required,
unsuitable inhibition targets for this objective. A per-cell **direction-of-effect** axis flips it — 14 of the top 15
effects are required machinery (knockdown *cripples* the cell), donor-consistently
— and the drug-relevant candidates surface in the high-effect, coherent part of the positive quadrant.

The **positive quadrant** (knockdown *enhances* effector function) is the
therapeutic hypothesis space — and we report it honestly. At 2 donors it is noisy:
a curated set of 29 known T-cell brakes shows **no significant evidence of enrichment** there (one-sided Mann–Whitney vs background, p = 0.56; `pipeline/brake_enrichment.py`), and the strongest raw
positives include likely artifacts. Individual literature brakes — **CD5, DGKA**
(donor-consistent), and the TGF-β node **SMAD3** (donor-split) — do land positive
as a consistency check, but the positive side is a **prioritized hypothesis space
for the full 4-donor cohort, not a finished target list**. Full write-up:
[`pipeline/real-finding-genomescale.md`](pipeline/real-finding-genomescale.md).

## Why it's trustworthy
- **Ranks by causal effect size** — power-equalized energy distance + a
  permutation E-test — not p-values, which inflate with cell count.
- **Adds the missing sign.** Magnitude can't tell an activation-*required* gene
  from a therapeutic *brake* — both land far from control. The signed axis does,
  and it self-validates: the TCR machinery is correctly flagged negative,
  donor-consistently.
- **Gated + honest:** viability (catches toxic knockdowns), author-provided
  knockdown efficiency, **donor-stratified** with a per-donor sign-agreement flag (two donors; no
  donor-level population inference).
- **Self-checking:** a real statistical bug — an n-dependent bias in the
  effect-size metric — was found and fixed with the Claude Science reviewer's help
  (see [`pipeline/WAR_LOG.md`](pipeline/WAR_LOG.md)).

## Reproduce
```bash
cd pipeline
make smoke      # dependency-free unit tests: E-distance core + signed axis + figure (runs anywhere)
make figure     # regenerate the target shortlist + all four figures
python brake_enrichment.py  # the honest brake-enrichment null (p=0.56)
# genome-scale (needs scanpy + the built h5ad on a GPU workstation):
make direction  DATA=<built.h5ad> LIB=<sgrna_library_metadata.csv> CONTROL=control
```
Fixed seeds, pinned `environment.yml`, one-command regeneration.

## How Claude Science got us there
Every result is a versioned artifact carrying its exact code, environment, and
conversation trail; a background reviewer checks claims against what actually ran.
The heavy genome-scale analysis runs on an **NVIDIA DGX Spark** over Claude
Science's SSH remote-compute; the signed direction axis over 2.64 M cells
completes in ~40 s.

## Repository layout
```
pipeline/
  edistance_core.py        power-equalized E-distance + permutation E-test (unbiased U-statistic)
  run_pipeline.py          QC → scVI embedding → E-distance ranking → viability + knockdown gates
  direction.py             signed effector-vs-dysfunction axis (CD4 + CD8 modules; unit-tested)
  direction_genomescale.py per-cell scoring on the 2.64M-cell build (row-chunked; runs on the DGX)
  merge_direction.py       merge the signed score + tier into the leaderboard
  figure_causal_map.py     the signed causal map (discovery engine)
  figure_targets.py        the convergent-evidence TARGET matrix (centerpiece)
  figure_evidence.py       donor-consistency scatter + direction distribution
  brake_enrichment.py      honest brake-enrichment test (Mann-Whitney, p=0.56)
  dossiers/                per-target evidence (Open Targets · ChEMBL · ClinicalTrials)
  Makefile · environment.yml · LICENSE (MIT) · SOURCES.md
  outputs_gladstone/       ranked_perturbations.csv (+ direction_*), direction_meta.json, figures
  real-finding-genomescale.md   the finding, with real numbers + honest caveats
deliverables/
  demo.mp4 (Remotion, natural VO) · demo_deck.pptx · index.html · summary.md
  figures/  target_matrix · causal_map · donor_consistency · direction_dist · brakepoint_onepager
```

## Data & license
Code: **MIT** ([`pipeline/LICENSE`](pipeline/LICENSE)). Primary data: the
Gladstone genome-scale CD4⁺ T-cell CRISPRi Perturb-seq (Marson lab; CZI Virtual
Cells Platform) — the expression matrix (the release also includes a DESeq2 DE result and supplementary tables, not used here).
Public evidence layers: **STRING v12** (interactome) and **Open Targets** (human
genetics); public validation sets (Shifrut/Marson, Datlinger) via scPerturb. There
is **no Gladstone-provided interaction network or regulatory model** — STRING and
Open Targets are public layers on top of the provided Perturb-seq data, not
substitutes for it. Provenance and licenses in
[`pipeline/SOURCES.md`](pipeline/SOURCES.md); only openly-licensed evidence is
bundled (no DrugBank).

---
*Repository: https://github.com/duanchengchen-oss/brakepoint · Demo video: https://duanchengchen-oss.github.io/brakepoint/deliverables/index.html*
